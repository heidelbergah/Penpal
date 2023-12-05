import mysql.connector

def convert_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
        
try:
    connection = mysql.connector.connect(host='loaclhost', database='database_name', username='username', password='password')
    
    cursor = connection.cursor()
    
    query = """ SELECT * from images """
    
    cursor.execute(query)
    records = cursor.fetchall()
    for row in records:
        file = row[0]
        convert_data(file, "C:\Desktop\images\image.png")
        
    print("Successfully Retrieved")
    
except mysql.connector.Error as error:
    print(format(error))
    
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Closed")