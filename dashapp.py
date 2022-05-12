import sqlite3
import sql_loader as sl

con = sqlite3.connect('ABunchOfTrees.db')
cur = con.cursor()

sl.sqlInitialize(cur)
sl.dataInitialization(cur)

con.commit()
con.close()