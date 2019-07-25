import mysql.connector
from db import DbConn



# TimeTableRecordModel :- No GET,POST,PUT,DELETE Allowed Here. For GET POST PUT DELETE , go for resource.TTRecord
class TTRecordModel():
    def __init__(self,idtimetable, frombit, fromdoranda, fromxavier, fromlalpur, typeofbus, typeofday, busno, isRunning, hasdeparted):
        self.idtimetable = idtimetable
        self.frombit     = str(frombit)     if str(frombit)!="None" else None
        self.fromdoranda = str(fromdoranda) if str(fromdoranda)!="None" else None
        self.fromxavier  = str(fromxavier)  if str(fromxavier) !="None" else None
        self.fromlalpur  = str(fromlalpur)  if str(fromlalpur) !="None" else None
        self.typeofbus = typeofbus.decode() if isinstance(typeofbus,bytearray) else typeofbus
        self.typeofday = typeofday.decode() if isinstance(typeofday,bytearray) else typeofday
        self.busno = busno.decode() if isinstance(busno,bytearray) else busno
        self.isRunning = isRunning
        self.hasdeparted= hasdeparted


    def tojson(self):
        jsonRecord = {
            'idtimetable':self.idtimetable,
            'frombit':self.frombit,
            'fromdoranda' : self.fromdoranda,
            'fromxavier'  : self.fromxavier,
            'fromlalpur' : self.fromlalpur,
            'typeofbus' : self.typeofbus,
            'typeofday' : self.typeofday,
            'busno' : self.busno,
            'isRunning' : self.isRunning,
            'hasdeparted' : self.hasdeparted
        }
        return jsonRecord


    @classmethod
    def getAllRecord(cls):
        query = "SELECT * FROM timetable"
        
        cursor = DbConn.connection.cursor(prepared=True)
        cursor.execute(query)
        resultset = cursor.fetchall()
        DbConn.connection.commit()
        cursor.close()
        


        lst = []
        for x in resultset:
            lst.append(cls(*x).tojson())
        return lst
    
    @classmethod
    def getRecordById(cls,idtimetable):
        # query= "SELECT * FROM timetable WHERE frombit = MAKETIME(?,?,?)";
        query = "SELECT * FROM timetable WHERE idtimetable=?"
        
        cursor = DbConn.connection.cursor(prepared=True)
        cursor.execute(query,(idtimetable,))
        resultset = cursor.fetchone()
        DbConn.connection.commit()
        cursor.close()
        
        if resultset:
            result = cls(*resultset)
            return result
        else:
            return None

    def updateStatus(self):
        try:
            query = "UPDATE timetable SET hasdeparted=? , isRunning=? WHERE idtimetable=?"
            
            cursor = DbConn.connection.cursor(prepared=True)
            cursor.execute(query,(self.hasdeparted,self.isRunning,self.idtimetable))
            DbConn.connection.commit()
            cursor.close()
            print("updated")
            return True
        except:
            print("An Error Occured")
            return False
        