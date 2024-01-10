import pandas as pd
import sqlite3
from sqlite3 import Error


def materials():
    """
    Свойства материалов.

    :return: Бетон, арматурная сталь
    """
    path = 'materials.db'  # База данных материалов
    con = None  # Соединение с базой данных
    try:
        con = sqlite3.connect(path)
        print(f"Соединение с SQLite DB '{path}' успешно !")
    except Error as e:
        print(f"Случилась ошибка '{e}'")
    finally:
        concrete = pd.read_sql(f"SELECT * FROM '{'concrete'}';", con, index_col='param', coerce_float=True)
        print(f"Таблица '{'concrete'}' загружена:")
        print(concrete)
        steel = pd.read_sql(f"SELECT * FROM '{'steel'}';", con, index_col='param', coerce_float=True)
        print(f"Таблица '{'steel'}' загружена:")
        print(steel)
        con.close()
        return concrete, steel
