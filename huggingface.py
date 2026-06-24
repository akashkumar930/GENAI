import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

# pyrefly: ignore [missing-import]
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(repo_id = "deepseek-ai/DeepSeek-V4-Pro",max_new_tokens = 500,temperature = 0.2)

model = ChatHuggingFace(llm = llm)

res = model.invoke("Hello , what is your name ?")
print(res.content)
