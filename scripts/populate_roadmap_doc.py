"""
Populate thesis roadmap Google Doc from markdown source.
Reads the markdown, inserts into the doc, applies formatting.
"""
import json, re, sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

DOC_ID = "1B0u8l3oAuCxmB2Mr4jbT7q_U97UzL8cQ0Nh3FMKmIAs"
MD_PATH = "D:/School/1 Projects/thesis/thesis_roadmap.md"

# ── Auth ──
token_path = Path.home() / "AppData/Local/hermes/google_token.json"
token_data = json.loads(token_path.read_text())
creds = Credentials.from_authorized_user_info(token_data)
service = build("docs", "v1", credentials=creds)

# ── Read markdown ──
raw_text = Path(MD_PATH).read_text(encoding="utf-8")
lines = raw_text.split("\n")

# ── Build the document content ──
# We strip markdown artifacts (** for bold will be re-applied via API)
# We also strip pipe-table formatting artifacts and replace with readable text

doc_lines = []
in_appendix = False
for line in lines:
    # Skip ALL original appendix content — replace with cleaner summary below
    if line.strip().startswith("## Appendix:"):
        in_appendix = True
        continue
    if in_appendix:
        continue
    
    # Skip table formatting lines (|---|---| etc)
    if re.match(r'^\|[-| :]+\|$', line.strip()):
        continue
    
    # Convert markdown tables to readable text
    if line.strip().startswith('|') and line.strip().endswith('|'):
        cells = [c.strip() for c in line.strip().split('|')]
        cells = [c for c in cells if c]  # Remove empty from leading/trailing |
        if len(cells) >= 2:
            doc_lines.append("  " + "  |  ".join(cells))
        continue
    
    doc_lines.append(line)

# After the loop, add the clean appendix summary
doc_lines.append("")
doc_lines.append("---")
doc_lines.append("## Appendix: Methodology Decision Summary")
doc_lines.append("")
doc_lines.append("Three LLMs independently reviewed the methodology choice. Verdict: 3-0 for Unsupervised Anomaly Detection. See the 'GLM Claim' document in suggestions/ for the full analysis.")
doc_lines.append("")
doc_lines.append("Why unsupervised anomaly detection was chosen over supervised classification:")
doc_lines.append("")
doc_lines.append("1. 13 known-problem units out of 2,599 campus-wide — 0-3 Abnormal observations expected in the study sample. Supervised classification with 0-3 positive examples is statistically unvalidatable.")
doc_lines.append("2. Labels from non-invasive technician inspection are a subjective proxy. A model trained on proxy labels learns to reproduce noise, not ground-truth faults.")
doc_lines.append("3. The thesis claim — 'flag unusual behavior, prioritize inspection' — is anomaly detection, not binary classification. The framing matches the method.")
doc_lines.append("4. Unsupervised detection finds ANY deviation from normal. Supervised classification can only detect failure modes present in the training data.")
doc_lines.append("")
doc_lines.append("Supervised classification (RF, XGBoost, RBF SVM) will be run as a CONDITIONAL SECONDARY experiment — only if controlled fault injection produces ≥30 labeled Abnormal samples. This is a bonus, not a dependency.")
doc_lines.append("")
doc_lines.append("Validation strategy (5-layer):")
doc_lines.append("  Layer 1 — Retrospective log comparison: anomaly score separation between known-fault and known-healthy units (Mann-Whitney U, p < 0.05)")
doc_lines.append("  Layer 2 — Controlled fault injection: inject known faults, verify anomaly score rises (TPR ≥ 80%)")
doc_lines.append("  Layer 3 — Monthly technician spot-checks: correlate findings with anomaly scores (agreement ≥ 70%)")
doc_lines.append("  Layer 4 — Confound verification: prove anomaly score isn't driven by weather, cleaning recency, or kit variation")
doc_lines.append("  Layer 5 — Maintenance reset: cleaned units show anomaly score drop → real signal, not noise")

doc_text = "\n".join(doc_lines)

# ── Insert text at position 1 ──
service.documents().batchUpdate(documentId=DOC_ID, body={
    "requests": [{
        "insertText": {
            "location": {"index": 1},
            "text": doc_text
        }
    }]
}).execute()

# ── Calculate line start indices ──
# After insertion, the doc starts at index 1
line_starts = [1]
for line in doc_lines[:-1]:
    line_starts.append(line_starts[-1] + len(line) + 1)  # +1 for newline

# ── Build formatting requests ──
reqs = []

def find_line_nums(pattern, text=doc_lines):
    """Find line indices matching a regex pattern."""
    return [i for i, l in enumerate(text) if re.match(pattern, l)]

def find_text_range(search_text, doc_line, offset_within_line=0):
    """Get the (start, end) indices for text within a line."""
    idx = doc_line.find(search_text)
    if idx == -1:
        return None
    s = line_starts[line_idx] + idx + offset_within_line
    e = s + len(search_text)
    return (s, e)

