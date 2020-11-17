import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def setcred():
    cred = credentials.Certificate({
    })
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {'databaseURL': '{url}'})
setcred()
