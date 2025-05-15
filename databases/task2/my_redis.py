import json
import os
import redis
from dotenv import load_dotenv


load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")


class RedisRepository:
    def __init__(self, redis_url: str = 'redis://localhost:6379'):
        self.client = redis.StrictRedis.from_url(redis_url)

    def set_user(self, user_id: int, full_name: str) -> None:
        serialized_data = json.dumps({'full_name': full_name})
        self.client.set(f'user:{user_id}', serialized_data)

    def get_user(self, user_id: int) -> str | None:
        result = self.client.get(f'user:{user_id}')
        if result:
            data = json.loads(result.decode('utf-8'))
            return data.get('full_name')
        return None

    def delete_user(self, user_id: int) -> None:
        self.client.delete(f'user:{user_id}')

