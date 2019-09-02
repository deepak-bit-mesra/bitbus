from flask import Flask,render_template,redirect,request,url_for,session,flash
from flask_restful import Api,Resource
from flask_jwt import JWT,jwt_required

# My Own Files
from models.timetable import TTRecordModel
from models.user import UserModel
from resources.timetable import TTListResource,TTRecordResource,TodayTimeTable
from security import authenticate,identify
import cronJob
# from db import db


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bc658df5e46833:7ff652b58b56936@us-cdbr-iron-east-02.cleardb.net/heroku_219aea5cf37fe0e'
# db = SQLAlchemy(app)
app.secret_key = "myEncryptionKey"
jwt = JWT(app,authenticate,identify) # /auth
api = Api(app)
# db.init_app(app)
# login_manager = LoginManager(app)




@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/result',methods=['POST'])
def result():
    if(request.method=='POST'):
        requestData = request.form
        lst = TTRecordModel.getdataByRequestData(requestData)
    return render_template('results.html',newlist= lst)

@app.route('/login')
def login():

    if 'username' in session:
        return redirect(url_for('admonconsile'))
    
    return render_template('login.html')

@app.route('/login' ,methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = authenticate(username,password)

    if user:
        session['username'] = user.username;
        return redirect(url_for('admonconsile'))
    else:
        flash('Username or Password Incorrect')
        return redirect(url_for('login'))
    

        
@app.route('/adminconsole')
def admonconsile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('AdminStatusUpdate.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))




api.add_resource(TTListResource,'/routine')
api.add_resource(TTRecordResource,'/ttRecordResource/<string:idtimetable>')
api.add_resource(TodayTimeTable,'/today')

if __name__=="__main__":
    
    app.run(host='0.0.0.0' ,port=5000,debug=False)
    # app.run(port=5000,debug=False)