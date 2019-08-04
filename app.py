from flask import Flask,render_template,jsonify,redirect,request,url_for
from flask_restful import Api,Resource
from flask_jwt import JWT,jwt_required

from models.timetable import TTRecordModel
from models.user import UserModel
from resources.timetable import TTListResource,TTRecordResource,TodayTimeTable
from security import authenticate,identify


app = Flask(__name__)
app.secret_key = "myEncryptionKey"
jwt = JWT(app,authenticate,identify) # /auth
api = Api(app)




@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        
        return redirect(url_for("result"),302)
    else:
        return render_template('index.html')
    # return render_template('index.html',currrentRountine=loadHome())

@app.route('/result',methods=['POST'])
def result():
    if(request.method=='POST'):
        requestData = request.form
        lst = TodayTimeTable.getdataByRequestData(requestData)
    return render_template('results.html',newlist= lst)


api.add_resource(TTListResource,'/routine')
api.add_resource(TTRecordResource,'/ttRecordResource/<string:idtimetable>')
api.add_resource(TodayTimeTable,'/today')

if __name__=="__main__":
    app.run(host='0.0.0.0' ,port=5000,debug=False)
    # app.run(port=5000,debug=False)