from pydantic import BaseModel
from typing import Optional

class DocumentRequest(BaseModel):
    doc_type: str
    prompt: str
    details: Optional[str] = ""

class ExportRequest(BaseModel):
    title: str = "Legal Document"
    content: str
    doc_type: Optional[str] = "docx"