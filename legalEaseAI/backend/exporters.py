import re
from io import BytesIO
from docx import Document

def sanitize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def filename_for(doc_type: str) -> str:
    safe = doc_type.replace(" ", "_").lower()
    return f"{safe}_draft"

def export_docx(title: str, content: str) -> BytesIO:
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(content)
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def export_pdf(title: str, content: str) -> BytesIO:
    buf = BytesIO()
    buf.write(content.encode('utf-8'))
    buf.seek(0)
    return buf

def format_docx(content: str) -> BytesIO:
    return export_docx("Legal Document", content)

def format_pdf(content: str) -> BytesIO:
    return export_pdf("Legal Document", content)

to_docx = export_docx
to_pdf = export_pdf