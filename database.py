import mysql.connector
 
db = mysql.connector.connect(
    host = "sql4.freemysqlhosting.net",
    user = "sql4448314",
    passwd = "zSNdlwGWqY",
    database = 'sql4448314'  
)

mycursor = db.cursor(buffered=True)

'''

mycursor.execute('DESCRIBE employer')


for x in mycursor:
  print(x)
'''
