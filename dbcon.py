import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import time
import matplotlib.pyplot as plt

#To remove
#import credentials
from verifyFace import decodeImg,compareImage,computeEncodingDb,computeEncodingLive

def loadData(data):
    ref = db.reference('users')
    email = (data['email'].split('@')[0]+data['email'].split('@')[1])
    email = email.split('.')[0]+email.split('.')[1]
    print(email)
    ref.child(email).update(data)
    # Generate a reference to a new location and add some data using push()
def getDataEmail(email,mode):
    # email = email.split('@')[0]+email.split('@')[1]
    # email = email.split('.')[0]+email.split('.')[1]
    ref = db.reference('users')
    snapshot = ref.order_by_child('email').equal_to(email).get()
    if mode == "uid":
        for key,val in snapshot.items():
            return val['uid']
    elif mode == "mobile":
        for key,val in snapshot.items():
            return val['mobile']
    elif mode == "name":
        for key,val in snapshot.items():
            return val['name']
    elif mode == "email":
        for key,val in snapshot.items():
            return val['email']
    elif mode == "whatsapp":
        for key,val in snapshot.items():
            return val['whatsapp']
    elif mode == "gmail":
        for key,val in snapshot.items():
            return val['gmail']
    elif mode == "password":
        for key,val in snapshot.items():
            return val['password']
    elif mode == "facebook":
        for key,val in snapshot.items():
            return val['facebook']
    elif mode == "twitter":
        for key,val in snapshot.items():
            return val['twitter']
    elif mode == "snap":
        for key,val in snapshot.items():
            return val['snap']
    elif mode == "is_logged_in":
        for key,val in snapshot.items():
            return val['is_logged_in']
    elif mode == "otpvalid":
        for key,val in snapshot.items():
            return val['otpvalid']
    elif mode == "otp":
        for key,val in snapshot.items():
            return val['otp']
    elif mode == "user_exist":
        for key,val in snapshot.items():
            return val['user_exist']
    elif mode == "status":
        for key,val in snapshot.items():
            return val['status']
    else:
        pass
    return "invalid"
# email = 'swajodjoj@gmail.com'
# condition = getDataEmail(email,'user_exist')
# if condition == "invalid":
#     print("User not existing")
# else:
#     print("User existing")

# print(getDataEmail('swaroopmanchala9@gmail.com','otpvalid'))

#loadData(data)
# data = {"name": "Swaroop", "email": "swaroop9ai9@gmail.com","mobile":"+919440775280"}
# loadData(data)
# data = {"email":'swaroop9ai9@gmail.com',"gmail":"gmail","twitter":"twitter"}
# loadData(data)
def getData(uid,mode):
    ref = db.reference('users')
    snapshot = ref.order_by_child('uid').equal_to(uid).get()
    if mode == "uid":
        for key,val in snapshot.items():
            data = val['uid']
    elif mode == "mobile":
        for key,val in snapshot.items():
            data = val['mobile']
    elif mode == "name":
        for key,val in snapshot.items():
            data = val['name']
    elif mode == "email":
        for key,val in snapshot.items():
            data = val['email']
    elif mode == "whatsapp":
        for key,val in snapshot.items():
            data = val['whatsapp']
    elif mode == "gmail":
        for key,val in snapshot.items():
            data = val['gmail']
    elif mode == "facebook":
        for key,val in snapshot.items():
            data = val['facebook']
    elif mode == "twitter":
        for key,val in snapshot.items():
            data = val['twitter']
    elif mode == "snap":
        for key,val in snapshot.items():
            data = val['snap']
    elif mode == "is_logged_in":
        for key,val in snapshot.items():
            data = val['is_logged_in']
    elif mode == "otpvalid":
        for key,val in snapshot.items():
            data = val['otpvalid']
    elif mode == "otp":
        for key,val in snapshot.items():
            data = val['otp']
    elif mode == "user_exist":
        for key,val in snapshot.items():
            data = val['user_exist']
    elif mode == "status":
        for key,val in snapshot.items():
            data = val['status']
    else:
        print("Invalid")
    return data

def setData(uid,mode,txt):
    ref = db.reference('users')
    snapshot = ref.order_by_child('uid').equal_to(uid).get()
    #print(snapshot)
    if mode =="gmail":
        ref.child(uid).update({'gmail': txt})
    elif mode == "facebook":
        ref.child(uid).update({'facebook': txt})
    elif mode == "twitter":
        ref.child(uid).update({'twitter': txt})
    elif mode == "is_logged_in":
        ref.child(uid).update({'is_logged_in': txt})
    elif mode == "otpvalid":
        ref.child(uid).update({'otpvalid': txt})
    elif mode == "otp":
        ref.child(uid).update({'otp': txt})
    elif mode == "user_exist":
        ref.child(uid).update({'user_exist': txt})
    elif mode == "status":
        ref.child(uid).update({'status': txt})
    else:
        print("Invalid")

def setDataEmail(email,mode,txt):
    email = email.split('@')[0]+email.split('@')[1]
    email = email.split('.')[0]+email.split('.')[1]
    ref = db.reference('users')
    # snapshot = ref.order_by_child('email').equal_to(email).get()
    #print(snapshot)
    if mode =="gmail":
        ref.child(email).update({'gmail': txt})
    elif mode == "facebook":
        ref.child(email).update({'facebook': txt})
    elif mode == "whatsapp":
        ref.child(email).update({'whatsapp':txt})
    elif mode == 'uid':
        ref.child(email).update({'uid':txt})
    elif mode == "twitter":
        ref.child(email).update({'twitter': txt})
    elif mode == "is_logged_in":
        ref.child(email).update({'is_logged_in': txt})
    elif mode == "otpvalid":
        ref.child(email).update({'otpvalid': txt})
    elif mode == "otp":
        ref.child(email).update({'otp': txt})
    elif mode == "user_exist":
        ref.child(email).update({'user_exist': txt})
    elif mode == "status":
        ref.child(email).update({'status': txt})
    elif mode == "snap":
        ref.child(email).update({'snap':txt})
    else:
        print("Invalid")



def checkMobileUnique(phone_number):
    ref = db.reference('users')
    snapshot = ref.get()
    results = []
    for key,val in snapshot.items():
        results.append(val['mobile'])
    data = pd.DataFrame(results)
    if phone_number in data.values:
        return False
    else:
        return True


def checkMobileUniquefast(phone_number):
    ref = db.reference('users')
    snapshot = ref.get()
    for val in snapshot.values():
        if phone_number == val['mobile']:
            return False
    return True


def checkFaceUnique(liveimg):
    liveimg = decodeImg(liveimg)
    livecode = computeEncodingLive(liveimg)
    ref = db.reference('users')
    snapshot = ref.get()
    for key,val in snapshot.items():
        dbimage = decodeImg(val['snap'])
        dbcode = computeEncodingDb(dbimage)
        if compareImage(dbcode,livecode):
            return False
        else:
            pass
    return True

# live = getData('km0TSkiycadzlPORHLGmc6I1GG13','snap')
# print(checkFaceUnique(live))

# facea = getData('km0TSkiycadzlPORHLGmc6I1GG13','snap')
# faceb = getData('yy6xkt7ID4TDfaNAzAIt1hDrjho1','snap')
# facea = decodeimg(facea)
# faceb = decodeimg(faceb)
# cv2.imwrite("face1.jpg", facea) # In order to display Image
# cv2.imwrite("face2.jpg", faceb) # In order to display Image
# faceacode = face_recognition.face_encodings(facea)[0]
# facebcode = face_recognition.face_encodings(faceb)
# print(compareimage(faceacode,facebcode))
