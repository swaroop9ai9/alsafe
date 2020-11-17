################################################################################
################################################################################
########   Python - Firebase - ALSafe                                   ########
########   Author: Swaroop Manchala                                     ########
################################################################################
################################################################################

import pyrebase
from flask import Flask, redirect, render_template, request, session, url_for
import os
from flask_mail import Mail, Message
from firebase import Firebase
from otp import send_whatsapp_message
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import math
from dbcon import checkMobileUnique,checkMobileUniquefast,getData,loadData,setData,checkFaceUnique,getDataEmail,setDataEmail
import credentials
#from flask_login import LoginManager, UserMixin, login_user, logout_user,current_user
from flask import Flask, render_template, Response
import cv2
from verifyFace import decodeImg,compareImage,computeEncodingDb,computeEncodingLive,noFaces
from flask import jsonify


# TWILIO_SID = “ACXXXXXXXXXXXXXX”
# TWILIO_AUTHTOKEN = “62f1efa7e0e9471cfdbfXXXXXXXXX”
# TWILIO_MESSAGE_ENDPOINT = “https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json".format(TWILIO_SID=TWILIO_SID)
# export EMAIL_USER= alsafenoreply@gmail.com # used for Email Verification
# export EMAIL_PASSWORD= QsEfThUkO
app = Flask(__name__)       #Initialze flask constructor
app.secret_key = os.urandom(24)
app.config['OAUTH_CREDENTIALS'] = {

    'facebook': {
        'id': '',
        'secret': ''
    },
    'twitter': {
        'id': '',
        'secret': ''
    }
}
config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "storageBucket": "",
}
# Get a reference to the auth service
fb = Firebase(config)
authenticity = fb.auth()
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": '',
    "MAIL_PASSWORD": ''
}
app.config.update(mail_settings)
mail = Mail(app)
#https://allsafe-2bd2e.firebaseapp.com/__/auth/handler
#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": "", "mobile": "", "otp": "", "otpvalid": False, "user_exist": False ,"gmail":"","facebook":"","whatsapp":"","twitter":"","status":False,"snap":"","imgstatus":False}

# usercode = " Image of User base64"


#Login
@app.route('/')
def index():
    session['user'] = False
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    checkey = session.get('user',None)
    if checkey:
        email = session.get('email',None)
        if getDataEmail(email,'is_logged_in'):
            searchid = getDataEmail(email,'uid')
            whatsapp = getData(searchid,"whatsapp")
            gmail = getData(searchid,"gmail")
            facebook = getData(searchid,"facebook")
            twitter = getData(searchid,"twitter")
            linkedin = getData(searchid,"linkedin")
            display = getDataEmail(email,'imgstatus')
            if display:
                img_base64 = getData(searchid,"snap")
            else:
                img_base64 = usercode
            return render_template("welcome.html", email = getDataEmail(email,'email'), name = getDataEmail(email,'name'), userId = searchid, whatsapp=whatsapp,gmail=gmail,facebook=facebook,twitter= twitter,linkedin=linkedin ,img_base64 = img_base64)
        else:
            return redirect(url_for('result'))
    else:
        return redirect(url_for('index'))

@app.route("/imgstatuson",methods = ["POST"])
def imgstatuson():
    email = session.get('email',None)
    if request.method == "POST":
            setDataEmail(email,'imgstatus',True)
            return redirect(url_for('welcome'))

@app.route("/imgstatusoff",methods = ["POST"])
def imgstatusoff():
    email = session.get('email',None)
    if request.method == "POST":
            setDataEmail(email,'imgstatus',False)
            return redirect(url_for('welcome'))



#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        mobile = result["mobile"]
        #Try signing in the user with the given information
        user = auth.sign_in_with_email_and_password(email, password)
        session['user'] = True
        session['email'] = email
        #Insert the user data in the global person
        # global person
        setDataEmail(email,'is_logged_in',False)
        return redirect(url_for('generateotp'))
        # except:
        #     #If there is any error, redirect back to login
        #     return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route("/signout", methods = ["POST","GET"])
def signout():
    checkey = session.get('user',None)
    if checkey:
        email = session.get('email',None)
        # person["is_logged_in"] = False
        setDataEmail(email,'is_logged_in',False)
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('index'))

