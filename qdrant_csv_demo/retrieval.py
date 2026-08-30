from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI


# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "csv_incidents_collection"
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large"
)


# STEP 1: CONNECT TO VECTOR DATABASE
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL,
)


# STEP 2: ASK FOR USER QUERY
human_query = input("Human Query: ")


# STEP 3: SIMILARITY SEARCH
search_results = qdrant.similarity_search(human_query, k=3)


# STEP 4: BUILD THE CONTEXT FROM MATCHING CSV ROWS
context = []

for row in search_results:
    row_block = f"""
    CSV Row Content:
    {row.page_content}

    Incident ID:
    {row.metadata.get('incident_id')}
    """
    context.append(row_block)


# STEP 5: SYSTEM PROMPT FOR LLM
SYSTEM_PROMPT = f"""
You are an AI RAG Assistant for DevOps incidents.
You have been provided context retrieved from historical CSV incident data.
Each section includes:
- CSV Row Content
- Incident ID

Answer the user's question only using this provided information.

If the answer is available:
- Explain the likely cause and suggested resolution
- Mention the relevant incident ID(s)
- Treat the rows as historical examples, not proof of the current system state

If the answer is not available:
- State that the answer is beyond the available CSV knowledge base

Data:
{context}
"""


# STEP 6: GENERATE THE LLM RESPONSE
response = client.responses.create(
    model="gpt-5.6-luna",
    input=human_query,
    instructions=SYSTEM_PROMPT,
)


# STEP 7: PRINT AI RESPONSE
print(response.output_text)
