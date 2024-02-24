import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
import os
from htmlTemplates import css, bot_template, user_template


# Methode d'import des pdfs
def get_pdf_text(pdf_docs): 
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Découpage des textes en "chunks"
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1024,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Vectorisation
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True) 
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    # st.write(response)
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            

def main():
    load_dotenv()
    st.set_page_config(page_title="Discutez avec plusieurs PDF",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Discutez avec plusieurs PDF :books:")
    user_question = st.text_input("Posez une question sur votre documents uploader:")
    if user_question:
        handle_userinput(user_question)

    # st.write(user_template.replace("{{MSG}}", "hello robot"), unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}", "hello human"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Vos documents")
        pdf_docs = st.file_uploader(
            "Téléverser vos PDF ici et cliquez sur 'Traiter'", accept_multiple_files=True)
        if st.button("Traiter"):
            with st.spinner("Traitement encours..."):
                #recuperer le texte pdf
                raw_text = get_pdf_text(pdf_docs)

                # récupérer les morceaux de texte
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)

                # créer un magasin de vecteurs
                vectorstore = get_vectorstore(text_chunks)
                st.write(vectorstore)

                # créer une chaîne de conversation
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                


if __name__ == '__main__':
    main()
