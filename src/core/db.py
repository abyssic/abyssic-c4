import sqlite3
import queue

from utils.utils import Utils

class PoolConn:
    def __init__(self, db_path, max_connections=5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.pool = queue.Queue(max_connections)
        self.__create_connections()

    def __create_connections(self):
        for _ in range(self.max_connections):
            try:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                self.pool.put(conn)

                Utils.colorize(f'Connected to database {self.db_path}')
            except sqlite3.Error as e:
                Utils.colorize(f'Error connecting to database {self.db_path}: {e}', 'error')

    def get_connection(self):
        return self.pool.get()

    def release_connection(self, conn):
        self.pool.put(conn)

    def close_all_connections(self):
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()

class DbMan:
    def __init__(self, db_path, max_connections=5):
        self.connection_pool = PoolConn(db_path, max_connections)

    def __enter__(self):
        self.connection = self.connection_pool.get_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection_pool.release_connection(self.connection)

    def execute_query(self, query, params=None, fetch=False):
        if not self.connection:
            Utils.colorize('No connection available', 'error')
            return None

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                result = cursor.fetchall()
                return result

            self.connection.commit()
            return True

        except sqlite3.Error as e:
            self.connection.rollback()
            Utils.colorize(f'Error executing query: {e}', 'error')
            return False

    def create(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.values()])
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        params = tuple(data.values())
        return self.execute_query(query, params)

    def read(self, table, condition=None):
        query = f'SELECT * FROM {table}'
        params = None
        if condition:
            query += f' WHERE {condition}'
        return self.execute_query(query, params, fetch=True)

    def update(self, table, data, condition):
        set_values = ', '.join([f'{key} = ?' for key in data.keys()])
        query = f'UPDATE {table} SET {set_values} WHERE {condition}'
        params = tuple(data.values())
        return self.execute_query(query, params)

    def delete(self, table, condition):
        query = f'DELETE FROM {table} WHERE {condition}'
        return self.execute_query(query)