@app.route("/search", methods = ["POST", "GET"])
def search():
    checkey = session.get('user',None)
    if checkey:
        email = session.get('email',None)
        if getDataEmail(email,'is_logged_in'):
            try:
                if request.method == 'GET':
                    return render_template('search.html')
                searchid = request.form['uid']
                email = getData(searchid,"email")
                name = getData(searchid,"name")
                whatsapp = getData(searchid,"whatsapp")
                gmail = getData(searchid,"gmail")
                facebook = getData(searchid,"facebook")
                twitter = getData(searchid,"twitter")
                linkedin = getData(searchid,"linkedin")
                display = getDataEmail(email,'imgstatus')
                if display:
                    img_base64s = getData(searchid,"snap")
                else:
                    img_base64s = usercode
                # email = session.get('email',None)
                if getDataEmail(email,'is_logged_in'):
                    return render_template("search.html", email = email, name = name, userId = searchid, whatsapp=whatsapp,gmail=gmail,facebook=facebook,twitter=twitter,linkedin=linkedin,img_base64s=img_base64s)
            except:
                return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))


@app.route("/authenticate", methods = ["GET","POST"])
def authenticate():
    checkey = session.get('user',None)
    if checkey:
        email = session.get('email',None)
        if request.method == "GET":
            return render_template('authenticate.html')
        else:
            if getDataEmail(email,'is_logged_in') == True:
                return render_template("authenticate.html", email = email, name = getDataEmail(email,'name'))
            else:
                return redirect(url_for('result'))
    else:
        return redirect(url_for('index'))



@app.route('/generateotp', methods=['GET', 'POST'])
def generateotp():
    checkey = session.get('user',None)
    if checkey:
        if request.method == 'GET':
            return render_template('generate.html')
        person["mobile"] = request.form['mobile']
        email = session.get('email',None)
        condition = getDataEmail(email,'user_exist')
        if condition:
            checker = True
        else:
            # checker = checkMobileUnique(person['mobile'])
            checker = True
        if checker:
            digits = "0123456789"
            OTP = "" # length of password can be chaged
            for i in range(8):
                OTP += digits[math.floor(random.random() * 10)]
            if OTP:
                to_number = "whatsapp:"+str(person["mobile"]) # Enter phone number along with country code with our '+'
                otp_msg = """Alsafe OTP code is :"""+str(OTP)
                msg = send_whatsapp_message(to_number, otp_msg)
                with app.app_context():
                    msg = Message(subject="Alsafe OTP verification",sender=app.config.get("MAIL_USERNAME"),recipients= [email],body=''' Welcome to Alsafe, We strive to maintian authenticity, integrity and accountability in your digital presence. This is your Session OTP  \t'''+str(OTP)+''' \n Please use the OTP, password and Live snap to login \n -From Alsafe Team''')
                mail.send(msg)
                setDataEmail(email,'otp',str(OTP))
                print(OTP)
                setDataEmail(email,'otpvalid',True)
                return redirect(url_for('validateotp'))
                # setDataEmail(email,'otpvalid',False)
                # setDataEmail(email,'otp',"")
                # #If there is any error, redirect back to generateotp
                # return redirect(url_for('generateotp'))
        else:
            return "This Mobile number is already registered"
    else:
        return redirect(url_for('index'))

@app.route('/fbcheck',methods=['GET','POST'])
def fbcheck():
    if request.method == "POST":
        email = session.get('email',None)
        setDataEmail(email,'facebook','facebook')
        return jsonify("Id is Authenticated with Facebook")

@app.route('/tweetcheck',methods=['GET','POST'])
def tweetcheck():
    if request.method == "POST":
        email = session.get('email',None)
        setDataEmail(email,'twitter','twitter')
        return jsonify("Id is Authenticated with Twitter")

@app.route('/linkedincheck',methods=['GET','POST'])
def tweetcheck():
    if request.method == "POST":
        email = session.get('email',None)
        setDataEmail(email,'linkedin','linkedin')
        return jsonify("Id is Authenticated with Linkedin")

