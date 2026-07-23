"""
Build a clean Google Doc from thesis_roadmap.md.
No native tables (avoids complex API issues) — uses formatted text tables.
All writes are in batches of 50 with 1.5s pauses to respect rate limits.
"""
import json, re, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

MD_PATH = "D:/School/1 Projects/thesis/thesis_roadmap.md"
token_path = Path.home() / "AppData/Local/hermes/google_token.json"
creds = Credentials.from_authorized_user_info(json.loads(token_path.read_text()))
docs = build("docs", "v1", credentials=creds)

doc = docs.documents().create(body={"title": "Thesis Roadmap — Predictive Maintenance for Coiled Evaporators"}).execute()
DOC_ID = doc["documentId"]
print(f"Doc: {DOC_ID}")

raw = Path(MD_PATH).read_text(encoding="utf-8")
lines = raw.split("\n")


class Builder:
    """Document builder with batched writes."""

    def __init__(self, service, doc_id):
        self.service = service
        self.doc_id = doc_id
        self.cursor = 1
        self.batch = []
        self.total_reqs = 0

    def _req(self, r):
        self.batch.append(r)
        if len(self.batch) >= 50:
            self.flush()

    def flush(self):
        if not self.batch:
            return
        self.service.documents().batchUpdate(
            documentId=self.doc_id, body={"requests": self.batch}
        ).execute()
        self.total_reqs += len(self.batch)
        print(f"  {len(self.batch)} flushed (total: {self.total_reqs})")
        self.batch = []
        time.sleep(1.5)

    def insert(self, text):
        start = self.cursor
        self._req({"insertText": {"location": {"index": self.cursor}, "text": text}})
        self.cursor += len(text)
        return start

    def para(self, text, style="NORMAL_TEXT", bold=False, italic=False, indent=None,
             sa=4, sb=4, fs=None, color=None):
        """Insert paragraph with newline."""
        s = self.insert(text + "\n")
        e = self.cursor
        ps = {"namedStyleType": style, "spaceAbove": {"magnitude": sa, "unit": "PT"},
              "spaceBelow": {"magnitude": sb, "unit": "PT"}, "lineSpacing": 1.15}
        flds = "namedStyleType,spaceAbove,spaceBelow,lineSpacing"
        if indent is not None:
            ps["indentStart"] = {"magnitude": indent, "unit": "PT"}
            flds += ",indentStart"
        self._req({"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": e},
                                            "paragraphStyle": ps, "fields": flds}})
        ts, tf = {}, []
        if bold: ts["bold"] = True; tf.append("bold")
        if italic: ts["italic"] = True; tf.append("italic")
        if fs: ts["fontSize"] = {"magnitude": fs, "unit": "PT"}; tf.append("fontSize")
        if color: ts["foregroundColor"] = {"color": {"rgbColor": color}}; tf.append("foregroundColor")
        if tf:
            self._req({"updateTextStyle": {"range": {"startIndex": s, "endIndex": e - 1},
                                            "textStyle": ts, "fields": ",".join(tf)}})

    def heading(self, text, level=1):
        sm = {1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3"}
        sa = {1: 18, 2: 14, 3: 10}.get(level, 10)
        sb = {1: 8, 2: 6, 3: 4}.get(level, 4)
        self.para(text, style=sm[level], sa=sa, sb=sb)

    def bold(self, text, indent=None, sa=4, sb=4):
        self.para(text, bold=True, indent=indent, sa=sa, sb=sb)

    def italic(self, text, indent=18):
        self.para(text, italic=True, indent=indent, sa=2, sb=2)

    def bullet(self, text, indent=0, checked=None):
        p = ""
        if checked is True: p = "☑ "
        elif checked is False: p = "☐ "
        else: p = ("  " * indent) + "• "
        self.para(p + text, indent=indent * 18, sa=2 if indent == 0 else 1, sb=1)

    def divider(self):
        s = self.insert("─" * 72 + "\n")
        e = self.cursor
        self._req({"updateTextStyle": {"range": {"startIndex": s, "endIndex": e - 1},
                                       "textStyle": {
                                           "foregroundColor": {"color": {"rgbColor": {"red": 0.6, "green": 0.6, "blue": 0.6}}},
                                           "fontSize": {"magnitude": 6, "unit": "PT"}},
                                       "fields": "foregroundColor,fontSize"}})
        self.para("", sa=1, sb=1)

    def rich(self, runs, sa=4, sb=4, indent=None):
        """Mixed-format line: [(text, {bold,italic,color}), ...]"""
        full = "".join(r[0] for r in runs) + "\n"
        s = self.insert(full)
        e = self.cursor
        ps = {"namedStyleType": "NORMAL_TEXT", "spaceAbove": {"magnitude": sa, "unit": "PT"},
              "spaceBelow": {"magnitude": sb, "unit": "PT"}, "lineSpacing": 1.15}
        flds = "namedStyleType,spaceAbove,spaceBelow,lineSpacing"
        if indent is not None:
            ps["indentStart"] = {"magnitude": indent, "unit": "PT"}
            flds += ",indentStart"
        self._req({"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": e},
                                            "paragraphStyle": ps, "fields": flds}})
        rs = s
        for txt, fmt in runs:
            if not txt: continue
            re_ = rs + len(txt)
            ts, tf = {}, []
            if fmt.get("bold"): ts["bold"] = True; tf.append("bold")
            if fmt.get("italic"): ts["italic"] = True; tf.append("italic")
            if fmt.get("code"):
                ts["weightedFontFamily"] = {"fontFamily": "Consolas", "weight": 400}
                ts["fontSize"] = {"magnitude": 9, "unit": "PT"}
                ts["backgroundColor"] = {"color": {"rgbColor": {"red": 0.92, "green": 0.92, "blue": 0.92}}}
                tf.extend(["weightedFontFamily.fontFamily", "fontSize", "backgroundColor"])
            if fmt.get("color"):
                ts["foregroundColor"] = {"color": {"rgbColor": fmt["color"]}}
                tf.append("foregroundColor")
            if tf:
                self._req({"updateTextStyle": {"range": {"startIndex": rs, "endIndex": re_},
                                                "textStyle": ts, "fields": ",".join(tf)}})
            rs = re_

    def text_table(self, headers, rows):
        """Format a table as clean text with bold headers."""
        # Column widths - calculate from content
        ncols = len(headers)
        col_widths = [len(h) for h in headers]
        for row in rows:
            for ci in range(min(len(row), ncols)):
                col_widths[ci] = max(col_widths[ci], len(str(row[ci])))
        col_widths = [min(w + 2, 60) for w in col_widths]
        total_w = sum(col_widths) + (ncols - 1) * 3 + 4

        # Header
        hdr_cells = []
        for ci, h in enumerate(headers):
            hdr_cells.append(h.ljust(col_widths[ci]))
        hdr_line = "  " + " │ ".join(hdr_cells)
        self.rich([(hdr_line, {"bold": True})], sa=6, sb=1)

        # Separator
        sep_line = "  " + "─┼─".join("─" * w for w in col_widths)
        self.para(sep_line, sa=0, sb=0, fs=6, color={"red": 0.7, "green": 0.7, "blue": 0.7})

        # Rows
        for ri, row in enumerate(rows):
            cells = []
            for ci in range(ncols):
                val = str(row[ci]) if ci < len(row) else ""
                cells.append(val.ljust(col_widths[ci]))
            row_line = "  " + " │ ".join(cells)
            self.para(row_line, sa=1, sb=1)

    def empty(self):
        self.insert("\n")

    def close(self):
        self.flush()
        print(f"\nTotal: {self.total_reqs} requests")
        print(f"URL: https://docs.google.com/document/d/{self.doc_id}/edit")


