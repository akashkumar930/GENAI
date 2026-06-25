from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage

print("_____________________________Welcome, Type 'Exit' to quit_____________________________________________")
print("1. Funny")
print("2. Angry")
print("3. Sarcastic")
print("4. Sad")
print("5 Romantic")

personalities = {
    "1": "You are a funny and witty AI agent, if asked about any topic you have to answer with jokes and make sure that answer is related to the topic",
    "2": "You are an angry AI agent, if asked about any topic you have to answer with anger and make sure that answer is related to the topic",
    "3": "You are a sarcastic AI agent, if asked about any topic you have to answer with sarcasm and make sure that answer is related to the topic",
    "4": "You are a sad AI agent, if asked about any topic you have to answer with sadness and make sure that answer is related to the topic",
    "5": "You are a romantic AI agent, if asked about any topic you have to answer with romance and make sure that answer is related to the topic",
}

choice = input("\n Choose personality(1-5): ")
if choice not in personalities:
    print("Invalid choice")
    exit()

messages = [
    SystemMessage(content=personalities[choice]),
]



while True:
    prompt = input("YOU: ")
    messages.append(HumanMessage(content=prompt))
    if prompt.lower() == "exit":
        break
    model = ChatMistralAI(model="mistral-small-2603", temperature=0.9, max_tokens=100)
    res = model.invoke(messages)
    messages.append(AIMessage(content=res.content))
    print("BOT: ",res.content)
    print(messages) 