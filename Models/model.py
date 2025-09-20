from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = AzureChatOpenAI(
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_version = "2025-01-01-preview"
)

# response = model.invoke('what is india?')
# print(response)
