import os
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",
    api_version="2023-05-15",
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# vector = embeddings.embed_query("Hello world")

# vectors = embeddings.embed_documents([
#     "Document one",
#     "Document two"
# ])

# print(len(vector), len(vectors))
