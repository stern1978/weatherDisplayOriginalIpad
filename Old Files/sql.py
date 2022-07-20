import sqlite3

with sqlite3.connect("laundry.db") as connection:
    c = connection.cursor()
#try:
    #print('dropping')
    #c.execute("""DROP TABLE laundry""")

#except:
    print ('creating')
    c.execute("""CREATE TABLE laundry(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount TEXT)""")
    c.execute("INSERT INTO laundry (amount) VALUES (29.10)")

    #c.execute('SELECT id, amount FROM laundry')
    print ('DONE')


