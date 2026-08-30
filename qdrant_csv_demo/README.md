# RAG with CSV Data and Qdrant

This example intentionally follows the same structure as the customer's existing PDF RAG lesson:

| Existing PDF lesson | This CSV lesson |
|---|---|
| Load a PDF | Load a CSV with `csv.DictReader` |
| Split PDF text into chunks | Treat each CSV row as one chunk |
| Create OpenAI embeddings | Create OpenAI embeddings |
| Save chunks in Qdrant | Save CSV rows in Qdrant |
| Retrieve matching pages | Retrieve matching incident rows |
| Cite page numbers | Cite incident IDs |

The dataset contains 24 realistic DevOps incidents covering Kubernetes, Linux, databases, networking, CI/CD, caches, queues, and observability.

## Files

- `data/devops_incidents.csv`: Sample data used for the similarity-search demo.
- `ingestion.py`: Loads CSV rows, converts them to LangChain Documents, creates embeddings, and stores them in Qdrant.
- `retrieval.py`: Accepts a user question, retrieves similar CSV rows, and generates a grounded answer.
- `compose.yaml`: Runs Qdrant locally on port `6333`.
- `.env.example`: OpenAI API key template.

## Setup

Use Python 3.11 or newer. From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your key to `.env`:

```bash
OPENAI_API_KEY="your_api_key_here"
```

## Step 1: Start Qdrant

Docker Compose:

```bash
docker compose up -d
```

Podman Compose can also use the same file:

```bash
podman compose up -d
```

Qdrant will be available at `http://localhost:6333`. Its dashboard is available at `http://localhost:6333/dashboard`.

## Step 2: Ingest the CSV

```bash
python ingestion.py
```

Expected output:

```text
CSV LOADED SUCCESSFULLY: 24 ROWS
ONE CSV ROW = ONE CHUNK
CSV DATA SAVED TO VECTOR DATABASE
```

The important teaching point is this line in `ingestion.py`:

```python
document = Document(
    page_content=row_content,
    metadata={"incident_id": row["incident_id"]},
)
```

`page_content` is embedded for similarity search. `metadata` is stored with the vector and returned with the matching row.

Run ingestion once for the demo. Running it again adds another copy of the same CSV records to the existing collection.

## Step 3: Ask a Question

```bash
python retrieval.py
```

Example questions:

```text
Human Query: My Kubernetes pods restart with exit code 137
Human Query: Why is Nginx unable to bind to port 80?
Human Query: The website returns 502 after changing the application port
Human Query: Terraform says that the remote state is locked
```

The retrieval script follows the same seven steps as the previous lesson:

1. Connect to Qdrant.
2. Ask for a human query.
3. Run similarity search.
4. Build context from matching CSV rows.
5. Create the grounded system prompt.
6. Generate the model response.
7. Print the answer.

## CSV Columns

| Column | Meaning |
|---|---|
| `incident_id` | Source ID used in the generated answer |
| `title` | Short incident summary |
| `service` | Affected service |
| `environment` | Production or staging |
| `severity` | Incident severity |
| `symptoms` | Observable failure behavior |
| `root_cause` | Historical root cause |
| `resolution` | Historical remediation |
| `tags` | Extra search vocabulary |

## How the RAG Flow Works

```text
devops_incidents.csv
        ↓
each row becomes a LangChain Document
        ↓
OpenAI text-embedding-3-large
        ↓
Qdrant collection: csv_incidents_collection
        ↓
similarity_search(user question)
        ↓
top 3 incident rows become prompt context
        ↓
GPT-5.6 Luna generates a cited answer
```
