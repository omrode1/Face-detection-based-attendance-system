import cv2
import os
import csv

def take_candidate_details():
    name = input("Enter candidate's name: ")
    branch = input("Enter candidate's branch: ")
    UID = input("Enter candidate's UID: ")
    sex = input("Enter candidate's sex: ")
    year_of_study = input("Enter candidate's year of study: ")
    # You can add more details such as ID, etc.
    return name, branch, UID, sex, year_of_study

def create_candidate_folder(name):
    folder_path = f"D:/office/Attendance system/candidates/{name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def capture_images(folder_path):
    cap = cv2.VideoCapture(1)  # Use camera index 0 for default camera
    count = 0
    while count < 100:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 1:  # Capture image only if exactly one face is detected
            (x, y, w, h) = faces[0]
            face_img = frame[y:y+h, x:x+w]
            resized_img = cv2.resize(face_img, (150, 150))  # Resize image for consistency
            cv2.imwrite(f"{folder_path}/{count}.jpg", resized_img)
            count += 1
            print(f"Image {count} captured.")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Capture Images', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

def register_candidate():
    name, branch, UID, sex, year_of_study = take_candidate_details()
    folder_path = create_candidate_folder(name)
    capture_images(folder_path)

    with open('D:/office/Attendance system/candidates.csv', 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Branch', 'UID', 'Sex', 'Year_of_Study', 'Folder_Path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if os.path.getsize('D:/office/Attendance system/candidates.csv') == 0:  # Check if file is empty
            writer.writeheader()

        writer.writerow({'Name': name, 'Branch': branch, 'UID': UID, 'Sex': sex, 'Year_of_Study': year_of_study, 'Folder_Path': folder_path})

    print("Candidate registered successfully.")

if __name__ == "__main__":
    register_candidate()