# 1. HEADINGS
heading_lines = []
for i, l in enumerate(doc_lines):
    m = re.match(r'^(#{1,6})\s+(.+)$', l)
    if m:
        level = min(len(m.group(1)), 3)  # Docs API supports H1-H3 easily
        style_map = {1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3"}
        s, e = line_starts[i], line_starts[i] + len(l)
        reqs.append({
            "updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {
                    "namedStyleType": style_map[level],
                    "spaceAbove": {"magnitude": 14 if level == 1 else 10, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6 if level == 1 else 4, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow",
            }
        })
        heading_lines.append(i)

# 2. BOLD (**text**) — handle inline bold
for m in re.finditer(r'\*\*(.+?)\*\*', doc_text):
    # Find which line this match falls in
    cumul = 0
    found = False
    for li, l in enumerate(doc_lines):
        next_cumul = cumul + len(l) + 1
        if cumul <= m.start() < next_cumul:
            doc_start = line_starts[li] + (m.start() - cumul) + 2  # skip opening **
            doc_end = doc_start + len(m.group(1))
            reqs.append({
                "updateTextStyle": {
                    "range": {"startIndex": doc_start, "endIndex": doc_end},
                    "textStyle": {"bold": True},
                    "fields": "bold",
                }
            })
            found = True
            break
        cumul = next_cumul
    if not found:
        # Fallback: scan directly in doc_text
        pass

# 3. BULLET LISTS — lines starting with - [ ] or - or *
bullet_types = [
    (r'^-\s+\[.\]\s+', "checkbox"),  # - [ ] / - [x]
    (r'^-\s+', "bullet"),             # - text
]
for i, l in enumerate(doc_lines):
    stripped = l.lstrip()
    if re.match(r'^- \[[ x]\] ', stripped):
        # Checkbox line — still render as bullet
        s, e = line_starts[i], line_starts[i] + len(l)
        reqs.append({
            "createParagraphBullets": {
                "range": {"startIndex": s, "endIndex": e},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        })
    elif re.match(r'^-\s+', stripped):
        s, e = line_starts[i], line_starts[i] + len(l)
        reqs.append({
            "createParagraphBullets": {
                "range": {"startIndex": s, "endIndex": e},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        })

# 4. NUMBERED LISTS
for i, l in enumerate(doc_lines):
    if re.match(r'^\s*\d+\.\s+', l):
        s, e = line_starts[i], line_starts[i] + len(l)
        reqs.append({
            "createParagraphBullets": {
                "range": {"startIndex": s, "endIndex": e},
                "bulletPreset": "NUMBERED_DECIMAL_ALPHA_ROMAN",
            }
        })

# 5. BLOCKQUOTES (> prefix → italic)
for i, l in enumerate(doc_lines):
    if l.strip().startswith(">"):
        s, e = line_starts[i], line_starts[i] + len(l)
        reqs.append({
            "updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "textStyle": {"italic": True},
                "fields": "italic",
            }
        })

# 6. HORIZONTAL RULES (---)
for i, l in enumerate(doc_lines):
    if re.match(r'^-{3,}$', l.strip()):
        s, e = line_starts[i], line_starts[i] + len(l)
        reqs.append({
            "updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {
                    "spaceAbove": {"magnitude": 8, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                },
                "fields": "spaceAbove,spaceBelow",
            }
        })

# 7. TABLE HEADER ROWS — bold the first row after a table separator line
# Find consecutive non-empty table lines (lines with "  |  " separator)
table_line_groups = []
current_group = []
for i, l in enumerate(doc_lines):
    if "  |  " in l:
        current_group.append(i)
    else:
        if len(current_group) >= 2:  # at least header + separator-like
            # First row is the header — bold it
            hdr_idx = current_group[0]
            s, e = line_starts[hdr_idx], line_starts[hdr_idx] + len(doc_lines[hdr_idx])
            reqs.append({
                "updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": e},
                    "textStyle": {"bold": True},
                    "fields": "bold",
                }
            })
        current_group = []

# Handle last group
if len(current_group) >= 2:
    hdr_idx = current_group[0]
    s, e = line_starts[hdr_idx], line_starts[hdr_idx] + len(doc_lines[hdr_idx])
    reqs.append({
        "updateTextStyle": {
            "range": {"startIndex": s, "endIndex": e},
            "textStyle": {"bold": True},
            "fields": "bold",
        }
    })

# ── Chunk and execute ──
print(f"Total formatting requests: {len(reqs)}")

# Insert text was already done above
# Now apply formatting in batches of 100
for i in range(0, len(reqs), 100):
    batch = reqs[i:i+100]
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": batch})
    print(f"  Applied batch {i//100 + 1}/{(len(reqs)-1)//100 + 1} ({len(batch)} requests)")

print("Done!")
print(f"Google Doc URL: https://docs.google.com/document/d/{DOC_ID}/edit")
