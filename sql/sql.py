import sqlite3

class database():
    def __init__(self, filename):
        self.filename = filename
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='purchases'")
        if not cur.fetchone()[0] == 1:
            cur.execute("CREATE TABLE purchases (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, name TEXT, price REAL)")
        con.commit()
        con.close()

    def add(self, category, name, price):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        #print("INSERT INTO purchases(date, category, name, price) VALUES (CURRENT_DATE, {0}, {1}, {2})".format(category, name, price))
        cur.execute("INSERT INTO purchases (date, category, name, price) VALUES (CURRENT_DATE, '{0}', '{1}', {2})".format(category, name, price))
        con.commit()
        con.close()

    def remove(self, id):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute("DELETE FROM purchases WHERE id = {0}".format(id))
        con.commit()
        con.close()

    def list(self, category = None):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        list = []
        for row in cur.execute("SELECT * FROM purchases ORDER BY date"):
            list.append(row)
        con.close()
        return list

    def sum(self, start_date = None, end_date = None, category = None):
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        sum = 0
        for row in cur.execute("SELECT price FROM purchases ORDER BY date"):
           sum += row[0]
        return sum

