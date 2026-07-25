import requests
import json 
from dotenv import load_dotenv
import os 

# LOAD THE .ENV FILE
load_dotenv() 

# ASK FOR CUSTOMER QUESTION
human_question = input("Enter your query: ")

# OPENAI API KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# SET THE OPENAI URL
OPENAI_URL = "https://api.openai.com/v1/responses"

# HEADERS
OPENAI_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# DATA
OPENAI_DATA = {
    "model": "gpt-5.6",
    "input": human_question
}

# MAKING THE HTTP REQUEST
response = requests.post(OPENAI_URL,data=json.dumps(OPENAI_DATA),headers=OPENAI_HEADERS)

print(response.json())
#print(response.json()['output'][0]['content'][0]['text'])