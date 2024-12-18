import sqlite3
import os

def connect_to_database(db_name):

    db_folder = os.path.join(os.path.dirname(__file__), "../database")
    db_path = os.path.join(db_folder, db_name)

    try:
        os.makedirs(db_folder, exist_ok=True)

        connection = sqlite3.connect(db_path)
        print(f"Conexión exitosa a la base de datos en '{db_path}'")
        return connection
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None
    finally:
        if 'connection' in locals() and connection:
            connection.close()

database_name = "cuywise.sqlite"

if __name__ == "__main__":
    connect_to_database(database_name)
