import asyncio

from pyasyncmysql import DB, DBConfig

TABLE = "users"

config = DBConfig(host="127.0.0.1",
                  port=3306,
                  username="root",
                  password="",
                  database="rsa")


async def update_user_session(username:        str,
                              hashed_password: str) -> None:
    async with DB(conf=config) as db:
        await db.update(table=TABLE,
                        where_username=username,
                        hashed_password=hashed_password)
    return


async def main():
    await update_user_session(username="root", hashed_password="1234567890")


if __name__ == "__main__":
    asyncio.run(main())
