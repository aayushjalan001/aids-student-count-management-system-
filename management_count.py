import pymongo
from flask import Flask, request, jsonify

app = Flask(__name__)

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://Karan_Balaji:2916@cluster0.3ep5q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["student_attendance"]
collection = db["students"]

@app.route('/check_attendance', methods=['POST'])
def check_attendance():
    rollno = request.form['rollno']
    student = collection.find_one({"rollno": rollno})
    if student:
        return jsonify({"message": f"Attendance found for {student['name']}."})
    else:
        return jsonify({"message": "No attendance record found."})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
