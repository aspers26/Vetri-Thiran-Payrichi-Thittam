import base64

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from ai_core.gemini_generator import GeminiDocumentGenerator

from .dependencies import get_settings

from .exporters import (
    filename_for,
    format_docx,
    format_pdf,
    sanitize_text,
)

from .schemas import (
    DocumentRequest,
    ExportRequest,
)


router = APIRouter()


@router.post("/generate")
def generate_document(
    request: DocumentRequest
):

    settings = get_settings()

    try:

        generator = GeminiDocumentGenerator(

            api_key=str(
                settings[
                    "gemini_api_key"
                ]
            ),

            model=str(
                settings[
                    "gemini_model"
                ]
            ),
        )

        content = generator.generate_document(

            request.document_type,

            request.parties,

            request.terms,

            request.effective_date,
        )

        max_chars = int(
            settings[
                "max_document_chars"
            ]
        )

        content = sanitize_text(
            content
        )[:max_chars]

        return {

            "success": True,

            "document_type":
                request.document_type,

            "content":
                content,

            "model":
                settings[
                    "gemini_model"
                ],
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(

            status_code=502,

            detail=(
                f"AI generation failed: "
                f"{exc}"
            )

        ) from exc


@router.post("/export/txt")
def export_txt(
    request: ExportRequest
):

    body = sanitize_text(
        request.text
    ).encode("utf-8")

    return Response(

        content=body,

        media_type=(
            "text/plain; charset=utf-8"
        ),

        headers={

            "Content-Disposition":
                (
                    "attachment; "
                    f'filename="{filename_for(request.document_type, "txt")}"'
                )
        },
    )


@router.post("/export/docx")
def export_docx(
    request: ExportRequest
):

    try:

        logo = None

        if request.logo_base64:

            logo = base64.b64decode(
                request.logo_base64
            )

        settings = get_settings()

        body = format_docx(

            request.text,

            request.document_type,

            request.terms,

            logo_bytes=logo,

            app_name=str(
                settings[
                    "app_name"
                ]
            ),
        )

        return Response(

            content=body,

            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            headers={

                "Content-Disposition":
                    (
                        "attachment; "
                        f'filename="{filename_for(request.document_type, "docx")}"'
                    )
            },
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=(
                f"DOCX export failed: "
                f"{exc}"
            )

        ) from exc


@router.post("/export/pdf")
def export_pdf(
    request: ExportRequest
):

    try:

        logo = None

        if request.logo_base64:

            logo = base64.b64decode(
                request.logo_base64
            )

        settings = get_settings()

        body = format_pdf(

            request.text,

            request.document_type,

            logo_bytes=logo,

            app_name=str(
                settings[
                    "app_name"
                ]
            ),
        )

        return Response(

            content=body,

            media_type="application/pdf",

            headers={

                "Content-Disposition":
                    (
                        "attachment; "
                        f'filename="{filename_for(request.document_type, "pdf")}"'
                    )
            },
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=(
                f"PDF export failed: "
                f"{exc}"
            )

        ) from exc