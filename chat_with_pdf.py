import streamlit as st
import os
import shutil
from openai import OpenAI
from os import environ

# langchain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter  # for chunking
from langchain.embeddings.openai import OpenAIEmbeddings  # for embeddings
from langchain.vectorstores import Chroma  # for chromadb vector storage
from langchain.chat_models import ChatOpenAI  # for LLM wrapper
from langchain.chains import ConversationalRetrievalChain  # for RAG conversational chain
from langchain.schema import Document

# PDF reading
from pypdf import PdfReader


client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)

st.title("📝 File Q&A with OpenAI")
# editing this to allow multiple file uploads
uploaded_files = st.file_uploader("Upload an article(s)", type=("txt", "md", "pdf"), accept_multiple_files=True)

# updating upon new file uploads
if "uploaded_file_names" not in st.session_state:
    st.session_state["uploaded_file_names"] = []
current_file_names = [file.name for file in uploaded_files] if uploaded_files else []
if current_file_names != st.session_state["uploaded_file_names"]:
    st.session_state["uploaded_file_names"] = current_file_names
    st.session_state["vectordb"] = None
    st.session_state["rag_chain"] = None
    st.session_state["chat_history"] = []
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article(s)"}]


question = st.chat_input(
    "Ask something about the article(s)",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article(s)"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# initialize vectordb in session state 
if "vectordb" not in st.session_state:
    st.session_state["vectordb"] = None

# initialize ragchain in session state
if "rag_chain" not in st.session_state:
    st.session_state["rag_chain"] = None

# initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# to read pdf files in chunks
def pdf_to_text(file):
    pdf = PdfReader(file)
    text_chunks = []
    for page in pdf.pages:
        try:
            text = page.extract_text()
        except Exception:
            text = ""

        if text:    
            text_chunks.append(text)
    text = "\n".join(text_chunks)
    return text

# to read txt files (assuming utf-8 encoding)
def txt_to_text(file):
    txt = file.read().decode("utf-8")
    return txt

# to parse and store multiple uploaded files
def load_files(files,existing_vectordb=None):

    all_docs=[]
    for file in files:
        #  determine file type and extract text
        filename = file.name
        if filename.endswith(".pdf"):
            text = pdf_to_text(file)
        elif filename.endswith(".txt") or filename.endswith(".md"):
            text = txt_to_text(file)
        else:
            st.warning(f"Unsupported file type: {filename}")
            continue
        # if file is empty, skip
        if not text or text.strip() == "":
            continue
        

        doc = Document(page_content=text, metadata={"source": filename})
        all_docs.append(doc)
    
    if not all_docs:
        return existing_vectordb if 'existing_vectordb' in locals() else None
    

    # chunking documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(all_docs)
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.environ["API_KEY"],
        model="openai.text-embedding-3-small"
    )
    if existing_vectordb:
        # Add new docs to existing vectordb
        existing_vectordb.add_documents(docs)
        return existing_vectordb
    else:
        # Create new vectordb
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            collection_name="assignment_collection"
        )
        return vectordb
    
# process files and store vectordb and rag_chain in session state
if uploaded_files and st.session_state.vectordb is None:
    with st.spinner("Processing uploaded files..."):
        vectordb = load_files(uploaded_files,st.session_state.get("vectordb"))
        st.session_state["vectordb"] = vectordb
###
        if vectordb is not None and st.session_state["rag_chain"] is None:
            llm = ChatOpenAI(
                temperature=0,
                model_name="openai.gpt-4o",
                openai_api_key=os.environ["API_KEY"]
            )
            retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                return_source_documents=True
            )
            st.session_state["rag_chain"] = chain



if question and uploaded_files:
    
    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    if st.session_state["rag_chain"] is None:
        st.chat_message("assistant").write("RAG pipeline not ready. Please upload readable files.")

    else:
        chain = st.session_state["rag_chain"]
        
        with st.chat_message("assistant"):
            result = chain({"question": question, "chat_history": st.session_state["chat_history"]})
            answer = result["answer"]
            # sources = [doc.metadata["source"] for doc in result["source_documents"]]
            # st.write(f"Answer (from {', '.join(set(sources))}): {answer}")
            st.write(answer)
            st.session_state["chat_history"].append((question, answer))
            st.session_state.messages.append({"role": "assistant", "content": answer})
        

