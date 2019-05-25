import resource
from Yunlib.db import db as db
from Yunlib.resource import ConfigLoader
import Yunlib.resource as resource

def init(filename):
    initPostgresql(filename)
    initSqlite3(filename)

def initPostgresql(filename):
    cloader = ConfigLoader(filename)
    access = cloader.db_access_config()
    access['db_type'] = 'postgresql'
    database = db(**access)
    print(database)

    with database.get_connection() as conn:
        with conn.cursor() as cursor:
            print("Try to remove table", resource.DB_USERINFO_TNAME)    
            cursor.execute("DROP TABLE IF EXISTS userinfo")

            print("Create table", resource.DB_USERINFO_TNAME)
            cursor.execute("""CREATE TABLE userinfo
                              (
                                  id SERIAL PRIMARY KEY NOT NULL,
                                  user_id TEXT NOT NULL UNIQUE,
                                  notify BOOLEAN NOT NULL DEFAULT true,
                                  note TEXT
                              );""")
        conn.commit()

def initSqlite3(filename):
    cloader = ConfigLoader(filename)
    access = cloader.db_access_config()
    access['db_type'] = 'sqlite3'
    database = db(**access)
    print(database)

    with database.get_connection() as conn:
        cursor = database.get_connection().cursor()
        print("Try to remove table", resource.DB_USERINFO_TNAME)    
        cursor.execute("DROP TABLE IF EXISTS userinfo")

        print("Create table", resource.DB_USERINFO_TNAME)
        cursor.execute("""CREATE TABLE userinfo
                          (
                              id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                              user_id TEXT NOT NULL UNIQUE,
                              notify BOOLEAN NOT NULL DEFAULT true,
                              note TEXT
                          );""")
        conn.commit()

if __name__ == "__main__":
    filename = input("Path to resource.ini: ")
    initPostgresql(filename)
    initSqlite3(filename)
