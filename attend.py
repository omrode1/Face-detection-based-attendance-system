import cv2
import numpy as np
import face_recognition


imgOm = face_recognition.load_image_file('D:\office\images\om.png')   
imgOm = cv2.cvtColor(imgOm, cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('D:\office\images\pfp.png')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgOm)[0]
encodeOm = face_recognition.face_encodings(imgOm)[0]
cv2.rectangle(imgOm, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
print(faceLoc)

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)
print(faceLocTest)

results = face_recognition.compare_faces([encodeOm], encodeTest) 
faceDis = face_recognition.face_distance([encodeOm], encodeTest)
print (results, faceDis)
cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


cv2.imshow('Om', imgOm)
cv2.imshow('OmTest', imgTest)
cv2.waitKey(0)