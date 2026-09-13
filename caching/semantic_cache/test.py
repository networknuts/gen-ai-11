from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai = OpenAI()

def get_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

result = get_embedding("what is devops?")
print(result)