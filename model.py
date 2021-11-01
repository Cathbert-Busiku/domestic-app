import mysql.connector
 
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = 'domesticworkerdb'  
)

mycursor = db.cursor(buffered=True)


#ycursor.execute("SELECT MAX(accepted) AS maximum FROM users")

#result = mycursor.fetchall()


