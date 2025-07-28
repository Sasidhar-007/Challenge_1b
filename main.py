#!/usr/bin/env python3
import json
import os
import re
from collections import Counter, defaultdict
from typing import List, Dict
import PyPDF2

# ——— Helpers —————————————————————————————————————————————

def load_input(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_output(path: str, data: Dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def extract_pages_text(pdf_path: str) -> List[str]:
    """Return list of page‐texts."""
    reader = PyPDF2.PdfReader(pdf_path)
    return [page.extract_text() or "" for page in reader.pages]

def split_into_sections(text: str) -> List[Dict]:
    """
    Naïve split: whenever we see an ALL‐CAP heading line,
    start a new section.
    """
    lines = text.splitlines()
    sections = []
    current = {"title": "Introduction", "text": []}
    heading_re = re.compile(r'^[A-Z][A-Z0-9 \-]{3,}$')
    for line in lines:
        if heading_re.match(line.strip()):
            # start new section
            sections.append(current)
            current = {"title": line.strip(), "text": []}
        else:
            current["text"].append(line)
    sections.append(current)
    # clean
    return [ {"section_title": s["title"],
              "text": "\n".join(s["text"]).strip() }
             for s in sections if s["text"] ]

def score_section(sec_text: str, keywords: List[str]) -> int:
    """Score by counting keyword occurrences."""
    cnt = Counter(re.findall(r'\w+', sec_text.lower()))
    return sum(cnt[w.lower()] for w in keywords)

# ——— Core Processing ——————————————————————————————————

def process_collection(input_json: str, pdf_dir: str, output_json: str):
    cfg = load_input(input_json)
    persona = cfg["persona"]["role"]
    task    = cfg["job_to_be_done"]["task"]
    docs    = cfg["documents"]
    keywords = (persona + " " + task).split()

    output = {
      "metadata": {
        "input_documents": [d["filename"] for d in docs],
        "persona": persona,
        "job_to_be_done": task
      },
      "extracted_sections": [],
      "subsection_analysis": []
    }

    for d in docs:
        pdf_path = os.path.join(pdf_dir, d["filename"])
        pages = extract_pages_text(pdf_path)
        all_secs = []
        for page_num, page in enumerate(pages, start=1):
            secs = split_into_sections(page)
            for s in secs:
                s["page_number"] = page_num
                s["score"] = score_section(s["text"], keywords)
                s["document"] = d["filename"]
                all_secs.append(s)

        # take top-3 by score
        top3 = sorted(all_secs, key=lambda x: x["score"], reverse=True)[:3]
        for rank, sec in enumerate(top3, start=1):
            output["extracted_sections"].append({
                "document": sec["document"],
                "section_title": sec["section_title"],
                "importance_rank": rank,
                "page_number": sec["page_number"]
            })
            # also add full text snippet
            output["subsection_analysis"].append({
                "document": sec["document"],
                "refined_text": sec["text"][:500] + "…",
                "page_number": sec["page_number"]
            })

    write_output(output_json, output)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(
        description="Run Challenge 1B PDF analysis"
    )
    p.add_argument("--input",  default="challenge1b_input.json")
    p.add_argument("--pdfs",   default="PDFs/")
    p.add_argument("--output", default="challenge1b_output.json")
    args = p.parse_args()

    process_collection(args.input, args.pdfs, args.output)
