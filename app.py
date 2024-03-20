from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import cv2
import numpy as np
import face_recognition
from datetime import datetime

app = Flask(__name__)

# Function to load candidates from CSV file
def load_candidates():
    candidates = []
    with open('D:/office/Attendance system/candidates.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            candidates.append(row)
    return candidates

# Function to mark attendance
def mark_attendance(name):
    with open('D:/office/Attendance system/Attendance.csv', 'a') as f:
        now = datetime.now()
        dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{name},{dt_string}\n')

# Function to detect faces and mark attendance
def detect_and_mark():
    path = 'D:/office/Attendance system/images'
    images = []
    classNames = []
    mylist = os.listdir(path)
    for cl in mylist:
        curImg = cv2.imread(os.path.join(path, cl))
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    encodings_known = find_encodings(images)

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
                name = classNames[match_index]
                mark_attendance(name)

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

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the candidate registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process form data and save to CSV file
        name = request.form['name']
        branch = request.form['branch']
        uid = request.form['uid']
        sex = request.form['sex']
        year_of_study = request.form['year_of_study']
        # Save image and other details to CSV (to be implemented)
        
        # Redirect to thank you page after 5 seconds
        return render_template('thank_you.html')
    return render_template('register.html')

# Route for viewing individual candidate attendance
@app.route('/attendance/<name>')
def candidate_attendance(name):
    # Load attendance from CSV file for the given candidate
    attendance_data = load_attendance(name)  # You need to implement load_attendance function
    # Display attendance data
    return render_template('attendance.html', name=name, attendance=attendance_data)

# Route for starting face detection and marking attendance
@app.route('/start_system')
def start_system():
    detect_and_mark()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
