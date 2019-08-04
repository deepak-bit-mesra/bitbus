import mysql.connector
#from models.timetable import TTRecordModel


class DbConn():
    
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='bitbus'
    )

    # connection = mysql.connector.connect(
    #     host='us-cdbr-iron-east-02.cleardb.net',
    #     user='bc658df5e46833',
    #     passwd='7ff652b58b56936',
    #     database='heroku_219aea5cf37fe0e'
    # )
    
    
        
        






