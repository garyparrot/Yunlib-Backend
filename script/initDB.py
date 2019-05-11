import resource
from Yunlib.db import db as db
from Yunlib.resource import ConfigLoader
import Yunlib.resource as resource

def init(filename):
    cloader = ConfigLoader(filename)
    database = db(**cloader.db_access_config())

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

if __name__ == "__main__":
    filename = input("Path to resource.ini: ")
    init(filename)
