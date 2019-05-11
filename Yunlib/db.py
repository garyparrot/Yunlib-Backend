import psycopg2

def db_action(func):
    """Decorator function to make sure the connect is up running"""

    def test_connection(self):
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT true")
            return cursor.fetchone()[0] == True

    def wrapper(*args, **kargs):
        self = args[0]
        if self._connection == None:
            self.setup_connection()
        Ok = False
        for i in range(5):
            try:
                Ok = test_connection(self)
            except psycopg2.OperationalError as e:
                self.setup_connection()
            except Exception as err:
                raise err
        if not Ok:
            raise Exception("Cannot setup connection to database")

        return func(*args,**kargs)

    return wrapper

class db:
    """Yunlib database manager"""

    def __init__(self, dbname, user, password, host, port):
        self._config = {}
        self._config["dbname"] = dbname
        self._config["user"] = user
        self._config["password"] = password
        self._config["host"] = host
        self._config["port"] = port
        self._connection = None
        self.userinfo = db_userinfo(self.get_connection)

    @db_action
    def get_connection(self):
        return self._connection

    def setup_connection(self):
        self._connection = psycopg2.connect(**self._config)

class db_userinfo:

    def __init__(self, connection_getter):
        self.get_connection = connection_getter

    def querys(self):
        with self.get_connection().cursor() as c:
            c.execute("SELECT * FROM userinfo")
            return c.fetchall()

    def insert(self,user_id, notify = True, note = None):
        with self.get_connection().cursor() as c:
            c.execute('INSERT INTO userinfo (user_id, notify, note) VALUES (%s, %s, %s)', [user_id, notify, note])
        self.get_connection().commit()

    def query_by_id(self,user_id):
        with self.get_connection().cursor() as c:
            c.execute('SELECT * FROM userinfo WHERE user_id = %s', [user_id])
            return c.fetchone()

    def update_notify(self,user_id, value):
        with self.get_connection().cursor() as c:
            c.execute('UPDATE userinfo SET notify = %s WHERE user_id = %s', [value, user_id])
        self.get_connection().commit()

    def is_notify_on(self,user_id):
        with self.get_connection().cursor() as c:
            c.execute('SELECT notify FROM userinfo WHERE user_id = %s', [user_id])
            return c.fetchone()[0]

    def delete(self,user_id):
        with self.get_connection().cursor() as c:
            c.execute('DELETE FROM userinfo WHERE user_id = %s', [user_id])
        self.get_connection().commit()

