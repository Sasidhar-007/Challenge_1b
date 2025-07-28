# Adobe Challenge Round 1B – Multi-Collection PDF Analysis

This solution performs **persona-based PDF content extraction** for multiple collections. The system reads an input JSON configuration, analyzes PDFs for relevant information, ranks important sections, and outputs a structured JSON response.

---

## 🧠 Core Methodology

1. **Keyword Matching by Persona & Task**
   - Combines `persona.role` and `job_to_be_done.task` as query context.
   - All sections in the PDF are scored based on keyword overlap.

2. **Section Splitting & Heuristics**
   - Each page is scanned for **ALL CAPS** or **heading-like** lines to define sections.
   - Uses simple regex to detect structured section titles.

3. **Page-by-Page Text Extraction**
   - Extracts raw text from each PDF page using `PyPDF2`.
   - Associates each section with its originating page.

4. **Importance Ranking**
   - Sections are scored using `Counter`-based frequency analysis.
   - Top 3 sections per document are ranked and returned.

5. **Structured JSON Output**
   - Outputs include:
     - Metadata: persona, task, documents
     - Extracted sections with ranking and page numbers
     - Subsection analysis: short refined excerpts from top sections

---

## 🔧 Libraries Used

- **PyPDF2** – PDF reading and text extraction
- **re / regex** – Title/section detection and text splitting
- **collections.Counter** – Section scoring

---

## ⚙️ Performance

- **Avg. Processing Time:** ~5–10 seconds per document
- **No GPU/ML Required** – Lightweight and interpretable
- **Single-Core Friendly:** Efficient for small- to medium-scale batch jobs

---

## 🧱 Folder Structure

```bash
Challenge_1b/
├── Collection 1/
│   ├── challenge1b_input.json
│   └── PDFs/
├── Collection 2/
│   ├── challenge1b_input.json
│   └── PDFs/
├── Collection 3/
│   ├── challenge1b_input.json
│   └── PDFs/
├── main.py
├── requirements.txt
└── README.md
```
---

## 🚀 Run Instructions
Install dependencies:

```bash
pip install -r requirements.txt
```
Run for one collection:

```bash
python3 main.py \
  --input "Collection 1/challenge1b_input.json" \
  --pdfs "Collection 1/PDFs/" \
  --output "Collection 1/challenge1b_output.json"

```
Run all collections:
```bash
for C in "Collection 1" "Collection 2" "Collection 3"; do
  python3 main.py \
    --input "$C/challenge1b_input.json" \
    --pdfs "$C/PDFs/" \
    --output "$C/challenge1b_output.json"
done

```
