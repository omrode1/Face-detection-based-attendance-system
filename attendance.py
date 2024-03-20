import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv

def load_known_candidates():
    with open('D:/office/Attendance system/candidates.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        encodings = []
        names = []
        for row in reader:
            img_path = os.path.join(row['Folder_Path'], '0.jpg')  # Assuming the first image is used for encoding
            img = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(img)[0]
            encodings.append(encoding)
            names.append(row['Name'])
        return encodings, names

def markAttendance(name):
    with open('D:/office/Attendance system/Attendance.csv', 'r+') as f:
        # Read all existing lines
        lines = f.readlines()
        # Extract existing names from lines
        existing_names = [line.split(',')[0] for line in lines]
        
        now = datetime.now()
        dtString = now.strftime('%Y-%m-%d %H:%M:%S')  # Date and time format
        
        if name not in existing_names:
            if now.hour < 12:  # Check if entry is before 12 PM
                f.write(f'{name},{dtString},IN\n')
            else:
                f.write(f'{name},{dtString},OUT\n')
        else:
            # Update exit time for the candidate
            for i, line in enumerate(lines):
                if name in line:
                    parts = line.strip().split(',')
                    if parts[-1] == 'IN' and now.hour >= 16:  # Check if exit is after 4 PM
                        parts[-1] = 'OUT'
                        parts[1] = dtString
                        lines[i] = ','.join(parts) + '\n'
                        f.seek(0)
                        f.writelines(lines)
                    break

encodings_known, names_known = load_known_candidates()
print('Encoding Complete')

cap = cv2.VideoCapture(1)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodings_cur_frame = face_recognition.face_encodings(imgS, facesCurFrame)

    for faceLoc, encodingFace in zip(facesCurFrame, encodings_cur_frame):
        matches = face_recognition.compare_faces(encodings_known, encodingFace)
        name = "Unknown"  # Default to Unknown
        if True in matches:
            match_index = matches.index(True)
            name = names_known[match_index]
            markAttendance(name)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
