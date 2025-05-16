from my_mongo import MongoTaskRepository
from datetime import datetime

# Дkя запуска mongodb: docker run -d --name my-mongo -p 27017:27017 -v mongo_data:/data/db mongo

tasks = [
        {
            "task_name": "breakfast",
            "task_description": "make breakfast",
            "assignee": "Peter",
            "created_at": datetime.utcnow(),
            "tags": ["home"]
        },
        {
            "task_name": "report",
            "task_description": "write a report",
            "assignee": "Peter",
            "reviewer": "John",
            "created_at": datetime.utcnow(),
            "tags": ["work"]
        },
        {
            "task_name": "call",
            "task_description": "call a partner",
            "assignee": "Anna",
            "created_at": datetime.utcnow(),
            "tags": ["work"]
        }
    ]


if __name__ == "__main__":
    my_mongo = MongoTaskRepository()

    my_mongo.create_task(tasks[0])
    my_mongo.create_task(tasks[1])
    task_id = my_mongo.create_task(tasks[2])

    print("Getting task:", my_mongo.get_task_by_id(task_id))

    del_res = my_mongo.delete_task(task_id)
    if del_res:
        print(f"Task {task_id} was deleted")
    else:
        print(f"Task {task_id} was not deleted")

