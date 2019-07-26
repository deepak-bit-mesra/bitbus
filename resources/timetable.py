from flask import Flask,render_template,jsonify
from flask_restful import Api,Resource,reqparse
from models.timetable import TTRecordModel
from flask_jwt import JWT,jwt_required
from db import DbConn



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
    
    @jwt_required()
    def put(self,idtimetable):
        record = TTRecordModel.getRecordById(int(idtimetable));
        if record:
            reqestData = TTRecordResource.parser.parse_args()
            record.isRunning = reqestData['isRunning']
            record.hasdeparted = reqestData['hasdeparted']
            record = record.updateStatus();
            if record:
                return {'Message':"Item Updated"} , 200
            else:
                return {"Message":"Internal Server Error"},500
        else:
            return {'Message':"Item Not Found"},404


class TTListResource(Resource):
    def get(self):
        lst = TTRecordModel.getAllRecord()
        if lst!=None:
            return {'res':lst},200
        else:
            return {'Message':'Could Not establish a connectiont to Mysql'}

    def post(self,idtimetable):
        pass        