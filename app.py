from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Function to load candidates from CSV file
def load_candidates():
    candidates = []
    with open('D:/office/Attendance system/candidates.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            candidates.append(row)
    return candidates

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process form data and save to CSV file
        name = request.form['name']
        branch = request.form['branch']
        uid = request.form['uid']
        sex = request.form['sex']
        year_of_study = request.form['year_of_study']
        # Save image and other details to CSV
        # Redirect to registration success page or another appropriate page
        return redirect(url_for('registration_success'))
    return render_template('register.html')

# Route for viewing individual candidate attendance
@app.route('/attendance/<name>')
def candidate_attendance(name):
    # Load attendance from CSV file for the given candidate
    attendance_data = load_attendance(name)  # You need to implement load_attendance function
    # Display attendance data
    return render_template('attendance.html', name=name, attendance=attendance_data)

# Route for clearing CSV files
@app.route('/clear_data')
def clear_data():
    # Clear contents of CSV files
    with open('candidates.csv', 'w') as csvfile:
        csvfile.truncate()
    with open('Attendance.csv', 'w') as csvfile:
        csvfile.truncate()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
