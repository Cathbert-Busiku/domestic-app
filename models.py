import mysql.connector
 
db = mysql.connector.connect(
    host = "us-cdbr-east-04.cleardb.com",
    user = "b63d65243cd882",
    passwd = "2e0005e6",
    database = 'heroku_75676b5f90d8756'  
)

mycursor = db.cursor(buffered=True)


'''

mycursor.execute('DESCRIBE employer')


for x in mycursor:
  print(x)

from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'bc71a3b40d6715'
app.config['MYSQL_DATABASE_PASSWORD'] = 'c0124eb5'
app.config['MYSQL_DATABASE_DB'] = 'heroku_360389a98465754'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'
mysql.init_app(app)
'''