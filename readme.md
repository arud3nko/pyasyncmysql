
# pyasyncmysql

Данная библиотека написана для упрощения асинхронной работы с базой данных MySQL и используется мною в небольших проектах, в которых можно обойтись без SQLAlchemy.
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

Больше примеров можно найти в директории examples

## Documentation

```python
async def select(*args:    ...,
                 table:    str,
                 **kwargs: ...) -> tuple | None:
    """

    Выборка
        > SELECT (...) FROM table WHERE (...)

    :param table: Таблица
    :param args: Поля для выборки, если не указано - выборка всех полей
    :param kwargs: Пары ключ=значение для условий, если не указано - выборка всей таблицы
    :return: Выборка, если выборка не содержит строк - None
    """

async def insert(table:   str,
                **kwargs: ...) -> int:
    """

    Добавление строки в таблицу
        > INSERT INTO table VALUES (...)

    :param table: Таблица
    :param kwargs: Пары ключ-значение (имя_столбца=значение)
    :return: Возвращает id строки, если строка успешно добавлена
    """

async def delete(table:    str,
                 **kwargs: ...) -> None:
    """

    Удаление строки из таблицы по условию
        > DELETE FROM table WHERE (...)

    :param table: Название таблицы
    :param kwargs: Пары ключ=значение для условий, если не указано - удаление всех строк таблицы
    :return:
    """

async def update(table:    str,
                 **kwargs: ...) -> None:
    """

    Обновляет строку в таблице
        > UPDATE table SET (...) WHERE (where_...)

    Если условия не указаны, будут обновлены все строки

    :param table: Название таблицы
    :param kwargs: С префиксом where_ > пары ключ=значение для условий
                   Без префикса > поля, которые будут обновлены
    :return:
    """    

```


## Authors

- [@arud3nko](https://www.github.com/arud3nko)


## License

[GNU GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html)

