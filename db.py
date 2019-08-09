import mysql.connector
#from models.timetable import TTRecordModel



# URL with old password  =
#  mysql://bc658df5e46833:48a9ade6@us-cdbr-iron-east-02.cleardb.net/heroku_219aea5cf37fe0e?reconnect=true

# URL with new password  = 
#  mysql://bc658df5e46833:7ff652b58b56936@us-cdbr-iron-east-02.cleardb.net/heroku_219aea5cf37fe0e?reconnect=true

# DB_HOST = us-cdbr-iron-east-02.cleardb.net
# DB_DATABASE = heroku_219aea5cf37fe0e
# SCHEMA =          heroku_219aea5cf37fe0e
# DB_USERNAME = bc658df5e46833
# DB_PASSWORD = 7ff652b58b56936

# for exporting
# mysqldump -u root -p bitbus > d:\bitbus.sql
# for importing 
# mysql -u bc658df5e46833 -h us-cdbr-iron-east-02.cleardb.net -p heroku_219aea5cf37fe0e < d:\bitbus.sql


#  heroku config:set DATABASE_URL=mysql://bc658df5e46833:48a9ade6@us-cdbr-iron-east-02.cleardb.net/heroku_219aea5cf3                                                       7fe0e?reconnect=true





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
    
    
        
        






