import cv2
import face_recognition

# List to store face encodings and names
known_face_encodings = []
known_face_names = []

# Load known images
known_person1_image = face_recognition.load_image_file("C:/Users/sande/Downloads/messi.jpg")
known_person2_image = face_recognition.load_image_file("C:/Users/sande/Downloads/kb.jpg")
known_person3_image = face_recognition.load_image_file("C:/Users/sande/Downloads/elon1.jpg")
known_person4_image = face_recognition.load_image_file("C:/Users/sande/Downloads/cr7.webp")

# Encode faces from the known images
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]
known_person3_encoding = face_recognition.face_encodings(known_person3_image)[0]
known_person4_encoding = face_recognition.face_encodings(known_person4_image)[0]

# Add the encodings and names to the lists
known_face_encodings.append(known_person1_encoding)
known_face_encodings.append(known_person2_encoding)
known_face_encodings.append(known_person3_encoding)
known_face_encodings.append(known_person4_encoding)

known_face_names.append("messi")
known_face_names.append("karan")
known_face_names.append("elon")
known_face_names.append("cr")

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Convert the frame to RGB (face_recognition works with RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Find all faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        name = "unknown"
        
        # Check if the face matches any known faces
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        # Draw a rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    # Display the resulting frame
    cv2.imshow("Video", frame)
    
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
