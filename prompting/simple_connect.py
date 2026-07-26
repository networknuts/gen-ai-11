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
    input=query
)

print(response.output_text)