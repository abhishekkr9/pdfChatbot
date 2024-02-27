from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def text_to_vectordb():
    loader = PyPDFDirectoryLoader('new_articles')
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    allData = text_splitter.split_documents(document)

    db = Chroma.from_documents(documents = allData, embedding =  embeddings, persist_directory='db_folder')
    db.persist()
    db = None
    
    
def get_data_from_db(query):
    if not Path("new_articles").exists():
        text_to_vectordb()
    else:
        vector_db = Chroma(persist_directory='db_folder', embedding_function=embeddings)
        retriever = vector_db.as_retriever(search_kwargs={'k': 2})

        llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

        llm_response = qa_chain.invoke(query)
        return llm_response
    
import os

def save_uploaded_file(uploaded_file, save_directory):
  if uploaded_file is not None:
    if not os.path.exists(save_directory):
      os.makedirs(save_directory)
    filename = f"{uploaded_file.name}"
    filepath = os.path.join(save_directory, filename)
    with open(filepath, "wb") as f:
      f.write(uploaded_file.read())
    st.success(f"File '{filename}' saved successfully!")


def main():
    st.set_page_config("Chat with multiple PDF")
    st.title('Document Search')
    with st.sidebar:

        uploaded_files = st.file_uploader("Choose files:", accept_multiple_files=True)

        save_directory = "new_articles"
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                save_uploaded_file(uploaded_file, save_directory)


    with st.form(key='my_form'):
        input_box = st.text_input('Ask a question related to the document...')
        try:
            result = get_data_from_db(input_box)
        except:
            pass
        if not input_box:
            st.warning('Please enter a question.')
        st.form_submit_button(label='Submit')

    if input_box:
        st.write(result['result'])
        st.caption("### Source")
        st.caption(result)

if __name__ == "__main__":
    main()
