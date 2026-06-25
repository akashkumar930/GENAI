from openpyxl.worksheet import dimensions
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAIEmbeddings

embeddings = ChatOpenAIEmbeddings(model_name = "text-embedding-3-small", dimensions=64)

# vector = embeddings.embed_query("You are learning GEN AI")
# print(vector)


texts = ["you are learning GEN AI","My name is Rohan","I am from Pune"]
vector = embeddings.embed_documents(texts)
print(vector)

