from my_redis import RedisRepository
from collections import namedtuple

# Для запуска образа: docker run --name redis-server -d -p 6379:6379 redis

my_redis = RedisRepository()


def set_users() -> None:
    User = namedtuple('User', ['id', 'name'])
    users = (
        User(1, "Harry Potter"),
        User(2, "John Doe"),
        User(3, "Peter Parker")
    )

    try:
        for us in users:
            my_redis.set_user(us.id, us.name)

        print("Users set")
    except Exception as e:
        print("Error during setting users:", e)


def get_one_user(id: int) -> str | None:
    try:
        result = my_redis.get_user(id)

        return result
    except Exception as e:
        print("Error during getting user:", e)


def delete_one_user(id: int) -> None:
    try:
        my_redis. delete_user(id)

    except Exception as e:
        print("Error during deleting user:", e)


if __name__ == "__main__":
    set_users()
    print(get_one_user(2))
    delete_one_user(3)
