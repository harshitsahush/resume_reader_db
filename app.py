from utils import *

#assign a uniqueid(uid) at each session
#make table if not made
#enter data along with uid
#fetch data only for the current uid

if('uid' not in st.session_state):
    st.session_state['uid'] = str(uuid.uuid4())


conn = sqlite3.connect("resume_info.pd")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS resume_data (uid TEXT, Name TEXT, E_mail TEXT, Contact TEXT, Skills TEXT, Experience TEXT)")
conn.commit()


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
        response_dict = json.loads(response)
        print(st.session_state["uid"])

        save_in_db(response_dict, st.session_state['uid'], cursor, conn)
        st.success("Entry saved!")

        df = get_from_db(st.session_state['uid'], cursor, conn)
        st.dataframe(df)

    else:
        st.error("Please upload a file!!!")