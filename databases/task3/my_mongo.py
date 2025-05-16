from typing import List

from bson import ObjectId
from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv()
mongo_url = os.getenv("MONGO_URL")


class MongoTaskRepository:
    def __init__(self, url: str = mongo_url) -> None:
        try:
            self._client = MongoClient(url)
            self._db = self._client.my_db
            print("Successfully connected to db.")
        except Exception as e:
            print("Error during connecting to db:", e)

    @property
    def db(self):
        return self._db

    def create_task(self, data: dict) -> str:
        try:
            task_id = self._db.tasks.insert_one(data).inserted_id
            if not task_id:
                raise ValueError("Task was not created")
            return task_id
        except Exception as e:
            print("Error during creating task:", e)

    def get_task_by_id(self, task_id: str) -> dict | None:
        try:
            task = self._db.tasks.find_one({"_id": task_id})
            if not task:
                raise ValueError("Task was not created")
            return task
        except Exception as e:
            print("Error during getting task:", e)

    def delete_task(self, task_id: str) -> bool:
        try:
            result = self.db.tasks.delete_one({"_id": ObjectId(task_id)})
            return result.deleted_count > 0
        except Exception as e:
            print("Error during deleting task:", e)

    def aggregate_by_tags(self) -> List[dict]:
        try:
            pipeline = [
                {"$unwind": "$tags"},
                {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            ]
            result = self.db.tasks.aggregate(pipeline)
            return list(result)
        except Exception as e:
            print("Error during aggregating task:", e)
