import redis
import uuid 

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# GENERATE PAYLOAD AND UPLOAD TO REDIS
def upload_payload(query):
    job_id = str(uuid.uuid4())
    payload = {
        "job_id": job_id,
        "query": query
    }
    queue_name = "rag:requests"
    redis_client.rpush(queue_name,str(payload))
    return job_id 

# ASK FOR HUMAN QUERY
human_query = input("Human Question: ")

# SEND QUERY TO REDIS VIA UPLOAD_PAYLOAD FUNC
job = upload_payload(human_query)
print("Query sent to Redis successfully!")
print(job)