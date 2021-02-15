
import MySQLdb

db = MySQLdb.connect("localhost", 'root', 'admin123', 'stockdb', charset='utf8')

cursor = db.cursor()
cursor.execute('select version()')

data = cursor.fetchone()

print('Database version: %s ' %data)

db.close()