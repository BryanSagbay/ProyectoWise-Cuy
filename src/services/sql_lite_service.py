import sqlite3
import os

class SQLiteService:
    def __init__(self, db_name="cuywise.sqlite"):

        self.db_folder = os.path.join(os.path.dirname(__file__), "../database")
        self.db_path = os.path.join(self.db_folder, db_name)

        os.makedirs(self.db_folder, exist_ok=True)

        self.connection = self.connect_to_database()

    def connect_to_database(self):
        try:
            connection = sqlite3.connect(self.db_path)
            print(f"Conexión exitosa a la base de datos: {self.db_path}")
            return connection
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def create_table(self):

        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS data_cuy (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        image_path TEXT NOT NULL,
                        weight REAL NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                """)
                self.connection.commit()
                print("Tabla 'data_cuy' creada o ya existente.")
            except sqlite3.Error as e:
                print(f"Error al crear la tabla: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":

    sqlite_service = SQLiteService()
    sqlite_service.create_table()
    sqlite_service.close_connection()
