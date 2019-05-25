import psycopg2

def db_action(func):
    """Decorator function to make sure the connect is up running"""

    def create_userinfo(self):
        cursor = self._connection.cursor()
        cursor.execute("""CREATE TABLE userinfo
                    (
                        id SERIAL PRIMARY KEY NOT NULL,
                        user_id TEXT NOT NULL UNIQUE,
                        notify BOOLEAN NOT NULL DEFAULT true,
                        note TEXT
                    );""")
        self._connection.commit()
        return True

    def test_connection(self):
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.userinfo')")
            if cursor.fetchone()[0] == 'userinfo':
                return True
            else:
                return create_userinfo(self)

    def wrapper(*args, **kargs):
        self = args[0]
        if self._connection == None:
            self.setup_connection()
        Ok = False
        for i in range(5):
            try:
                Ok = test_connection(self)
            except Exception as err:
                self.setup_connection()
                if i == 4:
                    raise err
        if not Ok:
            raise Exception("Cannot setup connection to database")

        return func(*args,**kargs)

    return wrapper

class db_postgresql:
    """Yunlib database manager for PostgreSQL"""

    def __init__(self, dbname, user, password, host, port, **kargs):
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
        """Return the database connection object, the connection is access guarantee"""
        return self._connection

    def setup_connection(self):
        """Setup the connection between server and database"""
        self._connection = psycopg2.connect(**self._config)

class db_userinfo:

    def __init__(self, connection_getter):
        self.get_connection = connection_getter

    def querys(self):
        """
        Query all the userinfo from database.

        :returns: A list of all the userinfo store in database
        """
        
        with self.get_connection().cursor() as c:
            c.execute("SELECT * FROM userinfo")
            return c.fetchall()

    def insert(self,user_id, notify = True, note = None):
        """
        Insert new userinfo.

        :param user_id: The user id for new user
        :param notify: The notification setting for new user
        :param note: The note for new user
        """
        
        with self.get_connection().cursor() as c:
            c.execute('INSERT INTO userinfo (user_id, notify, note) VALUES (%s, %s, %s)', [user_id, notify, note])
        self.get_connection().commit()

    def query_by_id(self,user_id):
        """
        Query userinfo by user id.

        :param user_id: The user id for query
        :returns: A tuple contain specified user's userinfo
        """
        
        with self.get_connection().cursor() as c:
            c.execute('SELECT * FROM userinfo WHERE user_id = %s', [user_id])
            return c.fetchone()

    def update_notify(self,user_id, value):
        """
        Update the notification setting of user by specified user id.

        :param user_id: The user id from specified user
        :param value: The value for notification setting
        """
        
        with self.get_connection().cursor() as c:
            c.execute('UPDATE userinfo SET notify = %s WHERE user_id = %s', [value, user_id])
        self.get_connection().commit()

    def is_notify_on(self,user_id):
        """
        Return a boolean value which indicates the user's notification setting is on.

        :param user_id: The user if for query.
        :returns: A boolean value 
        """
        
        with self.get_connection().cursor() as c:
            c.execute('SELECT notify FROM userinfo WHERE user_id = %s', [user_id])
            return c.fetchone()[0]

    def delete(self,user_id):
        """
        Delete specified userinfo by user id

        :param user_id: The user id of specified user
        """
        
        with self.get_connection().cursor() as c:
            c.execute('DELETE FROM userinfo WHERE user_id = %s', [user_id])
        self.get_connection().commit()

