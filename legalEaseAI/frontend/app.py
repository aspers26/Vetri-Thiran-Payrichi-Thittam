from __future__ import annotations

import base64
import html
import os

import requests
import streamlit as st

from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide",
)


st.markdown(
    """
    <style>

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
    }

    .hero {
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,.25);
        margin-bottom: 1.5rem;
    }

    .legal-preview {
        min-height: 500px;
        max-height: 700px;
        overflow-y: auto;
        padding: 24px;
        border-radius: 14px;
        background: #15171a;
        color: #f4f4f4;
        line-height: 1.7;
        border: 1px solid #333;
        font-family: Georgia, serif;
    }

    .muted {
        opacity: .72;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero">

        <h1>⚖️ LegalEase</h1>

        <p class="muted">
            AI-powered legal document drafting,
            editing and export.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:

    st.header(
        "Document details"
    )

    document_type = st.selectbox(

        "Document type",

        [
            "Employment Contract",

            "Lease Agreement",

            "Non-Disclosure Agreement (NDA)",

            "Freelance Work Contract",

            "Employment Offer Letter",

            "General Agreement",

            "Custom",
        ],
    )

    if document_type == "Custom":

        document_type = st.text_input(

            "Custom document type",

            "Service Agreement"
        )


    parties = st.text_area(

        "Parties involved",

        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),

        height=110,
    )


    terms = st.text_area(

        "Terms & conditions",

        placeholder=(
            "Payment within 30 days of invoice; "
            "Provider delivers work by the agreed deadline; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),

        height=180,

        help=(
            "Separate individual terms with semicolons."
        ),
    )


    effective_date = st.text_input(

        "Effective date",

        "April 15, 2026"
    )


    logo = st.file_uploader(

        "Optional logo",

        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    generate = st.button(

        "✨ Generate Document",

        type="primary",

        use_container_width=True
    )


if "document" not in st.session_state:

    st.session_state.document = ""


if "generated_type" not in st.session_state:

    st.session_state.generated_type = (
        document_type
    )


if generate:

    missing = []


    if not document_type.strip():

        missing.append(
            "document type"
        )


    if not parties.strip():

        missing.append(
            "parties"
        )


    if not terms.strip():

        missing.append(
            "terms"
        )


    if not effective_date.strip():

        missing.append(
            "effective date"
        )


    if missing:

        st.error(
            "Please provide: "
            + ", ".join(missing)
            + "."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "effective_date":
                effective_date,
        }


        with st.spinner(
            "Generating your legal draft..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=180,
                )


                response.raise_for_status()


                data = response.json()


                st.session_state.document = (
                    data["content"]
                )


                st.session_state.generated_type = (
                    document_type
                )


                st.success(
                    "Document generated successfully."
                )


            except requests.RequestException as exc:

                st.error(

                    "Could not reach the backend. "
                    f"Make sure FastAPI is running "
                    f"at {BACKEND_URL}.\n\n"
                    f"Details: {exc}"
                )


            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


st.subheader(
    "Document preview"
)


if st.session_state.document:

    tab_preview, tab_edit, tab_download = (
        st.tabs(
            [
                "Preview",
                "✏️ Edit",
                "⬇️ Download"
            ]
        )
    )


    with tab_preview:

        safe = html.escape(
            st.session_state.document
        )

        safe = safe.replace(
            "\n\n",
            "</p><p>"
        )

        safe = safe.replace(
            "\n",
            "<br>"
        )


        st.markdown(

            (
                '<div class="legal-preview">'
                f"<p>{safe}</p>"
                "</div>"
            ),

            unsafe_allow_html=True
        )


    with tab_edit:

        edited = st.text_area(

            "Edit the generated document",

            value=(
                st.session_state.document
            ),

            height=650,
        )


        if st.button(
            "Save edits"
        ):

            st.session_state.document = (
                edited
            )

            st.success(
                "Edits saved."
            )


    with tab_download:

        st.write(
            "Export the current version "
            "of the document."
        )


        logo_b64 = None


        if logo is not None:

            logo_b64 = (
                base64.b64encode(
                    logo.getvalue()
                ).decode("ascii")
            )


        export_payload = {

            "text":
                st.session_state.document,

            "document_type":
                st.session_state.generated_type,

            "terms":
                terms,

            "logo_base64":
                logo_b64,
        }


        col1, col2, col3 = (
            st.columns(3)
        )


        def fetch_export(
            endpoint: str
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}{endpoint}",

                    json=export_payload,

                    timeout=60,
                )

                response.raise_for_status()

                return (
                    response.content,
                    None
                )

            except Exception as exc:

                return (
                    None,
                    str(exc)
                )


        with col1:

            txt, error = fetch_export(
                "/export/txt"
            )


            if txt:

                st.download_button(

                    "Download TXT",

                    data=txt,

                    file_name=(
                        "legal_document.txt"
                    ),

                    mime="text/plain",

                    use_container_width=True
                )

            elif error:

                st.error(error)


        with col2:

            docx, error = fetch_export(
                "/export/docx"
            )


            if docx:

                st.download_button(

                    "Download DOCX",

                    data=docx,

                    file_name=(
                        "legal_document.docx"
                    ),

                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),

                    use_container_width=True
                )

            elif error:

                st.error(error)


        with col3:

            pdf, error = fetch_export(
                "/export/pdf"
            )


            if pdf:

                st.download_button(

                    "Download PDF",

                    data=pdf,

                    file_name=(
                        "legal_document.pdf"
                    ),

                    mime="application/pdf",

                    use_container_width=True
                )

            elif error:

                st.error(error)


else:

    st.info(

        "Enter the document details in the "
        "sidebar and click **Generate Document** "
        "to create a draft."
    )


st.divider()


st.caption(

    "LegalEase produces AI-assisted drafts "
    "for review. It is not a substitute for "
    "advice from a qualified legal professional."
)