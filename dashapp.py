import sqlite3
import sql_loader as sl

con = sqlite3.connect('ABunchOfTrees.db')
cur = con.cursor()

sl.tableInitialize(cur)
sl.databaseInitialize(cur)

con.commit()
con.close()