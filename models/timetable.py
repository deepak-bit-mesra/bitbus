import mysql.connector
from db import DbConn
from datetime import date,datetime,time

# def loadHome():
#     today = date.today()
#     # days  =["Monday","Tuesday","Wednesday","Thrusday","Friday","Saturday","Sunday"]
#     # datestr = "\nDate"+str(today) +"\nDay "+str(today.day)+"\nWeekDay "+days[(today.weekday())] 
#     # weekday = days[(today.weekday())]
#     mon = "Mon-Fri"
#     sun = "Sun"
#     sat = "sat"
#     week = [mon,mon,mon,mon,mon,sat,sun];
#     weekday = week[(today.weekday())]
#     jsonArr = TTRecordModel.getRecordByWeekDay()
#     return jsonArr;







    


# TimeTableRecordModel :- No GET,POST,PUT,DELETE Allowed Here. For GET POST PUT DELETE , go for resource.TTRecord
class TTRecordModel():
    listOfHolidays = ["Tue Jan 01 2019", "Tue Jan 15 2019", "Sat Jan 26 2019", "Sun Feb 10 2019", "Mon Mar 04 2019", "Thu Mar 21 2019", "Mon Apr 08 2019", "Sat Apr 13 2019", "Sun Apr 14 2019", "Wed Apr 17 2019", "Fri Apr 19 2019", "Sat May 18 2019", "Wed Jun 05 2019", "Thu Jul 04 2019", "Mon Aug 12 2019", "Thu Aug 15 2019", "Fri Aug 23 2019", "Mon Sep 09 2019", "Tue Sep 10 2019", "Tue Sep 17 2019", "Wed Oct 02 2019", "Sat Oct 05 2019", "Sun Oct 06 2019", "Mon Oct 07 2019", "Tue Oct 08 2019", "Sun Oct 27 2019", "Sat Nov 02 2019", "Sun Nov 10 2019", "Tue Nov 12 2019", "Fri Nov 15 2019", "Wed Dec 25 2019"]
    listOfHolidays = [datetime.strptime(x,'%a %b %d %Y') for x in listOfHolidays]

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

    def __str__(self):
        x = "id ="+(str)(self.idtimetable)+"\nfrombit ="+(str)(self.frombit)+"\nfromdoranda="+(str)(self.fromdoranda)+"\nfromxavier="+(str)(self.fromxavier)+"\nfromlalpur="+(str)(self.fromlalpur)+"\ntypeofbus="+(str)(self.typeofbus)+"\ntypeofday="+(str)(self.typeofday)+"\nhasDeparted="+(str)(self.hasdeparted)+"\nisRunning="+(str)(self.isRunning);
        return x;

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
             
        }
        jsonRecord['isRunning'] = True if bytearray(b'\x01') == self.isRunning else False
        jsonRecord['hasdeparted'] = True if bytearray(b'\x01') == self.hasdeparted else False
        return jsonRecord


    @classmethod
    def getAllRecord(cls):
        query = "SELECT * FROM timetable"
        try:
            if(DbConn.connection.is_connected()==False):
                DbConn.connection._open_connection()
            cursor = DbConn.connection.cursor(prepared=True)
            cursor.execute(query)
            resultset = cursor.fetchall()
            DbConn.connection.commit()
            cursor.close()
            DbConn.connection.close()
        except:
            return None
        lst = []
        for x in resultset:
            lst.append(cls(*x).tojson())
        return lst
    
    @classmethod
    def getRecordById(cls,idtimetable):
        # query= "SELECT * FROM timetable WHERE frombit = MAKETIME(?,?,?)";
        query = "SELECT * FROM timetable WHERE idtimetable=?"
        if(DbConn.connection.is_connected()==False):
            DbConn.connection._open_connection()
        cursor = DbConn.connection.cursor(prepared=True)
        cursor.execute(query,(idtimetable,))
        resultset = cursor.fetchone()
        DbConn.connection.commit()
        cursor.close()
        DbConn.connection.close()
        
        if resultset:
            result = cls(*resultset)
            return result
        else:
            return None

    @classmethod
    def getWeekin3Char(cls,dateObj):   
        mon = "Mon-Fri"
        sun = "Sun"
        sat = "sat"
        if dateObj in cls.listOfHolidays:
            return sun
        week = [mon,mon,mon,mon,mon,sat,sun];
        return week[dateObj.weekday()]

    @classmethod
    def getRecordByDate_Time_Source(cls,sourceQuery,currdate,curtime):
        print(currdate);
        dateobj = datetime.strptime(currdate,"%Y-%m-%d")
        weekDay  = cls.getWeekin3Char(dateobj)
        query = sourceQuery
        if(DbConn.connection.is_connected()==False):
            DbConn.connection._open_connection()
        cursor = DbConn.connection.cursor(prepared=True)
        cursor.execute(query,(curtime,weekDay))
        resultset = cursor.fetchall()
        DbConn.connection.commit()
        cursor.close()
        DbConn.connection.close()

        if resultset:
            lst = []
            for x in resultset:
                lst.append(cls(*x).tojson())
            
            return lst
        else:
            return None

    @classmethod
    def getdataByRequestData(cls,requestData):
        newlist = []
        if(requestData['source']== "Ranchi") and (requestData['destination']=='BIT'):
            query = "select * from timetable where fromxavier >= ? and typeofday=? order by fromxavier";
            pointsource = 'fromxavier'
            lst = TTRecordModel.getRecordByDate_Time_Source(query,requestData["curdate"],requestData["curtime"])
            
            
        elif(requestData['source']=='BIT') and (requestData['destination']=='Ranchi'):
            query = "select * from timetable where frombit >= ? and typeofday=? order by frombit";
            pointsource = 'frombit'
            lst = TTRecordModel.getRecordByDate_Time_Source(query,requestData["curdate"],requestData["curtime"])
            
        if lst:
            for x in lst:
                if len(x[pointsource]) == 7: # For Setting Up Proper Time in HTML
                    x[pointsource] = '0'+ x[pointsource]
                obj = {
                    'departure':x[pointsource],
                    'typeofbus':x['typeofbus'],
                    'idtimetable':x['idtimetable'],
                    'isRunning':"Yes" if x['isRunning']==1 else "No",
                    'hasdeparted':"Yes" if x['hasdeparted']==1 else "No"
                }
                newlist.append(obj)
        else:
            newlist=None
        return newlist


    def updateStatus(self):
        try:
            query = "UPDATE timetable SET hasdeparted=? , isRunning=? WHERE idtimetable=?"
            if(DbConn.connection.is_connected()==False):
                DbConn.connection._open_connection()
            cursor = DbConn.connection.cursor(prepared=True)
            cursor.execute(query,(self.hasdeparted,self.isRunning,self.idtimetable))
            DbConn.connection.commit()
            print("before Updating isRunning = ",self.isRunning,"\nhasdeparted = ",self.hasdeparted)
            
            record = TTRecordModel.getRecordById(self.idtimetable)
            print("After Updating Status ");
            print(record)
            cursor.close()
            DbConn.connection.close()
            print("updated")
            return True
        except:
            print("An Error Occured")
            return False
        