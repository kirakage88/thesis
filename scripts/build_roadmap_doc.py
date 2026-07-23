"""
Build Google Doc from thesis_roadmap.md — direct markdown → Docs translation.
Reads the markdown, creates a Google Doc, and inserts formatted content.
"""
import json, re, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

MD_PATH = "D:/School/1 Projects/thesis/thesis_roadmap.md"

# ── Auth ──
token_path = Path.home() / "AppData/Local/hermes/google_token.json"
token_data = json.loads(token_path.read_text())
creds = Credentials.from_authorized_user_info(token_data)
docs = build("docs", "v1", credentials=creds)

# ── Create doc ──
doc = docs.documents().create(body={"title": "Thesis Roadmap — Predictive Maintenance for Coiled Evaporators"}).execute()
DOC_ID = doc["documentId"]
print(f"Created doc: https://docs.google.com/document/d/{DOC_ID}/edit")

# ── Read markdown ──
raw = Path(MD_PATH).read_text(encoding="utf-8")
lines = raw.split("\n")

# ── Build content blocks ──
# Each block is (text, style_dict) where style_dict has optional keys:
#   heading_level: 1-4
#   bold: bool
#   italic: bool
#   code: bool
#   strikethrough: bool
#   bullet: True  (will be indented by nesting level)
#   numbered: True
#   indent: int  (nesting level for lists)

blocks = []
in_code_block = False
code_buf = []
in_table = False
table_buf = []
in_blockquote = False

def flush_code():
    global code_buf
    if code_buf:
        text = "\n".join(code_buf)
        blocks.append((text, {"code": True}))
        blocks.append(("", {}))  # blank line after code
        code_buf = []

def flush_table():
    global table_buf
    if len(table_buf) >= 2:
        # Render as aligned text
        for row in table_buf:
            # Skip separator rows
            if re.match(r'^[\s|:-]+$', row):
                continue
            cells = [c.strip() for c in row.split("|")]
            cells = [c for c in cells if c]
            if cells:
                # Bold the header row (first row)
                is_header = (table_buf.index(row) == 0)
                parts = []
                for c in cells:
                    if is_header:
                        parts.append(f"**{c}**")
                    else:
                        parts.append(c)
                blocks.append(("  " + "  |  ".join(parts), {"bold": is_header}))
        blocks.append(("", {}))
    table_buf = []

