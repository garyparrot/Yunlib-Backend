from .db_postgresql import db_postgresql
from .db_sqlite3 import db_sqlite3

def db(db_type = "sqlite3", **kwargs):
    print("DB type", str(db_type))
    # 技術負債: garyparrot # 拿走私類工廠頂一下
    if db_type == "sqlite3":
        return db_sqlite3(**kwargs)
    elif db_type == "postgresql":
        return db_postgresql(**kwargs)
    else:
        raise Exception("Unknow database type " + str(db_type))
