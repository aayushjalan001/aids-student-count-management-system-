import pymongo
import face_recognition
from flask import Flask, request, jsonify

app = Flask(__name__)

# MongoDB Connection
try:
    client = pymongo.MongoClient(
        "mongodb+srv://Karan_Balaji:2916@cluster0.3ep5q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    db = client["student_attendance"]
    collection = db["students"]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        # Validate file input
        if 'photo' not in request.files:
            return jsonify({"message": "No photo provided in the request."}), 400

        photo = request.files['photo']

        # Validate text inputs
        name = request.form.get('name')
        rollno = request.form.get('rollno')

        if not name or not rollno:
            return jsonify({"message": "Name and Roll Number are required fields."}), 400

        # Validate MIME type of the uploaded file
        if photo.mimetype not in ['image/jpeg', 'image/png']:
            return jsonify({"message": "Invalid file type. Only JPEG and PNG are allowed."}), 400

        print(f"Processing: Name={name}, Roll No={rollno}, File={photo.filename}, MIME={photo.mimetype}")

        # Load and process the uploaded image
        image = face_recognition.load_image_file(photo.stream)
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            return jsonify({"message": "No face detected in the provided photo."}), 400

        encoding = encodings[0]

        # Insert student data into MongoDB
        student_data = {
            "name": name,
            "rollno": rollno,
            "encoding": encoding.tolist()  # Convert NumPy array to list for JSON serialization
        }

        collection.insert_one(student_data)
        print("Student data inserted successfully:", student_data)

        return jsonify({"message": "Student added successfully!"}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"message": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
