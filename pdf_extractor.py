"""
PDF highlight extraction — reused unchanged from the main backend.
"""

import warnings
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader
import pdfplumber

from text_cleaner import clean_text

warnings.filterwarnings("ignore")


@dataclass
class Highlight:
    page: int
    text: str


def _get_annotation_quads(reader: PdfReader) -> list[dict]:
    annotations = []
    for page_num, page in enumerate(reader.pages):
        if "/Annots" not in page:
            continue
        for annot in page["/Annots"]:
            obj = annot.get_object()
            if obj.get("/Subtype") != "/Highlight":
                continue
            quads = obj.get("/QuadPoints")
            if quads:
                annotations.append({"page": page_num, "quads": list(quads)})
    annotations.sort(key=lambda a: (a["page"], -a["quads"][1]))
    return annotations


def _quads_to_bboxes(quads: list[float]) -> list[tuple]:
    bboxes = []
    for i in range(0, len(quads), 8):
        q = quads[i : i + 8]
        xs = [q[j] for j in range(0, 8, 2)]
        ys = [q[j] for j in range(1, 8, 2)]
        bboxes.append((min(xs), min(ys), max(xs), max(ys)))
    return bboxes


def extract_highlights(pdf_path: Path) -> list[Highlight]:
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        raise ValueError(f"Could not read PDF: {exc}") from exc

    annotation_data = _get_annotation_quads(reader)
    if not annotation_data:
        return []

    results = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for annotation in annotation_data:
            page_index = annotation["page"]
            page = pdf.pages[page_index]
            ph = page.height
            word_parts = []
            for x0, y0p, x1, y1p in _quads_to_bboxes(annotation["quads"]):
                top = ph - y1p
                bottom = ph - y0p
                crop = page.within_bbox((x0 - 2, top - 2, x1 + 2, bottom + 2), strict=False)
                word_parts.extend(w["text"] for w in crop.extract_words())
            text = clean_text(" ".join(word_parts))
            if text:
                results.append(Highlight(page=page_index + 1, text=text))

    return results
