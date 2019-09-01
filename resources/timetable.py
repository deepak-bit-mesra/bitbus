from flask import Flask,render_template,jsonify,make_response,redirect,url_for,session
from flask_restful import Api,Resource,reqparse
from models.timetable import TTRecordModel
from flask_jwt import JWT,jwt_required
from db import DbConn
from datetime import date,datetime,time




class TTRecordResource(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('idtimetable',type=str,required=True,help="Id for Time Table is Required")
    # parser.add_argument('frombit',type=str,required=True,help="FromBit is Required")
    # parser.add_argument('fromdoranda',type=str,required=True,help="fromdoranda is Required")
    # parser.add_argument('fromxavier',type=str,required=True,help="fromxavier is Required")
    # parser.add_argument('fromlalpur',type=str,required=True,help="fromlalpur is Required")
    # parser.add_argument('typeofbus',type=str,required=True,help="typeofbus is Required")
    # parser.add_argument('typeofday',type=str,required=True,help="typeofday is Required")
    # parser.add_argument('busno',type=str,required=True,help="busno is Required")
    parser.add_argument('isRunning',type=str,required=True,help="isRunning is Required")
    parser.add_argument('hasdeparted',type=str,required=True,help="hasdeparted is Required")
    
    
    def get(self,idtimetable):
        record = TTRecordModel.getRecordById(int(idtimetable))
        
        if(record):
            return record.tojson(),200
        else:
            return {'Message':'Record Not Found. Please try Another Id'},404
    
    # @jwt_required()
    def post(self,idtimetable):
        # if 'username' not in session:
        #     return redirect(url_for('login'))

        record = TTRecordModel.getRecordById(int(idtimetable))
        if record:
            reqestData = TTRecordResource.parser.parse_args()
            record.isRunning = 1 if reqestData['isRunning']=='True' else 0
            record.hasdeparted = 1 if reqestData['hasdeparted']=='True' else 0
            done = record.updateStatus()
            if done:
                record = TTRecordModel.getRecordById(int(idtimetable))
                print("After Updating Status  in POst Method");
                print(record)
                print("Returning Item Updated")
                recjson = record.tojson();
                print("recjson id = ",recjson["idtimetable"],"recjson hasdeparted = ",recjson["hasdeparted"])
                return {'Message':"Item Updated","record":record.tojson()} , 200
            else:
                return {"Message":"Internal Server Error"},500
        else:
            return {'Message':"Item Not Found"},404


class TTListResource(Resource):
    def get(self):
        lst = TTRecordModel.getAllRecord()
        if lst!=None:
            return {'res':lst},200,{'Access-Control-Allow-Origin':'*'}
            # TypeError: The view function did not return a valid response tuple. The tuple must have the form (body, status, headers), (body, status), or (body, headers).
            # responseBody = jsonify({'res':lst})
            # resp = make_response((responseBody,200))
            # resp.headers['Access-Control-Allow-Origin'] = '*'
            # return resp
        else:
            return {'Message':'Could Not establish a connectiont to Mysql'}

    def post(self,idtimetable):
        pass        

class  TodayTimeTable(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('source',type=str,required=True,help="Source is Required")
    parser.add_argument('destination',type=str,required=True,help="Destination is Required")
    parser.add_argument('curdate',type=str)
    parser.add_argument('curtime',type=str)
    def get(self):
        return TTRecordModel.getRecordByDate_Time_Source(None,None,None);
    
    def post(self):
        try:
            requestData = TodayTimeTable.parser.parse_args()
            newlist = TTRecordModel.getdataByRequestData(requestData)
            if newlist:
                return newlist,200
            else:
                return {'message':'No data Found'}
        except:
            return {"Message":"Bad Request"},500
    

    
            
