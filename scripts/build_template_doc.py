"""
Build a clean, template-style Google Doc from thesis_roadmap.md.
Batches ALL writes to respect Docs API rate limits (60 writes/min).
Uses proper tables, heading styles, and formatting throughout.
"""
import json, re, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

MD_PATH = "D:/School/1 Projects/thesis/thesis_roadmap.md"

# ── Auth ──
token_path = Path.home() / "AppData/Local/hermes/google_token.json"
creds = Credentials.from_authorized_user_info(json.loads(token_path.read_text()))
docs = build("docs", "v1", credentials=creds)

# ── Create doc ──
doc = docs.documents().create(body={"title": "Thesis Roadmap — Predictive Maintenance for Coiled Evaporators"}).execute()
DOC_ID = doc["documentId"]
print(f"Created doc: {DOC_ID}")

# ── Read markdown ──
raw = Path(MD_PATH).read_text(encoding="utf-8")
lines = raw.split("\n")


class DocBuilder:
    """Builds a Google Doc with batched requests to respect rate limits."""

    def __init__(self, docs_service, doc_id):
        self.service = docs_service
        self.doc_id = doc_id
        self.cursor = 1
        self.pending = []  # batch requests
        self.request_count = 0

    def _add(self, req):
        self.pending.append(req)
        if len(self.pending) >= 50:
            self.flush()

    def flush(self):
        if not self.pending:
            return
        self.service.documents().batchUpdate(
            documentId=self.doc_id, body={"requests": self.pending}
        ).execute()
        self.request_count += len(self.pending)
        print(f"  Flushed {len(self.pending)} requests (total: {self.request_count})")
        self.pending = []
        time.sleep(1.5)  # stay under 60/min rate limit

    def insert_text(self, text):
        """Queue text insert at current cursor. Advances cursor."""
        self._add({
            "insertText": {
                "location": {"index": self.cursor},
                "text": text
            }
        })
        old_cursor = self.cursor
        self.cursor += len(text)
        return old_cursor

    def insert_paragraph(self, text, style="NORMAL_TEXT", bold=False, italic=False,
                         indent=None, space_above=4, space_below=4, font_size=None):
        """Insert a paragraph line (text + newline)."""
        start = self.insert_text(text + "\n")
        end = self.cursor

        # Paragraph style
        ps = {
            "namedStyleType": style,
            "spaceAbove": {"magnitude": space_above, "unit": "PT"},
            "spaceBelow": {"magnitude": space_below, "unit": "PT"},
            "lineSpacing": 1.15,
        }
        fields = "namedStyleType,spaceAbove,spaceBelow,lineSpacing"
        if indent is not None:
            ps["indentStart"] = {"magnitude": indent, "unit": "PT"}
            fields += ",indentStart"

        self._add({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": ps,
                "fields": fields
            }
        })

        # Text style
        ts = {}
        ts_fields = []
        if bold:
            ts["bold"] = True
            ts_fields.append("bold")
        if italic:
            ts["italic"] = True
            ts_fields.append("italic")
        if font_size:
            ts["fontSize"] = {"magnitude": font_size, "unit": "PT"}
            ts_fields.append("fontSize")
        if ts_fields:
            self._add({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end - 1},  # excl newline
                    "textStyle": ts,
                    "fields": ",".join(ts_fields)
                }
            })

    def insert_heading(self, text, level=1):
        style_map = {1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3", 4: "HEADING_4"}
        sa = {1: 18, 2: 14, 3: 10, 4: 8}.get(level, 10)
        sb = {1: 8, 2: 6, 3: 4, 4: 4}.get(level, 4)
        self.insert_paragraph(text, style=style_map[level], space_above=sa, space_below=sb)

    def insert_rich_line(self, text_runs, space_above=4, space_below=4, indent=None):
        """Insert line with mixed formatting runs: [(text, {bold,italic,code}), ...]"""
        full_text = "".join(r[0] for r in text_runs) + "\n"
        start = self.insert_text(full_text)
        end = self.cursor

        # Paragraph style
        ps = {
            "namedStyleType": "NORMAL_TEXT",
            "spaceAbove": {"magnitude": space_above, "unit": "PT"},
            "spaceBelow": {"magnitude": space_below, "unit": "PT"},
            "lineSpacing": 1.15,
        }
        fields = "namedStyleType,spaceAbove,spaceBelow,lineSpacing"
        if indent is not None:
            ps["indentStart"] = {"magnitude": indent, "unit": "PT"}
            fields += ",indentStart"
        self._add({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": ps,
                "fields": fields
            }
        })

        # Apply per-run formatting
        run_start = start
        for text, fmt in text_runs:
            if not text:
                continue
            run_end = run_start + len(text)
            ts = {}
            flds = []
            if fmt.get("bold"):
                ts["bold"] = True
                flds.append("bold")
            if fmt.get("italic"):
                ts["italic"] = True
                flds.append("italic")
            if fmt.get("code"):
                ts["weightedFontFamily"] = {"fontFamily": "Consolas", "weight": 400}
                ts["fontSize"] = {"magnitude": 9, "unit": "PT"}
                ts["backgroundColor"] = {"color": {"rgbColor": {"red": 0.92, "green": 0.92, "blue": 0.92}}}
                flds.extend(["weightedFontFamily.fontFamily", "fontSize", "backgroundColor"])
            if fmt.get("color"):
                ts["foregroundColor"] = {"color": {"rgbColor": fmt["color"]}}
                flds.append("foregroundColor")
            if flds:
                self._add({
                    "updateTextStyle": {
                        "range": {"startIndex": run_start, "endIndex": run_end},
                        "textStyle": ts,
                        "fields": ",".join(flds)
                    }
                })
            run_start = run_end

    def insert_bold_line(self, text, indent=None):
        self.insert_rich_line([(text, {"bold": True})], indent=indent)

    def insert_italic_line(self, text, indent=None):
        self.insert_rich_line([(text, {"italic": True})], indent=indent)

    def insert_divider(self):
        """Thin gray horizontal rule via repeated character."""
        self.insert_rich_line([
            ("─" * 72, {"color": {"red": 0.6, "green": 0.6, "blue": 0.6}, "bold": False})
        ], space_above=2, space_below=2)
        # Override font size to be small
        start = self.cursor - 73  # text + newline
        end = self.cursor
        self._add({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end - 1},
                "textStyle": {"fontSize": {"magnitude": 6, "unit": "PT"}},
                "fields": "fontSize"
            }
        })

    def insert_empty(self):
        self.insert_text("\n")

    def insert_list_item(self, text, indent=0, checked=None):
        prefix = ""
        if checked is True:
            prefix = "☑ "
        elif checked is False:
            prefix = "☐ "
        else:
            prefix = "  " * indent + "• "
        self.insert_paragraph(prefix + text, indent=indent * 18,
                              space_above=2 if indent == 0 else 1, space_below=1)

    def insert_table(self, headers, rows):
        """Insert a real Google Docs table."""
        n_rows = len(rows) + 1  # +1 header
        n_cols = len(headers)
        self.flush()

        # 1) Insert table at cursor
        self.service.documents().batchUpdate(documentId=self.doc_id, body={
            "requests": [{
                "insertTable": {
                    "rows": n_rows,
                    "columns": n_cols,
                    "location": {"index": self.cursor}
                }
            }]
        }).execute()
        self.request_count += 1

        # 2) Get doc to find table cell positions
        doc_info = self.service.documents().get(documentId=self.doc_id).execute()
        body = doc_info.get("body", {}).get("content", [])

        # Find the table cells — scan from roughly our cursor position
        cells_by_pos = {}
        table_start = None
        for elem in body:
            tbl = elem.get("table")
            if not tbl:
                continue
            es = elem.get("startIndex", 0)
            if table_start is None or abs(es - self.cursor) < 5:
                table_start = es
            if abs(es - self.cursor) > 10:
                continue
            for ri, row in enumerate(tbl.get("tableRows", [])):
                for ci, cell in enumerate(row.get("tableCells", [])):
                    cs = cell.get("startIndex", 0)
                    ce = cell.get("endIndex", 0)
                    cells_by_pos[(ri, ci)] = (cs, ce)

        if not cells_by_pos:
            # Cannot find table — jump cursor forward
            self.cursor += 5
            return

        # Determine table end from last cell
        last_end = max(ce for _, ce in cells_by_pos.values())
        self.cursor = last_end + 1

        # 3) Fill cells
        fill_reqs = []
        style_reqs = []

        for ri in range(n_rows):
            for ci in range(n_cols):
                key = (ri, ci)
                if key not in cells_by_pos:
                    continue
                cs, ce = cells_by_pos[key]

                # Cell content
                if ri == 0:
                    content = headers[ci] if ci < len(headers) else ""
                else:
                    content = rows[ri - 1][ci] if ci < len(rows[ri - 1]) else ""

                if content:
                    fill_reqs.append({
                        "insertText": {
                            "location": {"index": cs + 1},
                            "text": content
                        }
                    })

                # Cell styling
                cell_style = {}
                style_fields = ["paddingTop", "paddingBottom", "paddingLeft", "paddingRight"]

                if ri == 0:
                    cell_style["backgroundColor"] = {
                        "color": {"rgbColor": {"red": 0.36, "green": 0.05, "blue": 0.18}}
                    }
                    style_fields.append("backgroundColor")

                cell_style["paddingTop"] = {"magnitude": 4 if ri == 0 else 3, "unit": "PT"}
                cell_style["paddingBottom"] = {"magnitude": 4 if ri == 0 else 3, "unit": "PT"}
                cell_style["paddingLeft"] = {"magnitude": 6, "unit": "PT"}
                cell_style["paddingRight"] = {"magnitude": 6, "unit": "PT"}

                style_reqs.append({
                    "updateTableCellStyle": {
                        "tableCellStyle": cell_style,
                        "fields": ",".join(style_fields),
                        "tableStartLocation": {"index": table_start},
                        "rowIndex": ri,
                        "columnIndex": ci
                    }
                })

        if fill_reqs:
            for i in range(0, len(fill_reqs), 25):
                batch = fill_reqs[i:i+25]
                self.service.documents().batchUpdate(
                    documentId=self.doc_id, body={"requests": batch}
                ).execute()
                self.request_count += len(batch)
                time.sleep(0.5)

        if style_reqs:
            for i in range(0, len(style_reqs), 50):
                batch = style_reqs[i:i+50]
                self.service.documents().batchUpdate(
                    documentId=self.doc_id, body={"requests": batch}
                ).execute()
                self.request_count += len(batch)
                time.sleep(0.8)

        # 4) Bold + white text on header row
        header_style_reqs = []
        for ri in range(n_rows):
            for ci in range(n_cols):
                key = (ri, ci)
                if key not in cells_by_pos:
                    continue
                cs, ce = cells_by_pos[key]
                if ri == 0:
                    hdr_text = headers[ci] if ci < len(headers) else ""
                    if hdr_text:
                        header_style_reqs.append({
                            "updateTextStyle": {
                                "range": {"startIndex": cs + 1, "endIndex": cs + 1 + len(hdr_text)},
                                "textStyle": {
                                    "bold": True,
                                    "foregroundColor": {"color": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}}
                                },
                                "fields": "bold,foregroundColor"
                            }
                        })
                else:
                    # Alternating row background
                    if ri % 2 == 0:
                        bg = {"red": 0.95, "green": 0.95, "blue": 0.95}
                    else:
                        bg = {"red": 1, "green": 1, "blue": 1}
                    header_style_reqs.append({
                        "updateTableCellStyle": {
                            "tableCellStyle": {
                                "backgroundColor": {"color": {"rgbColor": bg}}
                            },
                            "fields": "backgroundColor",
                            "tableStartLocation": {"index": table_start},
                            "rowIndex": ri,
                            "columnIndex": ci
                        }
                    })

        if header_style_reqs:
            for i in range(0, len(header_style_reqs), 50):
                batch = header_style_reqs[i:i+50]
                self.service.documents().batchUpdate(
                    documentId=self.doc_id, body={"requests": batch}
                ).execute()
                self.request_count += len(batch)
                time.sleep(0.5)

    def close(self):
        self.flush()
        print(f"\nTotal API requests: {self.request_count}")


