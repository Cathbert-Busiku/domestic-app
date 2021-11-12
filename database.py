import mysql.connector
 
db = mysql.connector.connect(
    host = "sql11.freemysqlhosting.net",
    user = "sql11450667",
    passwd = "BGLNL3Ead7",
    database = '	sql11450667'  
)
                                      
mycursor = db.cursor(buffered=True)


# mycursor.execute('DESCRIBE employer')


# for x in mycursor:
#    print(x)

