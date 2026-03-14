"""
PDF Highlight Extractor — Gradio app.
The entire application: UI, logic, and export in one file.

Deploy to Hugging Face Spaces, Render, or PythonAnywhere
by following the instructions in README.md.
"""

import json
import tempfile
from pathlib import Path

import gradio as gr

from pdf_extractor import extract_highlights, Highlight


# ── Formatters ────────────────────────────────────────────────

def to_txt(highlights: list[Highlight], stem: str) -> str:
    title = f"Highlights — {stem}"
    lines = [title, "=" * len(title), "", f"Total highlights: {len(highlights)}", "", "=" * 60, ""]
    for i, h in enumerate(highlights, 1):
        lines += [f"[{i}] Page {h.page}", h.text, ""]
    return "\n".join(lines)


def to_markdown(highlights: list[Highlight], stem: str) -> str:
    lines = [f"# Highlights — {stem}", "", f"**Total highlights:** {len(highlights)}", "", "---", ""]
    for i, h in enumerate(highlights, 1):
        lines += [f"## [{i}] Page {h.page}", "", h.text, ""]
    return "\n".join(lines)


def to_json(highlights: list[Highlight]) -> str:
    return json.dumps(
        [{"page": h.page, "text": h.text} for h in highlights],
        indent=2,
        ensure_ascii=False,
    )


# ── Main function ─────────────────────────────────────────────

def process_pdf(pdf_file, export_format: str):
    """
    Extract highlights from an uploaded PDF and return a preview + download file.
    """
    if pdf_file is None:
        return "Please upload a PDF file.", None

    path = Path(pdf_file.name)

    try:
        highlights = extract_highlights(path)
    except ValueError as e:
        return f"Error reading PDF: {e}", None

    if not highlights:
        return (
            "No highlights found in this PDF.\n\n"
            "Make sure the PDF contains annotation-based highlights "
            "(created with a PDF reader like Preview, Adobe, or Zotero) "
            "rather than just visually coloured text.",
            None,
        )

    stem = path.stem

    # Build preview (first 5 highlights)
    preview_lines = [f"Found {len(highlights)} highlight(s)\n"]
    for i, h in enumerate(highlights[:5], 1):
        preview_lines.append(f"[{i}] Page {h.page}\n{h.text}\n")
    if len(highlights) > 5:
        preview_lines.append(f"... and {len(highlights) - 5} more. Download the file to see all.")
    preview = "\n".join(preview_lines)

    # Build export file
    if export_format == "Plain Text":
        content = to_txt(highlights, stem)
        ext = "txt"
    elif export_format == "Markdown":
        content = to_markdown(highlights, stem)
        ext = "md"
    else:  # JSON
        content = to_json(highlights)
        ext = "json"

    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{ext}",
        mode="w",
        encoding="utf-8",
        prefix=f"{stem}_highlights_",
    )
    tmp.write(content)
    tmp.close()

    return preview, tmp.name


# ── Gradio UI ─────────────────────────────────────────────────

demo = gr.Interface(
    fn=process_pdf,
    inputs=[
        gr.File(
            label="Upload PDF",
            file_types=[".pdf"],
        ),
        gr.Radio(
            choices=["Plain Text", "Markdown", "JSON"],
            value="Plain Text",
            label="Export format",
        ),
    ],
    outputs=[
        gr.Textbox(
            label="Preview",
            lines=20,
            show_copy_button=True,
        ),
        gr.File(
            label="Download highlights",
        ),
    ],
    title="PDF Highlight Extractor",
    description=(
        "Extract all highlighted text from a PDF file. "
        "Upload your PDF, choose an export format, and download the results. "
        "PDFs are processed locally and not stored."
    ),
    examples=[],
    allow_flagging="never",
)

if __name__ == "__main__":
    demo.launch()