@app.route('/capture', methods=['GET','POST'])
def capture():
    checkey = session.get('user',None)
    if checkey:
        if request.method == 'POST':
            image = request.form['file']
            imgstr = image.split(',')[1]
            email = session.get('email',None)
            print("Session Email",email)
            print("Status :",getDataEmail(email,'status'))
            print("User Exist :",getDataEmail(email,'user_exist'))
            # if noFaces(imgstr):
            if True:
                if (getDataEmail(email,'status') == True and getDataEmail(email,'user_exist') == False):
                    # if checkFaceUnique(imgstr):
                    if True:
                        print("yes")
                        #Try creating the user account using the provided data
                        auth.create_user_with_email_and_password(email,getDataEmail(email,'password'))

                        #Login the user
                        user = auth.sign_in_with_email_and_password(email,getDataEmail(email,"password"))
                        setDataEmail(email,'uid',user["localId"])
                        setDataEmail(email,'user_exist',True)
                        setDataEmail(email,'snap',imgstr)
                        setDataEmail(email,'otp',"")
                        setDataEmail(email,'otpvalid',False)
                        setDataEmail(email,'is_logged_in',False)
                        setDataEmail(email,'status',False)
                        with app.app_context():
                            msg = Message(subject="Alsafe Welcome",sender=app.config.get("MAIL_USERNAME"),recipients= [email],body=''' Welcome to Alsafe, We strive to maintian authenticity, integrity and accountability in your digital presence. This is your User Id  \t'''+str(getDataEmail(email,'uid'))+''' \n Please use the user Id, mail Id, password and Live snap to login \n -From Alsafe Team''')
                        mail.send(msg)
                        return jsonify("Welcome to Alsafe, A Alsafe verification has been sent to the registered Email")

                    else:
                        setDataEmail(email,'is_logged_in',False)
                        # person['is_logged_in'] = False
                        return jsonify("Gotcha, You have already registered with US!")
                elif ((getDataEmail(email,'status') == True) and (getDataEmail(email,'user_exist') == True)):
                    print("Yes Yes")
                    dbimage = getDataEmail(email,'snap')
                    dbimage = decodeImg(dbimage)
                    liveimage = decodeImg(imgstr)
                    dbcode = computeEncodingDb(dbimage)
                    livecode = computeEncodingLive(liveimage)
                    outcome = compareImage(dbcode,livecode)
                    print(outcome)
                    if outcome:
                        setDataEmail(email,'is_logged_in',True)
                        return jsonify("Welcome To AlSafe")
                    else:
                        setDataEmail(email,'is_logged_in',False)
                        return jsonify("Person Unauthorised")
                else:
                    setDataEmail(email,'is_logged_in',False)
                    return jsonify('Invalid Login')
            else:
                setDataEmail(email,'is_logged_in',False)
                return jsonify("We need just One Face ! :)")
    else:
        return redirect(url_for('index'))



@app.route('/validateotp',methods=['GET','POST'])
def validateotp():
    checkey = session.get('user',None)
    if checkey:
        email = session.get('email',None)
        setDataEmail(email,'status',False)
        if request.method == 'GET':
            return render_template('validate.html')
        user_otp = request.form['otpcode']
        if getDataEmail(email,'otpvalid')== True:
            pass
        else:
            return redirect(url_for('generateotp'))
        checkotp = getDataEmail(email,'otp')
        print("OTP valid ?",getDataEmail(email,'otpvalid'))
        print("Original OTP",checkotp)
        print("USER OTP",user_otp)
        if (checkotp == str(user_otp)) and (getDataEmail(email,'otpvalid')==True):
            print("OTP correct")
            setDataEmail(email,'status',True)
            setDataEmail(email,'whatsapp','whatsapp')
            setDataEmail(email,'gmail','gmail')
            setDataEmail(email,'otpvalid',False)
            setDataEmail(email,'otp',"")
            return render_template('capture.html')
        else:
            print("OTP Incorrect")
            setDataEmail(email,'otpvalid',False)
            setDataEmail(email,'otp',"")
            setDataEmail(email,'status',False)
            return redirect(url_for('signup'))
    else:
        return redirect(url_for('index'))




@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        mobile = result['mobile']
        password = result["pass"]
        name = result["name"]
        condition = getDataEmail(email,'user_exist')
        if condition == "invalid" or condition == False:
            global person
            #Go to welcome page
            #return redirect(url_for('welcome'))
            person["is_logged_in"] = False
            person["user_exist"] = False
            person["email"] = email
            person["mobile"] = mobile
            person['password'] = password
            person["name"] = name
            person["otpvalid"] = False
            session['email'] = email
            loadData(person)
            session['user'] = True
            return render_template('generate.html')
        else:
            #If there is any error, redirect to register
            return redirect(url_for('login'))
    else:
        return redirect(url_for('signup'))


@app.route("/resetpass",methods = ["POST", "GET"])
def resetpass():
    if request.method == "POST":
        try:
            result = request.form           #Get the data submitted
            uid = result["uid"]
            email = getData(uid,"email")
            print(email)
            authenticity.send_password_reset_email(email)
            return "Please check your registered email for reset password link"
        except:
            return render_template("forgopass.html")
@app.route("/forgopass", methods = ["POST"])
def forgopass():
    return render_template("forgopass.html")




if __name__ == '__main__':
    # app.secret_key = os.urandom(24)
    #app.run(debug=True,host='0.0.0.1',port=int(os.environ.get('PORT', 5000)))
    app.run()
