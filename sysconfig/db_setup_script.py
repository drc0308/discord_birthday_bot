import sqlite3

con = sqlite3.connect('birthdays.db')
cur = con.cursor()
try:
    cur.execute(
        "CREATE TABLE birthday (user text, date text, username txt)"
    )
    con.commit()
    con.close()
except sqlite3.OperationalError:
    con.close()
