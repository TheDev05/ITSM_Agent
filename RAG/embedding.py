from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from Models.embedding import embeddings

def persist_documents():
    loader = PyPDFLoader('Documents\ITSM_FAQ.pdf')
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap = 50)
    chunks = splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        documents = chunks,
        embedding = embeddings,
        persist_directory = "./persit",
        collection_name = 'demo'
    )

    vector_store.persist()