# ══════════════════════════════════════════
b = Builder(docs, DOC_ID)

# ═══════════════ HEADER ═══════════════════
b.heading("Thesis Roadmap — Predictive Maintenance for Coiled Evaporators", 1)
b.para("Last updated: 2026-07-22")
b.para("Status: ███████░░░ 5% complete")
b.para("Group: John Ronald Pacaldo · Collin Brandon Asio · Simon France Sulibio")

b.rich([
    ("Architecture Decision: ", {"bold": True}),
    ("Unsupervised anomaly detection (primary) + supervised classification (secondary, conditional). Appendix has full A vs B analysis.", {})
])
b.divider()

# ═══════════════ LEGEND ═══════════════════
b.heading("Legend", 2)
b.bold("Type Symbols", sa=6, sb=2)
for e, l in [("📝","Paper Overhaul"),("🔧","Prototyping"),("💻","Coding"),
             ("🤖","Machine Learning"),("📊","Data Collection"),("🚀","Deployment"),("📋","Documentation")]:
    b.para(f"  {e}  {l}", indent=18, sa=1, sb=1)
b.empty()
b.bold("Priority Symbols", sa=4, sb=2)
for s, l in [("🔴","Critical"),("🟠","High"),("🟡","Medium"),("🟢","Low")]:
    b.para(f"  {s}  {l}", indent=18, sa=1, sb=1)
b.empty()
b.bold("Status Symbols", sa=4, sb=2)
for s, l in [("⬜","Not started"),("🔄","In progress"),("🚫","Blocked"),("✅","Completed")]:
    b.para(f"  {s}  {l}", indent=18, sa=1, sb=1)
