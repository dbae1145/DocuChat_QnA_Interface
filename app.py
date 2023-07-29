import re
from io import BytesIO
from typing import List

from langchain import LLMChain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader

import streamlit as st

from htmlTemplates import css, bot_template, user_template

def parse_file(file: BytesIO, filetype: str) -> List[str]:
    if filetype == 'pdf':
        pdf = PdfReader(file)
        output = []
        for page in pdf.pages:
            text = page.extract_text()
            text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
            text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
            text = re.sub(r"\n\s*\n", "\n\n", text)
            output.append(text)
        return output

# Define a function to convert text content to a list of documents
def text_to_docs(text: str, filename: str) -> List[Document]:
    """Converts a string or list of strings to a list of Documents
    with metadata."""
    if isinstance(text, str):
        # Take a single string as one page
        text = [text]
    page_docs = [Document(page_content=page) for page in text]

    # Add page numbers and filename as metadata
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1
        doc.metadata["filename"] = filename

    # Split pages into chunks
    doc_chunks = []

    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=100,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i, "filename": doc.metadata["filename"]}
            )
            # Add sources a metadata
            doc.metadata["source"] = f"{doc.metadata['filename']} {doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)
    return doc_chunks

# Define a function for the embeddings
def test_embed(api, pages):
    embeddings = OpenAIEmbeddings(openai_api_key=api)
    with st.spinner("It's indexing..."):
        index = FAISS.from_documents(pages, embeddings)
    st.success("Embeddings done.", icon="✅")
    return index

def get_conversation_chain(vectorstore, api):
    llm = ChatOpenAI(openai_api_key=api, temperature=0.0)

    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_with_sources_chain(llm)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        memory = memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

def reset_conversation():
    st.session_state.conversation = get_conversation_chain(st.session_state.vectorstore, st.session_state.api)
    st.session_state.chat_history = []

def main():
    st.set_page_config(
        page_title="🐄 IntelliKaroba 🐄",  # Browser tab title
    )
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">',unsafe_allow_html=True)
    st.write(css, unsafe_allow_html=True)
    st.title("🐄 IntelliKaroba 🐄")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "reset" not in st.session_state:
        st.session_state.reset = False

    with st.sidebar:
        st.markdown("**Introduction**")
        st.markdown("""
        Welcome to IntelliKaroba!
        Got documents? Don't get stampeded! 
        Bring them over to IntelliKaroba, your one-of-a-kind breed of chat interface. 
        We chew through content and ruminate on information until we provide the answers you seek.
        Inspired by Karoba, our beloved muse cow, we're ready to yield rich, creamy insights. 
        So, moo-ve over traditional chat interfaces! IntelliKaroba is here to steer you to the greener pastures of knowledge. 
        Let’s embark on this trail of discovery together!  
        """)
        uploaded_file = st.file_uploader("**Upload Your File**", type=["pdf"],accept_multiple_files=True)
        api = st.text_input("**Enter OpenAI API Key**", type="password", placeholder="sk-")

        if 'pages' not in st.session_state:
            st.session_state.pages = []

        if st.button("Process", key="process_document"):
            with st.spinner("Processing"):
                doc_dict = {}
                for file in uploaded_file:
                    filetype = file.name.split('.')[-1]
                    doc = parse_file(file, filetype)
                    pages = text_to_docs(doc, file.name)
                    doc_dict[file.name] = pages

                st.session_state.pages = doc_dict
                flattened_list = [item for sublist in list(st.session_state.pages.values()) for item in sublist]
                index = test_embed(api, flattened_list)
                st.session_state.vectorstore = index
                st.session_state.api = api
                st.session_state.conversation = get_conversation_chain(index, api)

    with st.expander("Show Page Content", expanded=False):
        if st.session_state.pages:
            files = list(st.session_state.pages.keys())
            filename = st.selectbox(label = "Select File", options=files)
            page_sel = st.number_input(
                label="Select Page", min_value=1, max_value=len(st.session_state.pages[filename]), step=1
            )
            st.session_state.pages[filename][page_sel - 1]

    query = st.text_input("**Ask about your data**", placeholder="Ask me anything",)
    submit_button = st.button('Submit', key="submit_button")

    if submit_button and not st.session_state.reset:
        handle_userinput(query)

    if st.button('Reset Chat'):
        st.session_state.reset = True
        reset_conversation()
    else:
        st.session_state.reset = False

    chat_history = reversed(st.session_state.chat_history)
    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
