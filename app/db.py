import os
from typing import Dict, List, Tuple

import sqlite3


conn = sqlite3.connect(os.path.join("app/db", "tgbotdb.db"))
cursor = conn.cursor()



def insert_blob(table: str, id_id, blob_data_tuple: tuple):
    try:
        sqlite_insert_blob_query = f"""INSERT INTO {table}
                                  (id, image) VALUES (?, ?)"""

        # Преобразование данных в формат кортежа
        cursor.execute(sqlite_insert_blob_query,(id_id[1], blob_data_tuple[1]))
        conn.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблиу")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def updates(table: str, id_id, column_values: Dict):
    try:
        columns = ', '.join( column_values.keys() )
        values = tuple(column_values.values())
        col = [ (str(i[0]) + '=' + str(i[1])) for i in column_values.items()]
        cols_s=''
        for l in col:
            cols_s=cols_s+str(l)
        placeholders = ", ".join( "?" * len(column_values.keys()) )
        cursor.execute(
            f"UPDATE {table} "
            f"SET {cols_s} "
            f"WHERE id={id_id}"
            )
        conn.commit()
        print(36, id_id, columns, values, cols_s)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor

def close_ses():
    conn.close()

def _init_db():
    """Инициализирует БД"""
    with open("tguser.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='tguser'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()
