from PyPDF2 import PdfReader
from groq import Groq
from docx import Document
import json
from pydantic import BaseModel
from sqlalchemy.sql import text
import streamlit as st
import uuid
import sqlite3

# class Education(BaseModel):
#     degree : str
#     university : str
#     grad_date : str

# class Experience(BaseModel):
#     job_title: str
#     company : str
#     duration : str
#     responsibilities : list[str]

class Response(BaseModel):
    name : str
    email : str
    contact : str
    skills : list[str]
    total_experience_duration : str
    # education : list[Education]
    # experiences : list[Experience]

def get_pdf_text(pdfs):
    text = ""
    print(type(pdfs))
    for pdf in pdfs:
        print(type(pdf))
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
    template = { "name" : '',
                 "email" : '',
                 "contact" : '',
                 "skills" : '', 
                 "total_experience_duration" : ''
    }

    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role" : "system",
                "content" : ''' Extract the candidate information data from this Content. Don't comment inside json. Only extract information from this context.Don't generate extra information: . make sure to give only key skills not everything. Give answer in json format. Template Output Example :'''+ json.dumps(template) + '''\n Don't give extra details in template.'''
            },
            {
                "role" : "user",
                "content" : text
            }
        ],
        model = "llama3-70b-8192",
        temperature=0.1,
        response_format={"type" : "json_object"}
    )

    return chat_completion.choices[0].message.content

def save_in_db(response, unique_id, cursor, conn):
    print(response)
    cursor.execute(
        "INSERT INTO resume_data (uid, Name, E_mail, Contact, Skills, Experience) VALUES (?,?,?,?,?,?)",
        (unique_id, response['name'], response['email'], response['contact'], response['skills'] , response["total_experience_duration"])
    )
    conn.commit()

def get_from_db(unique_id, cursor, conn):
    print(unique_id)
    with conn:
        cursor.execute(
            "SELECT Name,E_mail,Contact,Skills,Experience FROM resume_data WHERE uid = (?)", 
            ((unique_id,))
        )
        return cursor.fetchall()