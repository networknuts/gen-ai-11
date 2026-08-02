import requests
from dotenv import load_dotenv
from openai import OpenAI 
import os
import json

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# READ TOOL DESCRIPTION
f = open("weather_tool_description.txt","r")
weather_tool_desc = f.read()
f.close()

# CREATE THE FIRST TOOL - GET WEATHER TOOL
def get_weather(zipcode):
    countrycode = "in"
    apikey = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"
    result = requests.get(url)
    response = result.json()
    return response

# TOOL SCHEMA
openai_tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": weather_tool_desc,
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "The zipcode of the location to get the weather of."
                },
            },
            "required": ["zipcode"],
        },
    },
]

# ASK FOR CUSTOMER QUERY
user_query = input("Human Query: ")

# FIRST LLM CALL
response = client.responses.create(
    model="gpt-5.6-luna",
    input=user_query,
    tools=openai_tools
)

# EMPTY LIST TO CONTAIN TOOL OUTPUT
function_output = []

# EXECUTE TOOL CALL
for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments) #str to dict 
        if item.name == "get_weather":
            result = get_weather(args['zipcode'])
            print("RAW TOOL OUTPUT")
            print(result)
            print("-"*20)
        else:
            result = "unknown function called"

        function_output.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps({"result": result}) #dict to str 
        })

# SECOND LLM CALL
final_response = client.responses.create(
    model="gpt-5.6-luna",
    input=function_output,
    previous_response_id=response.id
)

print("AI SUMMARIZED OUTPUT")
print(final_response.output_text)