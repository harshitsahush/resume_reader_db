from PyPDF2 import PdfReader
from groq import Groq
from docx import Document
import json
from pydantic import BaseModel

class Education(BaseModel):
    degree : str
    university : str
    grad_date : str

class Experience(BaseModel):
    job_title: str
    company : str
    duration : str
    responsibilities : list[str]

class Response(BaseModel):
    name : str
    email : str
    contact : str
    skills : list[str]
    education : list[Education]
    experiences : list[Experience]

def get_pdf_text(pdfs):
    text = ""
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text() + "/n"
    return text

def get_docx_text(docx_files):
    for docx_file in docx_files:
        document = Document(docx_file)
        text = ""
        for para in document.paragraphs:
            text += para.text + "\n"
    return text

def query_response(text):
    client = Groq(api_key="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")
    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role" : "system",
                "content" : """You are a resume extractor API that responds in JSON. The provided text is a resume and the response must use the schema \n """ +
                json.dumps(Response.model_json_schema(), indent = 2)
            },
            {
                "role" : "user",
                "content" : text
            }
        ],
        model = "llama3-70b-8192",

        response_format={"type" : "json_object"}
    )

    return chat_completion.choices[0].message.content

