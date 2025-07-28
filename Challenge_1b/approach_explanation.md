
# Adobe Challenge Round 1B – Approach Explanation

This document explains the full approach to solve the **Multi-Collection PDF Analysis** task from Round 1B of Adobe's Hackathon.

---

## 🎯 Objective

To extract **important sections and refined content** from PDFs based on:
- A specific **persona**
- A **task/job-to-be-done** description

The output must include:
- Ranked important sections
- Cleaned-up content snippets
- Structured JSON format

---

## 🧠 Approach Breakdown

### 1. Input Parsing

The script reads `challenge1b_input.json` for:
- Persona details
- Task description
- List of PDF documents to analyze

### 2. PDF Text Extraction

Each document is processed using `PyPDF2`:
- Reads text from all pages
- Page text is stored for section detection

### 3. Section Splitting

Each page’s text is split using regex:
- Detects **ALL CAPS lines** and numbered headings (e.g., `1.`, `2.1`)
- Creates a logical set of document "sections"

### 4. Section Scoring

Each section is scored by:
- Tokenizing the text
- Counting overlap with persona + task keywords
- Using a simple `Counter()` to rank importance

### 5. Output Formatting

The output is a JSON file containing:
- `metadata`: Documents, persona, task
- `extracted_sections`: Top 3 ranked sections
- `subsection_analysis`: Snippets for each top section

---

## ✅ Why This Approach Works

- **No heavy NLP or training required** — lightweight, interpretable
- **Persona-Task targeting** ensures relevance
- **Easy to extend** — can plug in embeddings or semantic matching later

---

## ⚙️ Tools & Dependencies

- **Python 3**
- **PyPDF2** – for text extraction
- **Standard Library** – regex, JSON, argparse, Counter

---

## 🛠️ Future Improvements

- Use **semantic similarity** (e.g., BERT) instead of keyword match
- Apply **better section detection** using layout (via `pdfminer` or `pdfplumber`)
- Add **optional HTML or Markdown output** for visualization

---

## 🧪 Testing & Results

Tested on 3 sample collections:
- Travel Planning
- Acrobat Tutorials
- Cooking Recipes

Accuracy is based on correct detection of contextually relevant sections from noisy PDF input.

---
