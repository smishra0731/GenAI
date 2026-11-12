from langchain_groq import ChatGroq  # Import the ChatGroq class from langchain_groq
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage  # Import message classes from langchaincore.messages
#Initialize a chat model using the ChatGroq class with the specified model and temperature
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9)  # Initialize the chat model using the ChatGroq class

print("Choose your AI mode.")
print("1. Funny AI")
print("2. Sad AI")
print("3. Angry AI")
choice = int(input("Enter the number corresponding to your choice: "))

if choice == 1:
    mode = "You are a Funny AI agent. You are humorous and entertaining."
elif choice == 2:
    mode = "You are a Sad AI agent. You are empathetic and understanding."
elif choice == 3:
    mode = "You are an Angry AI agent. You respond aggressively and impatiently."

#Declare a variable to store the messages
messages = [
    SystemMessage(content=mode)
] 

print("-----------------Welcome to GenAI Chatbot, Type 0 to exit -----------------")
while True:    
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(messages)  # Invoke the model with a sample prompt
    messages.append(AIMessage(content=response.content))  # Append the AI response to the messages list
    print("Bot: ", response.content)  # Print the response from the model

print(messages)