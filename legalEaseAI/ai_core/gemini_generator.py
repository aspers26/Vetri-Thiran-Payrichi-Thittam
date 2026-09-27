import google.generativeai as genai


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI legal-document drafting assistant.

Your job is to produce a structured DRAFT of the requested legal document
from the user's supplied facts.

Important rules:

1. Do not invent names.
2. Do not invent dates.
3. Do not invent monetary amounts.
4. Do not invent addresses.
5. Do not invent legal citations.
6. Do not invent jurisdictions.
7. Do not invent obligations that were not requested.
8. Use professional legal drafting language.
9. Use clear headings and numbered sections.
10. Include signature blocks where appropriate.
11. If important information is missing, use a placeholder such as:
    [INSERT MISSING INFORMATION]
12. Do not claim that the generated document is legally valid in every
    jurisdiction.
13. Do not claim to be a lawyer.
14. Return only the document draft.
15. Do not wrap the document inside Markdown code fences.
"""


class GeminiDocumentGenerator:

    def __init__(
        self,
        api_key: str,
        model: str
    ) -> None:

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:

        prompt = f"""
Create a professional legal-document DRAFT.

DOCUMENT TYPE
-------------
{document_type}


PARTIES
-------
{parties}


TERMS AND CONDITIONS
--------------------
{terms}


EFFECTIVE DATE
--------------
{effective_date}


DOCUMENT REQUIREMENTS
---------------------

Create a complete structured draft.

Where appropriate include:

1. Document title
2. Introduction / recitals
3. Definitions
4. Parties
5. Scope / purpose
6. Responsibilities
7. Payment provisions
8. Confidentiality
9. Intellectual property
10. Term and termination
11. Representations
12. Liability provisions
13. Dispute provisions
14. Governing law placeholder if jurisdiction was not supplied
15. General provisions
16. Signature section

Only include provisions that make sense for the selected document type.

Do not fabricate missing information.

For missing important information use placeholders such as:

[INSERT ADDRESS]

[INSERT PAYMENT AMOUNT]

[INSERT GOVERNING LAW]

[INSERT TERMINATION PERIOD]

Return only the legal document.
"""

        response = self.client.models.generate_content(

            model=self.model,

            contents=prompt,

            config=types.GenerateContentConfig(

                system_instruction=SYSTEM_INSTRUCTION,

                temperature=0.25,

                max_output_tokens=12000,
            ),
        )

        text = (
            response.text
            if response.text
            else ""
        ).strip()

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text