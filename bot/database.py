import mysql.connector

class Database():
    """docstring for Database"""
    def __init__(self):
        super(Database, self).__init__()
        self.host = "localhost"
        self.user = "root"
        self.passwd = ""
        self.db = "raveagleBot"
        self.c = None

    def connect(self):
        if not self.c:
            try:
                self.c = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.passwd,
                    database=self.db)
            except Exception as e:
                raise e

    def close(self):
        if not self.c:
            self.c.close()
            self.c = None

    def get(self, table):
        if not self.c:
            self.connect()
        cursor = self.c.cursor()
        sql = "SELECT * FROM " + table
        cursor.execute(sql)
        return cursor.fetchall()

    def get_where(self, table, args):
        if not self.c:
            self.connect()
        cursor = self.c.cursor()
        sql = "SELECT * FROM " + table + " WHERE "
        for key in args.keys():
            sql += key + " = %s, "
        sql = sql[:-2]
        cursor.execute(sql, tuple(args.values()))
        return cursor.fetchall()

    def insert(self, table, args):
        if not self.c:
            self.connect()
        cursor = self.c.cursor()
        sql = "INSERT INTO " + table + " (id, is_bot, first, last, username) VALUES (%s, %s, %s, %s, %s)"
        val = tuple(args.values())
        cursor.execute(sql, val)
        self.c.commit()
        return cursor.rowcount

if __name__ == '__main__':
    d = Database()
    data = {
        'id':32,
        'is_bot':1,
        'first':"args.first_name",
        'last':None,
        'username':None
    }
    d.insert("user", data)