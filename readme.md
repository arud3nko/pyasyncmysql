
# pyasyncmysql

Данный пакет написан для упрощения взаимодействия с базой данных MySQL и используется мною в небольших (и средне-больших) асинхронных проектах, в которых можно обойтись без SQLAlchemy.
Взаимодействие производится асинхронно с использованием asyncio и библиотек:

    - aiomysql > Для взаимодействия с БД
    - pypika   > Для генерирования запросов
    - pydantic > Для валидации параметров БД


## Installation

Установите, клонировав репозиторий и установив зависимости из файла requirements.txt
    
## Usage

```python
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
```


## Authors

- [@arud3nko](https://www.github.com/arud3nko)


## License

[GNU GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html)

