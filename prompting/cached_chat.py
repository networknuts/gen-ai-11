from dotenv import load_dotenv
from openai import OpenAI

# LOAD THE .ENV FILE
load_dotenv()

# ASK FOR CUSTOMER QUERY
query = input("Enter your query: ")

# MAKE THE REQUEST TO OPENAI LLM 
client = OpenAI()
response = client.responses.create(
    model="gpt-5.6-luna",
    input=[
        {
            "role": "user",
            "content": "hello, my name is aryan."
        },
        {
            "role": "assistant",
            "content": "Hello, Aryan! Nice to meet you. How can I help you today?"
        },
        {
            "role": "user",
            "content": query
        }
    ]
)

print(response.output_text)