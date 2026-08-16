from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI 

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "example_collection"
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# STEP 1: CONNECT TO VECTOR DATABASE
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL
)

# STEP 2: ASK FOR USER QUERY
human_query = input("Human Query: ")

# STEP 3: SIMILARITY SEARCH
search_results = qdrant.similarity_search(human_query)

# STEP 4: BUILDING THE CHUNKS

context = []


for chunk in search_results:
    chunk_block = f""" 
    Page Content:
    {chunk.page_content}
    Page Number:
    {chunk.metadata.get("page")}
    """
    context.append(chunk_block)

# STEP 5: SYSTEM PROMPT FOR LLM

SYSTEM_PROMPT = f"""
You are an AI RAG Assistant.
You have been provided context extracted from PDF document(s).
Each section includes:
- Page Content
- Page Number

Answer the user's question only using this provided information.
If the answer is available:
- Respond from only the data you have
- Mention the relevant page number(s) from where the data came from

If the answer is not available:
- State to user that the answer is beyond your knowledge base

Data:
{context}
"""

# STEP 6: GENERATE THE LLM RESPONSE
response = client.responses.create(
    model="gpt-5.6-luna",
    input=human_query,
    instructions=SYSTEM_PROMPT
)

# STEP 7: PRINT AI RESPONSE
print(response.output_text)