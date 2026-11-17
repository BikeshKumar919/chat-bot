
from pathlib import Path

import pymupdf
from docx import Document


def extract_pdf_text(file_path: Path) -> str:
    """
    Extract text from a PDF resume.
    """

    text = []

    with pymupdf.open(file_path) as pdf:

        for page in pdf:
            page_text = page.get_text("text")
            text.append(page_text)

    return "\n".join(text).strip()


def extract_docx_text(file_path: Path) -> str:
    """
    Extract text from a DOCX resume.
    """

    document = Document(file_path)

    text = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text.strip())

    # Extract tables (many resumes use tables)
    for table in document.tables:
        for row in table.rows:
            row_text = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if row_text:
                text.append(" | ".join(row_text))

    return "\n".join(text).strip()


def extract_resume_text(file_path: Path) -> str:
    """
    Identify file type and extract resume text.
    """

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")