b.divider()

# ═══════════════ PARSE PHASES ═══════════════════
phases = []
cur_phase = None
cur_goal = ""
cur_lines = []

in_code = False
for line in lines:
    if line.strip().startswith("```"):
        in_code = not in_code
        if cur_phase: cur_lines.append(line)
        continue
    # Stop capturing phase content when we hit post-phase sections
    if cur_phase and re.match(r'^## (Milestones|Risk Registry|Assignment Legend|Appendix)', line):
        phases.append((cur_phase, cur_goal, cur_lines))
        cur_phase = None; cur_lines = []
    pm = re.match(r'^## (Phase \d+ .*)', line)
    if pm:
        if cur_phase: phases.append((cur_phase, cur_goal, cur_lines))
        cur_phase = pm.group(1); cur_goal = ""; cur_lines = []; continue
    gm = re.match(r'^\*\*(Goal:.*)\*\*', line)
    if gm and cur_phase: cur_goal = gm.group(1); continue
    if cur_phase: cur_lines.append(line)
if cur_phase: phases.append((cur_phase, cur_goal, cur_lines))

# ═══════════════ RENDER PHASES ═══════════════════
for pname, pgoal, plines in phases:
    b.rich([(pname, {"bold": True})], sa=16, sb=2)
    if pgoal:
        b.italic(pgoal, indent=14)
    b.empty()

    # Split into sub-sections
    secs = []
    cur = []
    for l in plines:
        s = l.strip()
        if not s: continue
        if s.startswith("---") or s.startswith("```"): continue
        # Detect section headers
        h3 = re.match(r'^### (.+)', s)
        h4 = re.match(r'^#### (.+)', s)
        bld = re.match(r'^\*\*(.+)\*\*$', s)
        if h3 or h4 or bld:
            if cur: secs.append(("content", cur))
            if h3: secs.append(("h3", h3.group(1)))
            elif h4: secs.append(("h4", h4.group(1)))
            else: secs.append(("bold", bld.group(1)))
            cur = []
        else:
            cur.append(l)
    if cur: secs.append(("content", cur))

    for st, sd in secs:
        if st == "h3":
            b.rich([(sd, {"bold": True, "color": {"red": 0.36, "green": 0.05, "blue": 0.18}})], sa=10, sb=2)
        elif st == "h4":
            b.bold(sd, sa=6, sb=2)
        elif st == "bold":
            b.bold(sd, sa=6, sb=2)
        elif st == "content":
            for l in sd:
                s = l.strip()
                if not s: continue
                if s.startswith(">"):
                    b.italic(re.sub(r'^>\s?', "", s), indent=18)
                    continue
                chk = re.match(r'^(\s*)- \[([ x])\]\s+(.*)', s)
                if chk:
                    b.bullet(chk.group(3), indent=len(chk.group(1)) // 2, checked=chk.group(2) == "x")
                    continue
                bul = re.match(r'^(\s*)[*-]\s+(.*)', s)
                if bul:
                    b.bullet(bul.group(2), indent=len(bul.group(1)) // 2)
                    continue
                num = re.match(r'^(\s*)\d+\.\s+(.*)', s)
                if num:
                    b.para(f"  {num.group(2)}", indent=(len(num.group(1)) // 2) * 18, sa=1, sb=1)
                    continue
                # Inline bold
                parts = re.split(r'(\*\*.*?\*\*)', s)
                if len(parts) > 1:
                    runs = [(p[2:-2], {"bold": True}) if p.startswith("**") else (p, {}) for p in parts]
                    b.rich(runs, sa=1, sb=1)
                else:
                    b.para(s, sa=1, sb=1)
    b.divider()

# ═══════════════ MILESTONES ═══════════════════
b.heading("Milestones & Deadlines", 2)
b.text_table(
    ["Date", "Milestone", "Deliverables"],
    [
        ["YYYY-MM-DD", "Phase 1 complete", "Ch1 overhauled, Ch3 pre-proto, architecture locked"],
        ["YYYY-MM-DD", "Phase 2 complete", "2 portable kits assembled, ESP-NOW working, CSV verified"],
        ["YYYY-MM-DD", "Phase 3 complete", "Ch2 overhauled, synthesis matrix, lit aligned with unsupervised"],
        ["YYYY-MM-DD", "Phase 4 complete", "ACS712+ZMPT101B calibrated, DB built, Ch4 draft"],
        ["YYYY-MM-DD", "Phase 5 complete", "Ch3 condensed, 4 models defined, validation protocol"],
        ["YYYY-MM-DD", "Phase 6 complete", "6-mo data collection, 30-40 units, fault injection, checks"],
        ["YYYY-MM-DD", "Phase 7 complete", "CNN vibration autoencoder trained, evaluated"],
        ["YYYY-MM-DD", "Phase 8 complete", "4 unsupervised models + 5 validation layers"],
        ["YYYY-MM-DD", "Phase 9 complete", "Dashboard live, scoring pipeline, Ch3 deployment"],
        ["YYYY-MM-DD", "Phase 10 complete", "Full draft submitted for adviser review"],
        ["YYYY-MM-DD", "Defense", "Presentation, demo, Q&A"],
        ["YYYY-MM-DD", "Final submission", "Hardbound copies + digital archive"],
    ]
)
b.divider()

# ═══════════════ RISK REGISTRY ═══════════════════
b.heading("Risk Registry", 2)
b.text_table(
    ["Risk", "Likelihood", "Impact", "Mitigation"],
    [
        ["Insufficient Abnormal data (0-3 natural faults in 6 months)", "High", "High", "Unsupervised does not need Abnormal labels. Fault injection provides guaranteed validation samples."],
        ["Fault injection permission denied by campus facilities", "Medium", "High", "Engage PPO early. Fallback: retrospective log validation + technician spot-checks."],
        ["Calibration equipment not available at XU labs", "Low", "High", "Confirmed available. Verify access during Phase 1."],
        ["DIY airflow sensor not ready in time (PMV experiment)", "High", "Low", "Conditional — H4 and RQ3 drop silently if sensor fails. No impact on primary thesis."],
        ["30-40 units overwhelming for 2-kit weekly rotation", "Medium", "Medium", "Start with 20 units, expand as process stabilizes."],
        ["Scope too large for 3 members", "Medium", "High", "Cut non-critical tasks. Supervised experiment is conditional — no penalty if skipped."],
        ["Adviser feedback requires major revision", "Medium", "Medium", "Incremental drafts per phase, not one bulk submission."],
        ["Anomaly score confounded by ambient conditions", "Medium", "Medium", "Layer 4 validation: include confounds as control variables. Report transparently."],
        ["CNN spectrogram approach fails (data volume, domain mismatch)", "Medium", "Medium", "Fallback: vibration statistical features (RMS, kurtosis, peak frequency) as tabular features."],
    ]
)
b.divider()

# ═══════════════ ASSIGNMENT ═══════════════════
b.heading("Assignment Legend", 2)
b.text_table(
    ["Abbreviation", "Name"],
    [["JRP", "John Ronald Pacaldo"], ["CBA", "Collin Brandon Asio"], ["SFS", "Simon France Sulibio"]]
)
b.divider()

# ═══════════════ APPENDIX ═══════════════════
b.heading("Appendix: Supervised vs. Unsupervised Decision Summary", 2)
b.para("Three LLMs independently reviewed the methodology choice. Verdict: 3-0 for Unsupervised Anomaly Detection.")

b.bold("Why Unsupervised Won", sa=10, sb=4)
b.text_table(
    ["Reason", "Detail"],
    [
        ["Math is fatal for supervised", "13 known-problem units / 2,599 campus-wide. ~0-3 Abnormal in 30-40 sample. Statistically unvalidatable."],
        ["Labels aren't ground truth", "Technician inspection is subjective proxy — can't see the evaporator non-invasively."],
        ["Matches the thesis claim", "'Flag unusual behavior → prioritize inspection' = anomaly detection, not classification."],
        ["Handles novel failures", "Unsupervised detects ANY deviation from normal. Supervised only detects known failure modes."],
    ]
)

b.bold("Supervised as Conditional Secondary", sa=10, sb=2)
b.para("If controlled fault injection yields ≥ 30 labeled Abnormal samples, run RF/XGBoost/RBF SVM as a comparison experiment. This is a bonus, not a dependency.")

b.bold("Validation Strategy (5-Layer)", sa=10, sb=4)
b.text_table(
    ["Layer", "Method", "Target"],
    [
        ["Layer 1", "Retrospective log comparison — anomaly score separation (known-fault vs healthy)", "Mann‑Whitney U p < 0.05"],
        ["Layer 2", "Controlled fault injection — verify anomaly score rises post-fault", "TPR ≥ 80%"],
        ["Layer 3", "Monthly technician spot-checks — correlate findings with anomaly scores", "Agreement ≥ 70%"],
        ["Layer 4", "Confound verification — score vs ambient temp, humidity, cleaning recency, kit ID", "p > 0.05 per confound"],
        ["Layer 5", "Maintenance reset — cleaned units show anomaly score drop", "Wilcoxon signed‑rank p < 0.05"],
    ]
)

b.close()
