from typing import TypedDict 
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# LANGCHAIN OPENAI MODULE
load_dotenv()
llm = ChatOpenAI(model="gpt-5.6-luna")

# STEP 1: DEFINE THE STATE
class CodeState(TypedDict):
    user_request: str #done
    code: str #done
    rating: int 

# STEP 2: CREATING THE NODES

# NODE 1: GENERATE CODE
def generate_code(state: CodeState):
    response = llm.invoke(
        f"""
        Write code for the following user request:
        {state["user_request"]}

        Return only the code.
        """
    )
    return {
        "code": response.content
    }

# NODE 2: JUDGE CODE
def judge_code(state: CodeState):
    response = llm.invoke(
        f"""
        Review the given code on the following parameters:
        1. Error handling
        2. Scalability
        3. Modern code practices

        Provide a rating to the code after reviewing it on the above parameters.

        Code:
        {state["code"]}

        Only Return the rating in the following format: (do not provide the feedback data)
        integer value between 1-10
        """
    )
    return {
        "rating": response.content
    }

# STEP 3: BUILDING THE RELATIONSHIP
graph = StateGraph(CodeState)

#DEFINED YOUR NODES
graph.add_node("generate_code",generate_code)
graph.add_node("judge_code",judge_code)

#DEFINED WHICH NODE TRAVELS TO WHICH NODE
graph.add_edge(START,"generate_code")
graph.add_edge("generate_code","judge_code")
graph.add_edge("judge_code",END)

#COMPILE THE GRAPH
app = graph.compile()

# STEP 4: RUN THE AGENT

user_request = input("Enter idea to create code for: ")

result = app.invoke({
    "user_request": user_request,
    "code": "",
    "rating": ""
})

print("GENERATED CODE")
print(result["code"])

print("\nRATING")
print(result["rating"])