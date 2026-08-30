import csv

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


# ENVIRONMENT VARIABLES
load_dotenv()
CSV_FILE_PATH = "data/devops_incidents.csv"
EMBEDDING_MODEL = "text-embedding-3-large"
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "csv_incidents_collection"


# STEP 1: LOAD THE CSV DATA
csv_documents = []

with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        # Every CSV row becomes one searchable LangChain Document.
        row_content = f"""
        Incident ID: {row['incident_id']}
        Title: {row['title']}
        Service: {row['service']}
        Environment: {row['environment']}
        Severity: {row['severity']}
        Symptoms: {row['symptoms']}
        Root Cause: {row['root_cause']}
        Resolution: {row['resolution']}
        Tags: {row['tags']}
        """

        document = Document(
            page_content=row_content,
            metadata={
                "incident_id": row["incident_id"],
                "title": row["title"],
                "service": row["service"],
                "environment": row["environment"],
                "severity": row["severity"],
            },
        )
        csv_documents.append(document)

print(f"CSV LOADED SUCCESSFULLY: {len(csv_documents)} ROWS")


# STEP 2: CHUNKING STRATEGY
# A CSV row is already a small, meaningful unit, so each row is one chunk.
chunked_data = csv_documents
print("ONE CSV ROW = ONE CHUNK")


# STEP 3: EMBEDDING STRATEGY
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)


# STEP 4: STORE CSV ROWS IN VECTOR DATABASE
qdrant = QdrantVectorStore.from_documents(
    chunked_data,
    embeddings,
    url=QDRANT_URL,
    prefer_grpc=False,
    collection_name=QDRANT_COLLECTION_NAME,
)

print("CSV DATA SAVED TO VECTOR DATABASE")