def render_inline(text):
    """Parse inline formatting markers and return list of (txt, fmt) runs."""
    # Handle bold+italic ***...*** first
    runs = []
    # Simple approach: split on **
    parts = re.split(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    for p in parts:
        if not p:
            continue
        fmt = {}
        if p.startswith("***") and p.endswith("***"):
            fmt = {"bold": True, "italic": True}
            p = p[3:-3]
        elif p.startswith("**") and p.endswith("**"):
            fmt = {"bold": True}
            p = p[2:-2]
        elif p.startswith("*") and p.endswith("*"):
            fmt = {"italic": True}
            p = p[1:-1]
        elif p.startswith("`") and p.endswith("`"):
            fmt = {"code": True}
            p = p[1:-1]
        runs.append((p, fmt))
    return runs if runs else [(text, {})]

for line in lines:
    # Handle code blocks
    if line.strip().startswith("```"):
        if in_code_block:
            flush_code()
            in_code_block = False
        else:
            flush_table()  # tables can't span code
            in_code_block = True
        continue

    if in_code_block:
        code_buf.append(line.rstrip())
        continue

    # Handle tables
    if line.strip().startswith("|") and line.strip().endswith("|"):
        if not in_table:
            flush_table()
            in_table = True
        table_buf.append(line.strip())
        continue
    else:
        if in_table:
            flush_table()
            in_table = False

    # Horizontal rule
    if re.match(r'^-{3,}$', line.strip()):
        blocks.append(("────────────────────────────────", {}))
        blocks.append(("", {}))
        continue

    # Blockquotes
    if line.strip().startswith(">"):
        text = re.sub(r'^>\s?', "", line).strip()
        if text:
            blocks.append((text, {"italic": True}))
        continue

    # Headings
    heading_match = re.match(r'^(#{1,4})\s+(.+)$', line)
    if heading_match:
        level = len(heading_match.group(1))
        text = heading_match.group(2)
        blocks.append((text, {"heading_level": level}))
        continue

    # Empty lines
    if not line.strip():
        continue

    # List items (with checkbox)
    list_match = re.match(r'^(\s*)- \[([ x]?)\]\s+(.*)', line)
    if list_match:
        indent = len(list_match.group(1)) // 2
        checked = list_match.group(2) == "x"
        text = list_match.group(3)
        prefix = "☐ " if not checked else "☑ "
        blocks.append((prefix + text, {"indent": indent}))
        continue

    # List items (bullet)
    list_match = re.match(r'^(\s*)[*-]\s+(.*)', line)
    if list_match:
        indent = len(list_match.group(1)) // 2
        text = list_match.group(2)
        blocks.append(("• " + text, {"indent": indent}))
        continue

    # Numbered list
    num_match = re.match(r'^(\s*)\d+\.\s+(.*)', line)
    if num_match:
        indent = len(num_match.group(1)) // 2
        text = num_match.group(2)
        blocks.append((f"{text}", {"indent": indent, "numbered": True}))
        continue

    # Normal paragraph
    if line.strip():
        blocks.append((line.strip(), {}))
        continue

# Flush any remaining table
flush_table()

# ── Insert text into doc ──
# We'll insert all blocks as a single text blob with newlines
doc_text_parts = []
for text, fmt in blocks:
    doc_text_parts.append(text)
full_text = "\n".join(doc_text_parts)

# Insert at position 1
docs.documents().batchUpdate(documentId=DOC_ID, body={
    "requests": [{
        "insertText": {
            "location": {"index": 1},
            "text": full_text
        }
    }]
}).execute()

# ── Now apply formatting ──
# We need to track character positions of each block
cursor = 1  # Google Docs index (1-based after first insert)
line_starts = []
for text, fmt in blocks:
    line_starts.append(cursor)
    cursor += len(text) + 1  # +1 for newline
# Total length
total_len = cursor

reqs = []

def make_range(start, end):
    """Create a Google Docs range object."""
    return {"startIndex": start, "endIndex": end}

def get_text_range(block_idx):
    """Return (start, end) character indices for block."""
    start = line_starts[block_idx]
    text, _ = blocks[block_idx]
    end = start + len(text)
    return start, end

# First pass: apply structural formatting (headings, lists)
for i, (text, fmt) in enumerate(blocks):
    start, end = get_text_range(i)
    if not text:
        continue
    
    # Heading style
    if "heading_level" in fmt:
        level = fmt["heading_level"]
        style_map = {1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3", 4: "HEADING_4"}
        reqs.append({
            "updateParagraphStyle": {
                "range": make_range(start, end),
                "paragraphStyle": {
                    "namedStyleType": style_map[level],
                    "spaceAbove": {"magnitude": 12 if level <= 2 else 6, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }
        })
        continue
    
    # Code block
    if fmt.get("code"):
        reqs.append({
            "updateParagraphStyle": {
                "range": make_range(start, end),
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 4, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }
        })
        reqs.append({
            "updateTextStyle": {
                "range": make_range(start, end),
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Consolas", "weight": 400},
                    "fontSize": {"magnitude": 9, "unit": "PT"},
                    "backgroundColor": {"color": {"rgbColor": {"red": 0.95, "green": 0.95, "blue": 0.95}}}
                },
                "fields": "weightedFontFamily.fontFamily,fontSize,backgroundColor"
            }
        })
        continue
    
    # List items — set indentation
    if "indent" in fmt:
        level = fmt["indent"]
        indent_pts = 18 * level
        reqs.append({
            "updateParagraphStyle": {
                "range": make_range(start, end),
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "indentStart": {"magnitude": indent_pts, "unit": "PT"},
                    "spaceAbove": {"magnitude": 2, "unit": "PT"},
                    "spaceBelow": {"magnitude": 1, "unit": "PT"},
                    "lineSpacing": 1.15
                },
                "fields": "namedStyleType,indentStart,spaceAbove,spaceBelow,lineSpacing"
            }
        })
        continue
    
    # Blockquote (italic)
    if fmt.get("italic"):
        reqs.append({
            "updateParagraphStyle": {
                "range": make_range(start, end),
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "indentStart": {"magnitude": 18, "unit": "PT"},
                    "indentEnd": {"magnitude": 18, "unit": "PT"},
                    "spaceAbove": {"magnitude": 4, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,indentStart,indentEnd,spaceAbove,spaceBelow"
            }
        })
        reqs.append({
            "updateTextStyle": {
                "range": make_range(start, end),
                "textStyle": {"italic": True},
                "fields": "italic"
            }
        })
        continue
    
    # Normal paragraph
    reqs.append({
        "updateParagraphStyle": {
            "range": make_range(start, end),
            "paragraphStyle": {
                "namedStyleType": "NORMAL_TEXT",
                "lineSpacing": 1.15,
                "spaceAbove": {"magnitude": 2, "unit": "PT"},
                "spaceBelow": {"magnitude": 2, "unit": "PT"},
            },
            "fields": "namedStyleType,lineSpacing,spaceAbove,spaceBelow"
        }
    })

# Second pass: inline formatting — bold/italic/code within paragraphs
for i, (text, fmt) in enumerate(blocks):
    start, end = get_text_range(i)
    if not text or fmt.get("heading_level") or fmt.get("code"):
        continue
    
    # Find all inline bold/italic/code spans in the text
    for m in re.finditer(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|`[^`]+`)', text):
        span_start = start + m.start()
        span_end = start + m.end()
        inner = m.group(0)
        
        style = {}
        if inner.startswith("***") and inner.endswith("***"):
            style["bold"] = True
            style["italic"] = True
            # Reduce indices to exclude markers
            span_start += 3
            span_end -= 3
        elif inner.startswith("**") and inner.endswith("**"):
            style["bold"] = True
            span_start += 2
            span_end -= 2
        elif inner.startswith("`") and inner.endswith("`"):
            style["weightedFontFamily"] = {"fontFamily": "Consolas", "weight": 400}
            style["fontSize"] = {"magnitude": 9, "unit": "PT"}
            style["backgroundColor"] = {"color": {"rgbColor": {"red": 0.92, "green": 0.92, "blue": 0.92}}}
            span_start += 1
            span_end -= 1
        
        if style and span_end > span_start:
            # Fix field paths for nested objects
            fields_str = ",".join(style.keys())
            fields_str = fields_str.replace("weightedFontFamily", "weightedFontFamily.fontFamily")
            # backgroundColor is a proper field name, fontSize too - no change needed
            reqs.append({
                "updateTextStyle": {
                    "range": make_range(span_start, span_end),
                    "textStyle": style,
                    "fields": fields_str
                }
            })

# Apply all style in batched requests
BATCH_SIZE = 100
for i in range(0, len(reqs), BATCH_SIZE):
    batch = reqs[i:i + BATCH_SIZE]
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": batch}).execute()
    if (i + BATCH_SIZE) % 200 == 0:
        time.sleep(0.5)

print(f"Applied {len(reqs)} formatting requests in {len(reqs)//BATCH_SIZE + 1} batches")
print(f"Google Doc URL: https://docs.google.com/document/d/{DOC_ID}/edit")
