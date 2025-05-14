from core.models import *
from core.db import engine, Base


def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # try:
    #     with engine.connect() as connection:
    #         print("Подключение успешно!")
    # except Exception as e:
    #     print("Ошибка подключения:", e)
   create_tables()
