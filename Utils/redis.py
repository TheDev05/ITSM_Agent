from dotenv import load_dotenv
import redis
import os

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True,
    username=os.getenv('REDIS_USER'),
    password=os.getenv('REDIS_PASS'),
)
