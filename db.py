import mysql.connector
#from models.timetable import TTRecordModel


class DbConn():
    
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='bitbus'
    )
    
    
        
        






