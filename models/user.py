import mysql.connector
from db import DbConn



class UserModel:
    def __init__(self,uid,username,password):
        self.id = uid
        self.username = username.decode() if isinstance(username,bytearray) else None
        self.password = password.decode() if isinstance(password,bytearray) else None
    
    def __str__(self):
        _str= "Username = "+self.username+"\nPassword = "+self.password
        return _str
    
    @classmethod
    def find_by_username(cls,username):
        query = "SELECT * FROM admin WHERE username=?"
        return cls.find_by_param(query,username)

    @classmethod
    def find_by_id(cls,uid):
        query = "SELECT * FROM admin WHERE idadmin=?"
        return cls.find_by_param(query,uid)
    
    @classmethod
    def find_by_param(cls,query,param):
        if(DbConn.connection.is_connected()==False):
            DbConn.connection._open_connection()
        cursor = DbConn.connection.cursor(prepared=True)
        cursor.execute(query,(param,))
        resultset = cursor.fetchone()
        DbConn.connection.commit()
        cursor.close()
        DbConn.connection.close()

        if resultset:
            user = cls(*resultset)
            print(user)
        else:
            user = None
        return user

