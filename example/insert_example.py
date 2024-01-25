import asyncio

from pyasyncmysql import DB, DBConfig

TABLE = "users"

config = DBConfig(host="127.0.0.1",
                  port=3306,
                  username="root",
                  password="",
                  database="rsa")


async def insert_rsa_session(username:        str,
                             hashed_password: str) -> int:
    async with DB(conf=config) as db:
        _id = await db.insert(table=TABLE,
                              username=username,
                              hashed_password=hashed_password)

        return _id


async def main():
    last_row_id = await insert_rsa_session(username="root",
                                           hashed_password="17808bf2-8258-4408-835a-0c59b20715f3")
    print(last_row_id)  # 1


if __name__ == "__main__":
    asyncio.run(main())
