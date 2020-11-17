import face_recognition
from scipy.spatial import distance
import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
import io


def compareImage(imageencoding,unknownencode):
    for unknown_encode in unknownencode:
        d = distance.euclidean(imageencoding,unknown_encode)
        print(d)
    if d <0.5:
        outcome = True
    else:
        outcome = False
    return outcome
#
def computeEncodingDb(image):
    imageencoding = face_recognition.face_encodings(image)[0]
    return imageencoding
def computeEncodingLive(liveimage):
    liveimageencoding = face_recognition.face_encodings(liveimage)
    return liveimageencoding
def decodeImg(baseimg):
    img = imread(io.BytesIO(base64.b64decode(baseimg)))
    opencvimage = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #cv2.imwrite("reconstructed.jpg", opencvimage) # In order to display Image
    return opencvimage

def noFaces(imgstr):
    liveimage = decodeImg(imgstr)
    face_location = face_recognition.face_locations(liveimage)     # Returns the location of the face by using a sliding window classifier
    print("Number of faces found :",len(face_location),"\n")
    if len(face_location) == 1:
        return True
    else:
        return False
# name1 = input("Enter name of image 1 : ")
# image = cv2.imread('/Users/batman/Downloads/'+str(name1)+'.jpg')
# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  # To convert to RGB format
# imageencoding = face_recognition.face_encodings(image)[0]
# name2 = input("Enter name of image 2 : ")
# unknownimg = cv2.imread('/Users/batman/Downloads/'+str(name2)+'.jpg')
# unknownimg = cv2.cvtColor(unknownimg,cv2.COLOR_BGR2RGB)  # To convert to RGB format
# unknownencode = face_recognition.face_encodings(unknownimg)
