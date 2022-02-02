import sqlite3

class Database():
    def _db_operation(func):
        def wrapped(self, *args):
            con = sqlite3.connect(self.filename)
            self.cur = con.cursor()
            try:
                result = func(self, *args)
            except:
                result = None
            finally:
                con.commit()
                con.close()
            return result
        return wrapped

    def __init__(self, filename):
        self.filename = filename
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='purchases'")
        if not cur.fetchone():
            cur.execute("CREATE TABLE purchases (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, name TEXT, price REAL)")
        con.commit()
        con.close()

    @_db_operation
    def c_add(self, category, name, price):
        self.cur.execute("INSERT INTO purchases (date, category, name, price) VALUES (CURRENT_DATE, '{0}', '{1}', {2})".format(category, name, price))

    @_db_operation
    def c_remove(self, id):
        self.cur.execute("DELETE FROM purchases WHERE id = {0}".format(id))

    @_db_operation
    def c_list(self, category = None):
        val_list = []
        if category:
            for row in self.cur.execute("SELECT * FROM purchases WHERE category='{0}' ORDER BY date".format(category)):
                val_list.append(row)
        else:
            for row in self.cur.execute("SELECT * FROM purchases ORDER BY date"):
                val_list.append(row)
        return val_list

    @_db_operation
    def c_sum(self, start_date = None, end_date = None, category = None):
        self.cur.execute("SELECT sum(price) FROM purchases ORDER BY date")
        val_sum = self.cur.fetchone()[0]
        return val_sum

