import asyncio

from pyasyncmysql import DB, DBConfig

TABLE = "users"

config = DBConfig(host="127.0.0.1",
                  port=3306,
                  username="root",
                  password="",
                  database="rsa")


async def select_user_session(username:        str,
                              hashed_password: str) -> tuple | None:
    async with DB(conf=config) as db:
        session = await db.select("id",
                                  "username",
                                  table=TABLE,
                                  username=username,
                                  hashed_password=hashed_password)

    return session


async def main():
    result = await select_user_session(username="root", hashed_password="17808bf2-8258-4408-835a-0c59b20715f3")
    print(result)  # ((13, 'root'),)


if __name__ == "__main__":
    asyncio.run(main())
