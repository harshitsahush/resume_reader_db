import streamlit as st
from io import StringIO
import pandas as pd
from utils import *

st.title("Resume Reader")
st.header("Built using Streamlit and Groq")
doc = st.file_uploader("Please upload the resume here.", accept_multiple_files=True)
option = st.selectbox("Select the files type", (".pdf", ".docx", ".txt"))
submit = st.button("Process")

if(submit):
    if(doc):
        if(option == ".pdf"):
            text = get_pdf_text(doc)
        elif(option == ".docx"):
            text = get_docx_text(doc)
        else:
            text = doc[0].read().decode("utf-8")

        response = query_response(text)
        st.success(json.loads(response))
       
        
    else:
        st.error("Please upload a file!!!")