# ══════════════════════════════════════════
builder = DocBuilder(docs, DOC_ID)

# ═══════════════════ HEADER ═══════════════════
builder.insert_heading("Thesis Roadmap — Predictive Maintenance for Coiled Evaporators", 1)
builder.insert_paragraph("Last updated: 2026-07-22")
builder.insert_paragraph("Status: ███████░░░ 5% complete")
builder.insert_paragraph("Group: John Ronald Pacaldo · Collin Brandon Asio · Simon France Sulibio")

builder.insert_rich_line([
    ("Architecture Decision: ", {"bold": True}),
    ("Unsupervised anomaly detection (primary) + supervised classification (secondary, conditional). See appendix for full A vs B analysis.", {})
])

builder.insert_divider()

# ═══════════════════ LEGEND ═══════════════════
builder.insert_heading("Legend", 2)

builder.insert_bold_line("Type Symbols")
for emoji, label in [
    ("📝", "Paper Overhaul"), ("🔧", "Prototyping"), ("💻", "Coding"),
    ("🤖", "Machine Learning"), ("📊", "Data Collection"), ("🚀", "Deployment"),
    ("📋", "Documentation"),
]:
    builder.insert_paragraph(f"  {emoji}  {label}", indent=18, space_above=1, space_below=1)

builder.insert_empty()
builder.insert_bold_line("Priority Symbols")
for sym, label in [("🔴", "Critical"), ("🟠", "High"), ("🟡", "Medium"), ("🟢", "Low")]:
    builder.insert_paragraph(f"  {sym}  {label}", indent=18, space_above=1, space_below=1)

