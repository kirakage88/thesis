"""
SIMPLEST POSSIBLE approach: create doc, dump all markdown, style headings + code blocks.
No line-by-line parsing, no mixed formatting runs, no table gymnastics.
"""
import json, re, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

MD_PATH = "D:/School/1 Projects/thesis/thesis_roadmap.md"
token_path = Path.home() / "AppData/Local/hermes/google_token.json"
creds = Credentials.from_authorized_user_info(json.loads(token_path.read_text()))
docs = build("docs", "v1", credentials=creds)

# 1) Create empty doc
doc = docs.documents().create(body={"title": "Thesis Roadmap — Predictive Maintenance for Coiled Evaporators"}).execute()
DOC_ID = doc["documentId"]
print(f"Doc: {DOC_ID}")

# 2) Read raw markdown text
raw = Path(MD_PATH).read_text(encoding="utf-8")
# Keep everything — the markdown is the content we want

# 3) Insert ALL text in one batch
text_to_insert = raw + "\n\n"
docs.documents().batchUpdate(documentId=DOC_ID, body={
    "requests": [{"insertText": {"location": {"index": 1}, "text": text_to_insert}}]
}).execute()
doc_len = len(text_to_insert) + 1  # doc starts at index 1, so text ends at 1 + len(text)
print(f"Inserted {len(text_to_insert)} chars")

time.sleep(1)

# 4) Find heading positions and apply styles
# We need to get the doc content to find line boundaries
doc_info = docs.documents().get(documentId=DOC_ID).execute()
body_text = doc_info.get("body", {}).get("content", [])
print(f"Doc has {len(body_text)} structural elements")

# Build index map: for each structural element, get its start/end
# We need to identify which elements correspond to heading lines in the markdown
# The markdown headings are: # H1, ## H2, ### H3, #### H4

# Strategy: find all heading lines in the raw text, compute their positions
# relative to the inserted text, then apply paragraph style at those positions

heading_styles = {
    1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3", 4: "HEADING_4"
}

# Find all heading lines and their character positions in the raw text
heading_positions = []  # [(start_pos, end_pos, level), ...]

for m in re.finditer(r'^(#{1,4})\s+(.+)$', raw, re.MULTILINE):
    level = len(m.group(1))
    start = m.start()
    end = m.end()
    heading_positions.append((start, end, level))

print(f"Found {len(heading_positions)} heading lines")

# Apply heading styles in batches of 50
for i in range(0, len(heading_positions), 50):
    batch = []
    for start, end, level in heading_positions[i:i+50]:
        # Positions in the doc are 1-indexed: doc starts at 1, so we add 1
        # The heading text starts after the # and space characters
        # m.start() gives start of line including ###, we want the paragraph from line start to end
        doc_start = start + 1  # +1 because doc index 1 is the first char of inserted text
        doc_end = end + 1      # +1 for same reason
        
        batch.append({
            "updateParagraphStyle": {
                "range": {"startIndex": doc_start, "endIndex": doc_end},
                "paragraphStyle": {
                    "namedStyleType": heading_styles[level],
                    "spaceAbove": {"magnitude": 12, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"}
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }
        })
    
    if batch:
        docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": batch}).execute()
        time.sleep(1)
    print(f"  Styled {i + len(batch)}/{len(heading_positions)} headings")

# 5) Apply code block formatting (Consolas + gray background for ``` blocks)
code_blocks = []
in_code = False
code_start = 0
for m in re.finditer(r'```', raw):
    if not in_code:
        code_start = m.start()
        in_code = True
    else:
        code_end = m.end()
        code_blocks.append((code_start, code_end))
        in_code = False

print(f"Found {len(code_blocks)} code blocks")

for i, (cs, ce) in enumerate(code_blocks):
    # Apply monospace + gray background to the entire code block content (including backticks)
    doc_start = cs + 1
    doc_end = ce + 1
    
    try:
        docs.documents().batchUpdate(documentId=DOC_ID, body={
            "requests": [{
                "updateTextStyle": {
                    "range": {"startIndex": doc_start, "endIndex": doc_end},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": "Consolas", "weight": 400},
                        "fontSize": {"magnitude": 9, "unit": "PT"},
                        "backgroundColor": {"color": {"rgbColor": {"red": 0.92, "green": 0.92, "blue": 0.92}}}
                    },
                    "fields": "weightedFontFamily.fontFamily,fontSize,backgroundColor"
                }
            }]
        }).execute()
        
        # Add left indent to code blocks
        docs.documents().batchUpdate(documentId=DOC_ID, body={
            "requests": [{
                "updateParagraphStyle": {
                    "range": {"startIndex": doc_start, "endIndex": doc_end},
                    "paragraphStyle": {
                        "indentStart": {"magnitude": 18, "unit": "PT"},
                        "lineSpacing": 1.0
                    },
                    "fields": "indentStart,lineSpacing"
                }
            }]
        }).execute()
        
        if (i + 1) % 10 == 0:
            time.sleep(1)
    except Exception as e:
        print(f"  Code block {i+1} error: {e}")

# 6) Apply default font to entire document
docs.documents().batchUpdate(documentId=DOC_ID, body={
    "requests": [{
        "updateDocumentStyle": {
            "documentStyle": {
                "marginTop": {"magnitude": 36, "unit": "PT"},
                "marginBottom": {"magnitude": 36, "unit": "PT"},
                "marginLeft": {"magnitude": 54, "unit": "PT"},
                "marginRight": {"magnitude": 54, "unit": "PT"}
            },
            "fields": "marginTop,marginBottom,marginLeft,marginRight"
        }
    }]
}).execute()

# 7) Set default paragraph style for body text
docs.documents().batchUpdate(documentId=DOC_ID, body={
    "requests": [{
        "updateParagraphStyle": {
            "range": {"startIndex": 1, "endIndex": 2},
            "paragraphStyle": {
                "namedStyleType": "NORMAL_TEXT",
                "lineSpacing": 1.15
            },
            "fields": "namedStyleType,lineSpacing"
        }
    }]
}).execute()

print(f"\n✅ Done: https://docs.google.com/document/d/{DOC_ID}/edit")
print(f"   {len(heading_positions)} headings styled")
print(f"   {len(code_blocks)} code blocks styled")
