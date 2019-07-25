from flask import Flask,render_template,jsonify
from flask_restful import Api,Resource
from flask_jwt import JWT,jwt_required

from models.timetable import TTRecordModel
from models.user import UserModel
from resources.timetable import TTListResource,TTRecordResource
from security import authenticate,identify


app = Flask(__name__)
app.secret_key = "myEncryptionKey"
jwt = JWT(app,authenticate,identify) # /auth
api = Api(app)




@app.route('/')
def home():
    return render_template('index.html')


api.add_resource(TTListResource,'/routine')
api.add_resource(TTRecordResource,'/ttRecordResource/<string:idtimetable>')

if __name__=="__main__":
    app.run(port=5000,debug=True)