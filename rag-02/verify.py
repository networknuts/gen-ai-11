import redis

# CONNECT TO REDIS

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

job_id = "2ab4da4b-c00a-440c-b7b5-52454b54dcb9"

answer = redis_client.get(job_id)
print(answer)