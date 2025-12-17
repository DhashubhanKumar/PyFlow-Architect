import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# We use Llama 3 - the best open-source model available on Groq
llm = ChatGroq(model="llama-3.3-70b-versatile")

try:
    response = llm.invoke("The Groq brain is alive!")
    print("AI Response:", response.content)
except Exception as e:
    print(f"Error: {e}")