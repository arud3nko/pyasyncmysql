"""

Модуль, реализующий асинхронное взаимодействие с БД MySQL

"""


from typing import Any

import aiomysql

from aiomysql.connection import Error
from deprecated.sphinx import deprecated
from pypika import Query, Table, Order

from .config import DBConfig


class DB:
    """

    Класс для асинхронной работы с БД MySQL.
    Соединение реализуется с помощью асинхронной библиотеки aiomysql
    Для генерации запросов используется неблокирующий pypika

    :param conf: Параметры БД
    """
    def __init__(self, conf: DBConfig):
        self.host = conf.host
        self.port = conf.port
        self.username = conf.username
        self.password = conf.password
        self.database = conf.database

        self.connection = None
        self.cursor = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def select(self,
                     table: str,
                     *args:      Any) -> list:
        """

        Выборка полей из таблицы
            > SELECT (...) FROM table
        Если не указаны поля - полная выборка из таблицы
            > SELECT * FROM table

        :param table: Таблица
        :param args: Поля для выборки, если не указаны > SELECT *
        :return: Выборка
        """
        table = Table(table)
        if args:
            q = Query.from_(table).select(*[getattr(table, arg) for arg in args])
        else:
            q = Query.from_(table).select(table.star)
        result = await self.__execute_query(q.get_sql(quote_char=None))
        return result

    async def select_where(self,
                           table:  str,
                           where_cond:  ...,
                           where_value: ...) -> list | None:
        """

        Выборка по условию
            > SELECT * FROM table WHERE where_cond = where_value

        :param table: Таблица
        :param where_cond: Параметр условия
        :param where_value: Значение параметра

        :return: Выборка, если не найдено - None
        """
        table = Table(table)
        q = Query.from_(table).select(table.star).where(getattr(table, where_cond) == where_value)
        result = await self.__execute_query(q.get_sql(quote_char=None))
        if not result:
            return None
        return result

    async def select_where_two(self,
                               table:   str,
                               where_cond:   ...,
                               where_value:  ...,
                               second_cond:  ...,
                               second_value: ...) -> list | None:
        """

        Выборка по двум условиям
            > SELECT * FROM table WHERE where_cond = where_value AND second_cond = second_value

        :param table: Таблица
        :param where_cond: Параметр 1 условия
        :param where_value: Значение 1 параметра
        :param second_cond: Параметр 2 условия
        :param second_value: Значение 2 параметра
        :return: Выборка, если не найдено - None

        TODO: Убрать костыль, сделать через **kwargs
        """
        table = Table(table)
        q = Query.from_(table).select(table.star).where(getattr(table, where_cond) == where_value
                                                        and
                                                        getattr(table, second_cond) == second_value)
        result = await self.__execute_query(q.get_sql(quote_char=None))
        if not result:
            return None
        return result

    async def insert(self,
                     table: str,
                     **kwargs:   Any) -> int:
        """

        Добавление строки в таблицу
            > INSERT INTO table VALUES (...)

        :param table: Таблица
        :param kwargs: Пары ключ-значение (имя_столбца=значение)
        :return: Возвращает id строки, если строка успешно добавлена
        """
        q = Query.into(Table(table)).columns(*kwargs.keys()).insert(*kwargs.values())
        await self.__execute_query(q.get_sql(quote_char=None))
        return self.cursor.rowcount

    async def delete(self,
                     table:  str,
                     where_cond:  ...,
                     where_value: ...) -> None:
        """

        Удаление строки из таблицы по условию
            > DELETE FROM table WHERE where_cond = where_value

        :param table: Название таблицы
        :param where_cond: Параметр условия
        :param where_value: Значение параметра
        :return:
        """
        table = Table(table)
        q = Query.from_(table).delete().where(getattr(table, where_cond) == where_value)
        await self.__execute_query(q.get_sql(quote_char=None))
        return

    async def update(self,
                     table:  str,
                     where_cond:  ...,
                     where_value: ...,
                     **kwargs) -> None:
        """

        Обновляет строку в таблице по условию
            > UPDATE table SET (...) WHERE where_cond = where_value

        :param table: Название таблицы
        :param where_cond: Параметр условия
        :param where_value: Значение параметра
        :return:
        """
        table = Table(table)
        q = Query.update(table).where(getattr(table, where_cond) == where_value)
        for key, value in kwargs.items():
            q = q.set(key, value)
        await self.__execute_query(q.get_sql(quote_char=None))
        return

    @deprecated(reason="Не используется после версии 1.1, так как после insert возвращается _id", version="1.1")
    async def get_last_row_id(self,
                              table: str):
        """

        Получение _id последней строки

        :param table: Таблица
        :return: _id последней строки
        """
        table = Table(table)
        q = Query.from_(table).select('id').orderby('id', order=Order.desc).limit(1)
        result = await self.__execute_query(q.get_sql(quote_char=None))
        if not result:
            return 1
        return int(result[0][0])

    async def __connect(self) -> None:
        """

        Установка соединения с БД

        :return:
        """
        self.connection = await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            db=self.database,
            charset='utf8'
        )
        return

    async def __disconnect(self) -> None:
        """

        Разрыв соединения с БД

        :return:
        """
        self.connection.close()
        return

    async def __execute_query(self,
                              query: str) -> Any:
        """

        Выполнение запроса

        :param query: Строка запроса
        :return: Результат
        """
        try:
            await self.__connect()
            self.cursor = await self.connection.cursor()
            await self.cursor.execute(query)
            result = await self.cursor.fetchall()
            await self.connection.commit()
            return result
        except Error:
            raise
        finally:
            await self.__disconnect()


if __name__ == '__main__':
    pass
