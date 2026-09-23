from mcp import Client
from openai import AsyncOpenAI
from dotenv import load_dotenv
import json
import asyncio

# SETUP THE ENVIRONMENT
load_dotenv()
MCP_SERVER_URL = "http://localhost:8000/mcp"

async def main():
    query = input("Enter banking query: ")
    async with Client(MCP_SERVER_URL) as mcp_client, AsyncOpenAI() as ai_client:
        tool_list = await mcp_client.list_tools()
        tools = [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            }
            for tool in tool_list.tools
        ]
        # LET LLM DECIDE ON A TOOL
        response = await ai_client.responses.create(
            model="gpt-5.6-luna",
            instructions="You are an MCP Client with access to tools for banking requests.",
            input=query,
            tools=tools,
            parallel_tool_calls=False
        )
        # CALL THE SELECTED TOOL AND PRINT ITS RESULT
        for call in response.output:
            if call.type == "function_call":
                print(f"LLM SELECTED TOOL: {call.name}")
                result = await mcp_client.call_tool(call.name,json.loads(call.arguments))
                print(result.content[0].text)

asyncio.run(main())