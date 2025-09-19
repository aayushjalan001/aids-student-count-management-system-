import pymongo
import face_recognition
import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://Karan_Balaji:2916@cluster0.3ep5q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["face_recognition_db"]
collection = db["faces"]

# Store face encodings and names for recognition
known_face_encodings = []
known_face_names = []

# Variable to hold the name of the most recently recognized face
latest_recognized_name = "Unknown"

# Load known faces from database
def load_known_faces():
    global known_face_encodings, known_face_names

    # Query faces data from MongoDB
    faces = collection.find()

    for face in faces:
        encoding = face["encoding"]
        name = face["name"]

        # Add the face encoding and name
        known_face_encodings.append(np.array(encoding))
        known_face_names.append(name)
        print(f"Loaded {name}'s face encoding.")

# Call the function to load known faces
load_known_faces()

# Debugging: Log loaded face encodings and names
print("Loaded face encodings:", known_face_encodings)
print("Loaded face names:", known_face_names)

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not video_capture.isOpened():
    print("Error: Could not access the webcam.")

# Function to generate frames for the video feed
def gen_frames():
    global latest_recognized_name
    while True:
        ret, frame = video_capture.read()  # Capture a frame
        if not ret:
            print("Error: Failed to capture video frame.")
            continue  # Skip to the next iteration if frame capture fails

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
        face_locations = face_recognition.face_locations(rgb_frame)  # Detect faces
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # Get face encodings

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]
                latest_recognized_name = name  # Update the latest recognized name

            # Draw rectangle and label on the frame
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Encode the frame as JPEG and yield it for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recognition_status')
def recognition_status():
    recognized = False
    name = ""

    # Check if a recognized face exists
    if latest_recognized_name != "Unknown":
        recognized = True
        name = latest_recognized_name  # Get the name of the most recent recognized face

    # Print status for debugging
    print(f"Recognition Status: recognized={recognized}, name={name}")

    return jsonify({"recognized": recognized, "name": name})

if __name__ == '__main__':
    app.run(debug=True)
