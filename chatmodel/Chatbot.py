from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI
messages = []
print("_____________________________Welcome, Type 'Exit' to quit_____________________________________________")
while True:
    prompt = input("YOU: ")
    messages.append(prompt)
    if prompt.lower() == "exit":
        break
    model = ChatMistralAI(model="mistral-small-2603", temperature=0.9, max_tokens=100)
    res = model.invoke(messages)
    messages.append(res.content)
    print("AI: ",res.content)
    print(messages)