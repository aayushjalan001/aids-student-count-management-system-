import pymongo
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://Karan_Balaji:2916@cluster0.3ep5q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["face_recognition_db"]
attendance_collection = db["attendance"]

@app.route('/retrieve_attendance', methods=['GET', 'POST'])
def retrieve_attendance():
    if request.method == 'POST':
        date = request.form['date']
        print(f"Received date: {date}")  # Debugging statement
        records = attendance_collection.find({"date": date})
        attendance_list = [{"name": record["name"], "time": record["time"]} for record in records]
        print(f"Attendance records: {attendance_list}")  # Debugging statement
        return render_template('retrieve_attendance.html', attendance=attendance_list, date=date)
    return render_template('retrieve_attendance.html', attendance=[], date='')

if __name__ == '__main__':
    app.run(debug=True)
