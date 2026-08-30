from typing import TypedDict 
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json 
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient

# LANGCHAIN OPENAI MODULE
load_dotenv()

llm_developer = ChatOpenAI(model="gpt-5.6-terra") 
llm_qa = ChatOpenAI(model="gpt-5.6-sol") 

MAX_RETRIES = 3

# MONGODB PYTHON CONNECTION

client = MongoClient("mongodb://localhost:27017")

# DEFINE THE STATE
class CodeState(TypedDict):
    user_request: str 
    code: str 
    rating: int 
    retries: int 
    feedback: str 
    status: str #running, approved, failed

# NODE 1: DEVELOPER NODE
def developer_node(state: CodeState):
    prompt = f"""
    You are a java developer.
    Write code for the following requirement of the user:
    {state['user_request']}

    If feedback is provided, improve the previous version of the code.
    Previous code:
    {state['code']}

    Feedback:
    {state['feedback']}

    Only return the java code, no markdown.
    """
    result = llm_developer.invoke(prompt).content.strip()
    return {
        "code": result,
        "feedback": ""
    }

# NODE 2: QA NODE
def qa_node(state: CodeState):
    prompt = f"""
    You are a senior QA java engineer.
    Evaluate the following java code for the given requirements:
    - Correctness of the code
    - Structure of the code
    - Readability of the code
    - Is the code following industry best practices
    - Error handling capability of the code
    - The scalability of the code if need to scale to hundreds of users
    - Is the code having any vulnerabilities

    Return the output in the following dict format:
    {{
        "rating": integer value between 1-10,
        "feedback": string value with clear explanations of improvements to make to the code 
    }}

    Code: 
    {state['code']}
    """
    ai_output = llm_qa.invoke(prompt).content.strip()
    result = json.loads(ai_output)
    return {
        "rating": int(result["rating"]),
        "feedback": result["feedback"]
    }

# NODE 3: APPROVAL NODE
def set_approved(state: CodeState):
    return {"status": "approved"}

# NODE 4: FAILURE NODE
def set_failed(state: CodeState):
    return {"status": "failed"}

# NODE 5: INCREMENTAL RETRY NODE
def incremental_retry(state: CodeState):
    return {"retries": state['retries']+1}

# NODE 6: ROUTING NODE
def check_rating(state: CodeState):
    if state['rating'] >= 7:
        return "approved"
    if state['retries'] >= MAX_RETRIES:
        return "failed"
    return "retry"

# BUILD THE GRAPH
graph = StateGraph(CodeState)

# ASSIGN AN ALIAS TO EVERY NODE
graph.add_node("developer",developer_node)
graph.add_node("qa",qa_node)
graph.add_node("approval",set_approved)
graph.add_node("failure",set_failed)
graph.add_node("retry",incremental_retry)

# DECLARE THE STARTING POINT OF THE WORKFLOW
graph.set_entry_point("developer")

# DECLARE THE FLOW OF THE DATA
graph.add_edge("developer","qa")
graph.add_conditional_edges(
    "qa",
    check_rating,
    {
        "approved": "approval",
        "failed": "failure",
        "retry": "retry"
    }
)
graph.add_edge("approval",END)
graph.add_edge("failure", END)
graph.add_edge("retry","developer")

# COMPILE THE WORKFLOW
memory = MongoDBSaver(client)
app = graph.compile(checkpointer=memory)

# DECLARE THE UNIQUE IDENTIFIES
user_id = "1"
session_id = "2"

thread_id = f"{user_id}_{session_id}"

# CHECK FOR EXISTING THREAD ID
read_config = {"configurable": {"thread_id": thread_id}}
existing_thread = memory.get(read_config)

# EXECUTE BASED UPON EXISTING OR NON-EXISTING THREAD ID
try:
    if existing_thread:
        print("RESUMING FROM FAILED EXECUTION")
        result = app.invoke({},config=read_config)
    else:
        # TAKE THE USER INPUT
        print("THIS IS A FRESH EXECUTION")
        user_input = input("Enter java app request: ")
        # EXECUTE THE AGENTIC WORKFLOW
        result = app.invoke({
            "user_request": user_input,
            "code": "",
            "rating": 0,
            "feedback": "",
            "retries": 0,
            "status": "running"
        },config=read_config)
    print("\nFINAL RESULT\n")
    print(f"Code: {result['code']}")
    print(f"Rating: {result['rating']}")
    print(f"Retries Used: {result['retries']}")
    print(f"Feedback: {result['feedback']}")
    print(f"Status: {result['status']}")
except Exception as e:
    print(f"Error: {e}")