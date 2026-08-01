from dotenv import load_dotenv
from openai import OpenAI 

# SECTION 1: SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# SECTION 2: READ THE GIVEN SYSTEM PROMPT
f = open("simple_prompt.txt","r")
SYSTEM_PROMPT = f.read()
f.close()

# SECTION 3: ASK FOR CUSTOMER QUERY
human_query = input("Enter your query: ")

# SECTION 4: INVOKE THE LLM CALL
response = client.responses.create(
    model="gpt-5.6-luna",
    input=human_query,
    instructions=SYSTEM_PROMPT
)

# SECTION 5: PRINT THE OUTPUT
print(response.output_text)