import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user="root",          
    password="Withi123!",
    database="classicmodels"
)

cursor = connection.cursor()


cursor.execute("SELECT * FROM customers")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
connection.close()

with open('Test.txt','w') as f:
    for row in rows:
     f.writelines(f'{row}\n') 
    
