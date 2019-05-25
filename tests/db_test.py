import unittest, random, string
from Yunlib.resource import ConfigLoader
from Yunlib.db import db


class UnitTestSqlite3(unittest.TestCase):

    def setUp(self):
        self.cloader = ConfigLoader('./resource.ini')
        access = self.cloader.db_access_config()
        access['db_type'] = 'sqlite3'
        self.database = db( **access )

    def test_connection_up(self):
        c =self.database.get_connection().cursor()
        c.execute('SELECT true')
        self.assertTrue(c.fetchone()[0] == True)
        c.execute('SELECT true')
        self.assertFalse(c.fetchone()[0] == False)

    def test_crud(self):
        """Test CRUD"""

        user = { "user_id": "FAKE_USER", "notify" : True, "note" : "TEST" }
        letters = string.ascii_lowercase
        user['user_id'] += ''.join(random.choice(letters) for i in range(5))
        self.database.userinfo.insert(**user)

        query = self.database.userinfo.query_by_id(user['user_id'])
        self.assertTrue(query[1] == user['user_id'])
        self.assertTrue(query[2] == user['notify'])
        self.assertTrue(query[3] == user['note'])

        print(self.database.userinfo.query_by_id(user['user_id']))
        trigger1 = self.database.userinfo.is_notify_on(user['user_id'])
        print(self.database.userinfo.query_by_id(user['user_id']))
        self.assertTrue(self.database.userinfo.is_notify_on(user['user_id']))
        self.database.userinfo.update_notify(user['user_id'], not trigger1)
        self.assertFalse(self.database.userinfo.is_notify_on(user['user_id']))
        print(self.database.userinfo.query_by_id(user['user_id']))
        trigger2 = self.database.userinfo.is_notify_on(user['user_id'])
        print(self.database.userinfo.query_by_id(user['user_id']))
        self.assertFalse(trigger1 == trigger2)

        self.database.userinfo.delete(user['user_id'])

        self.database.userinfo.querys()

class UnitTestPostgresql(unittest.TestCase):

    def setUp(self):
        self.cloader = ConfigLoader('./resource.ini')
        access = self.cloader.db_access_config()
        access['db_type'] = 'postgresql'
        self.database = db( **access )

    def test_connection_up(self):
        with self.database.get_connection().cursor() as c:
            c.execute('SELECT true')
            self.assertTrue(c.fetchone()[0] == True)
        with self.database.get_connection().cursor() as c:
            c.execute('SELECT true')
            self.assertFalse(c.fetchone()[0] == False)

    def test_crud(self):
        """Test CRUD"""

        user = { "user_id": "FAKE_USER", "notify" : True, "note" : "TEST" }
        letters = string.ascii_lowercase
        user['user_id'] += ''.join(random.choice(letters) for i in range(5))
        self.database.userinfo.insert(**user)

        query = self.database.userinfo.query_by_id(user['user_id'])
        self.assertTrue(query[1] == user['user_id'])
        self.assertTrue(query[2] == user['notify'])
        self.assertTrue(query[3] == user['note'])

        print(self.database.userinfo.query_by_id(user['user_id']))
        trigger1 = self.database.userinfo.is_notify_on(user['user_id'])
        print(self.database.userinfo.query_by_id(user['user_id']))
        self.assertTrue(self.database.userinfo.is_notify_on(user['user_id']))
        self.database.userinfo.update_notify(user['user_id'], not trigger1)
        self.assertFalse(self.database.userinfo.is_notify_on(user['user_id']))
        print(self.database.userinfo.query_by_id(user['user_id']))
        trigger2 = self.database.userinfo.is_notify_on(user['user_id'])
        print(self.database.userinfo.query_by_id(user['user_id']))
        self.assertFalse(trigger1 == trigger2)

        self.database.userinfo.delete(user['user_id'])

        self.database.userinfo.querys()

if __name__ == "__main__":
    unittest.main()
