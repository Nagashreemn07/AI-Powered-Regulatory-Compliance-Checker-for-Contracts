from google import genai
from google.genai import types
from pydantic import BaseModel
from enum import Enum
import PyPDF2
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Create Gemini client once
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------- Document Type --------------------
class DocumentType(str, Enum):
    DPA = "Data Processing Agreement"
    JCA = "Joint Controller Agreement"
    C2C = "Controller-to-Controller Agreement"
    Subprocessor = "Processor-to-Subprocessor Agreement"
    SCC = "Standard Contractual Clauses"

class FindDocumentType(BaseModel):
    document_type: DocumentType

def document_type(file_path: str) -> str:
    """Detect the type of a GDPR-related document using Gemini API."""

    # Extract text from PDF
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""

    # Prepare prompt
    prompt = f"""
    Determine the type of this document. It must be one of the following:
    1. Data Processing Agreement
    2. Joint Controller Agreement
    3. Controller-to-Controller Agreement
    4. Processor-to-Subprocessor Agreement
    5. Standard Contractual Clauses

    Input Document Text:
    {text}

    Return the response in JSON format:
    {{
        "document_type": "<type_of_document>"
    }}
    """

    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type="application/json"
        )
    )

    # Parse JSON response
    try:
        result_json = json.loads(response.text)
        doc_type = result_json.get("document_type")
        return doc_type
    except Exception as e:
        print("Error parsing Gemini response:", e)
        return None

# -------------------- Agreement Comparison --------------------
def compare_agreements(unseen_data: str, template_data: str):
    """Compare two agreements using Gemini API and return structured results."""

    prompt = f"""
    You are an AI legal assistant specialized in contract review and compliance.

    Compare the two documents below:

    Template document (regulatory standard reference):
    {template_data}

    Document under review:
    {unseen_data}

    Tasks:
    1. Identify any missing or altered clauses in the new contract compared to the template.
    2. Flag potential compliance risks based on GDPR regulations.
    3. Assign a risk score between 0 and 100 for the new contract (0 = no risk, 100 = maximum risk)
    4. Provide reasoning for the assigned risk score.
    5. Suggest specific amendments or recommendations to bring the contract in line with current regulatory standards and best practices.
    6. Provide the response in a concise, structured format, like this:

    - Missing Clauses: [...]
    - Potential Compliance Risks: [...]
    - Risk Score (0-100): ...
    - Reasoning: [...]
    - Recommendations: [...]

    Keep each section brief and focused on key points. Avoid long paragraphs or unnecessary details.
    """

    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            temperature=0.3
        )
    )

    # Print structured result
    print(response.text)
    return response.text
