from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

texts = ["you are learning GEN AI","My name is Rohan","I am from Pune"]
vector = embeddings.embed_documents(texts)
# print(vector)
print(len(vector))
print(vector[0])