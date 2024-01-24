import asyncio

from pyasyncmysql import DB, DBConfig

TABLE = "users"

config = DBConfig(host="127.0.0.1",
                  port=3306,
                  username="root",
                  password="",
                  database="rsa")


async def insert_rsa_session(username:        str,
                             hashed_password: str) -> None:
    async with DB(conf=config) as db:
        await db.insert(table=TABLE,
                        username=username,
                        hashed_password=hashed_password)


async def main():
    await insert_rsa_session(username="root",
                             hashed_password="17808bf2-8258-4408-835a-0c59b20715f3")

if __name__ == "__main__":
    asyncio.run(main())
