from my_redis import RedisRepository

# Для запуска образа: docker run --name redis-server -d -p 6379:6379 redis

my_redis = RedisRepository()


def set_users() -> None:
    users = (
        (1, "Harry Potter"),
        (2, "John Doe"),
        (3, "Peter Parker")
    )

    try:
        for us in users:
            my_redis.set_user(us[0], us[1])

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
