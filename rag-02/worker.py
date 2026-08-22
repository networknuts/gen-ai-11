import redis
import ast 
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI 

# SETUP THE AI ENVIRONMENT
load_dotenv()
client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "example_collection"
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# CONNECTION TO THE VECTOR DATABASE
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL
)

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# PULL DATA OUT OF REDIS
queue_name = "rag:requests"

print("WORKER STARTED, WAITING FOR QUERIES.")

while True: 
    queue_name, raw_payload = redis_client.blpop(queue_name)
    payload = ast.literal_eval(raw_payload)
    job_id = payload["job_id"]
    human_query = payload["query"]
    print(f"Processing Query: {job_id}")
    
    # AI RAG CODE
    search_results = qdrant.similarity_search(human_query)
    context = []
    for chunk in search_results:
        chunk_block = f""" 
        Page Content:
        {chunk.page_content}
        Page Number:
        {chunk.metadata.get("page")}
        """
        context.append(chunk_block)
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
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=human_query,
        instructions=SYSTEM_PROMPT
    )
    answer = response.output_text
    redis_client.set(str(job_id),answer,ex=86400)
    print(f"Job: {job_id} completed successfully!")