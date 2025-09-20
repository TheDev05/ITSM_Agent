from langchain.tools import tool
from langchain.vectorstores import Chroma
from Models.embedding import embeddings
import Utils.status_manager as status_manager
import time

@tool('get_internal_information', description = "retrive internal FAQ informations from RAG documents")  
def get_internal_information(query: str):
    status_manager.add_status("looking into internal informations for solutions...")
    time.sleep(2)
    
    vector_store = Chroma(
        embedding_function = embeddings,
        persist_directory = './persit',
        collection_name = 'demo'
    )
    
    print('RAG invoked')

    retriver = vector_store.as_retriever(search_kwargs = {'k' : 2})
    result = retriver.invoke(query)
    
    status_manager.add_status("solution found, augumenting...")
    time.sleep(2)
    
    return '\n\n'.join([doc.page_content for doc in result])