builder.insert_empty()
builder.insert_bold_line("Status Symbols")
for sym, label in [("⬜", "Not started"), ("🔄", "In progress"), ("🚫", "Blocked"), ("✅", "Completed")]:
    builder.insert_paragraph(f"  {sym}  {label}", indent=18, space_above=1, space_below=1)

builder.insert_divider()

# ═══════════════════ PHASES ═══════════════════
# Parse markdown into phase blocks
phases = []
cur_phase = None
cur_goal = ""
cur_lines = []

in_code = False
for line in lines:
    if line.strip().startswith("```"):
        in_code = not in_code
        if cur_phase:
            cur_lines.append(line)
        continue

    pm = re.match(r'^## (Phase \d+ .*)', line)
    if pm:
        if cur_phase:
            phases.append((cur_phase, cur_goal, cur_lines))
        cur_phase = pm.group(1)
        cur_goal = ""
        cur_lines = []
        continue

    gm = re.match(r'^\*\*(Goal:.*)\*\*', line)
    if gm and cur_phase:
        cur_goal = gm.group(1)
        continue

    if cur_phase:
        cur_lines.append(line)

if cur_phase:
    phases.append((cur_phase, cur_goal, cur_lines))

# Process each phase
for phase_name, goal_text, task_lines in phases:
    # Insert phase heading + goal
    builder.insert_rich_line([(phase_name, {"bold": True})],
                              space_above=16, space_below=2)
    if goal_text:
        builder.insert_italic_line(goal_text, indent=18)
    builder.insert_empty()

    # Process each phase — collect all lines first, separate sections, then render
    # Break the phase into sub-sections (delimited by H3/H4/bold headers)
    phase_sections = []  # [(section_header_type, header_text, [content_lines])]
    cur_sec_lines = []
    cur_sec_is_code = False

    def line_is_phase_header(l):
        s = l.strip()
        return bool(re.match(r'^#{3,4}\s+', s)) or bool(re.match(r'^\*\*.+\*\*$', s)) or s.startswith("---")

    for sl in task_lines:
        stripped = sl.strip()
        if not stripped:
            continue

        # Start new section on H3/H4/bold header
        if line_is_phase_header(sl):
            if cur_sec_lines:
                phase_sections.append(("content", cur_sec_lines))
                cur_sec_lines = []
            if stripped.startswith("### "):
                phase_sections.append(("h3", stripped[4:]))
            elif stripped.startswith("#### "):
                phase_sections.append(("h4", stripped[5:]))
            elif re.match(r'^\*\*.+\*\*$', stripped):
                phase_sections.append(("bold_header", stripped[2:-2]))
            continue

        cur_sec_lines.append(sl)

    if cur_sec_lines:
        phase_sections.append(("content", cur_sec_lines))

    # Render the sections
    for sec_type, sec_data in phase_sections:
        if sec_type == "h3":
            builder.insert_rich_line([
                (sec_data, {"bold": True, "color": {"red": 0.36, "green": 0.05, "blue": 0.18}})
            ], space_above=10, space_below=2)
        elif sec_type == "h4":
            builder.insert_rich_line([(sec_data, {"bold": True})], space_above=6, space_below=2)
        elif sec_type == "bold_header":
            builder.insert_rich_line([(sec_data, {"bold": True})], space_above=6, space_below=2)
        elif sec_type == "content":
            for sl in sec_data:
                sl_stripped = sl.strip()
                if not sl_stripped or sl_stripped.startswith("---") or sl_stripped.startswith("```"):
                    continue
                # Blockquote
                if sl_stripped.startswith(">"):
                    builder.insert_italic_line(sl_stripped.lstrip("> ").strip(), indent=18)
                    continue
                # Checklist
                chk = re.match(r'^(\s*)- \[([ x]?)\]\s+(.*)', sl)
                if chk:
                    builder.insert_list_item(chk.group(3), indent=len(chk.group(1)) // 2,
                                              checked=chk.group(2) == "x")
                    continue
                # Bullet
                bul = re.match(r'^(\s*)[*-]\s+(.*)', sl)
                if bul:
                    builder.insert_list_item(bul.group(2), indent=len(bul.group(1)) // 2)
                    continue
                # Numbered
                num = re.match(r'^(\s*)\d+\.\s+(.*)', sl)
                if num:
                    builder.insert_paragraph(f"  {num.group(2)}", indent=(len(num.group(1)) // 2) * 18,
                                              space_above=1, space_below=1)
                    continue
                # Inline bold
                parts = re.split(r'(\*\*.*?\*\*)', sl_stripped)
                if len(parts) > 1:
                    runs = [(p[2:-2], {"bold": True}) if p.startswith("**") else (p, {}) for p in parts]
                    builder.insert_rich_line(runs, space_above=1, space_below=1)
                else:
                    builder.insert_paragraph(sl_stripped, space_above=1, space_below=1)
    
    builder.insert_divider()

builder.flush()

# ═══════════════════ MILESTONES TABLE ═══════════════════
builder.insert_heading("Milestones & Deadlines", 2)
builder.insert_table(
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

# ═══════════════════ RISK REGISTRY ═══════════════════
builder.insert_divider()
builder.insert_heading("Risk Registry", 2)
builder.insert_table(
    ["Risk", "Likelihood", "Impact", "Mitigation"],
    [
        ["Insufficient Abnormal data (0-3 natural faults)", "High", "High", "Unsupervised mitigates — fault injection provides guaranteed Abnormal samples"],
        ["Fault injection permission denied", "Medium", "High", "Engage PPO early; fallback to log validation + spot-checks"],
        ["Calibration equipment unavailable", "Low", "High", "Confirmed available — verify access Phase 1"],
        ["DIY airflow sensor not ready (PMV)", "High", "Low", "Conditional — H4 and RQ3 drop silently"],
        ["30-40 units overwhelm 2-kit rotation", "Medium", "Medium", "Start with 20 units, expand gradually"],
        ["Scope too large for 3 members", "Medium", "High", "Cut non-critical tasks; conditional experiments are optional"],
        ["Adviser requires major revision", "Medium", "Medium", "Incremental drafts per phase, not bulk submission"],
        ["Score confounded by ambient conditions", "Medium", "Medium", "Layer 4 validation: include confounds as control variables"],
        ["CNN spectrogram fails", "Medium", "Medium", "Fallback: vibration statistical features (RMS, kurtosis, etc.)"],
    ]
)

# ═══════════════════ ASSIGNMENT ═══════════════════
builder.insert_divider()
builder.insert_heading("Assignment Legend", 2)
builder.insert_table(
    ["Abbreviation", "Name"],
    [
        ["JRP", "John Ronald Pacaldo"],
        ["CBA", "Collin Brandon Asio"],
        ["SFS", "Simon France Sulibio"],
    ]
)

# ═══════════════════ APPENDIX ═══════════════════
builder.insert_divider()
builder.insert_heading("Appendix: Supervised vs. Unsupervised Decision Summary", 2)
builder.insert_paragraph("Three LLMs independently reviewed the methodology choice. Verdict: 3-0 for Unsupervised Anomaly Detection.")

builder.insert_bold_line("Why Unsupervised Won")
builder.insert_table(
    ["Reason", "Detail"],
    [
        ["Math is fatal for supervised", "13 known-problem / 2,599 campus-wide. ~0-3 Abnormal in 30-40 sample. Can't validate."],
        ["Labels aren't ground truth", "Technician inspection is subjective — can't see the evaporator non-invasively."],
        ["Matches the thesis claim", "'Flag unusual behavior → prioritize inspection' = anomaly detection."],
        ["Handles novel failures", "Unsupervised detects any deviation; supervised only known failure modes."],
    ]
)

builder.insert_bold_line("Supervised as Conditional Secondary")
builder.insert_paragraph("If controlled fault injection yields ≥ 30 labeled Abnormal samples, run RF/XGBoost/RBF SVM as a comparison experiment. Bonus, not dependency.")

builder.insert_bold_line("Validation Strategy (5-Layer)")
builder.insert_table(
    ["Layer", "Method", "Target"],
    [
        ["Layer 1", "Retrospective log: score separation known-fault vs healthy", "Mann-Whitney U p<0.05"],
        ["Layer 2", "Controlled fault injection: verify score rises post-fault", "TPR ≥ 80%"],
        ["Layer 3", "Monthly technician spot-checks vs anomaly scores", "Agreement ≥ 70%"],
        ["Layer 4", "Confound verification: score vs weather, cleaning, kit", "p > 0.05 per confound"],
        ["Layer 5", "Maintenance reset: score drops after cleaning", "Wilcoxon p < 0.05"],
    ]
)

# ── Finalize ──
builder.close()
print(f"\n✅ Done: https://docs.google.com/document/d/{DOC_ID}/edit")
