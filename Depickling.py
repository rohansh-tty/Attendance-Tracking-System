'''This is the main file. It actually contains the pickle object that consists of images and their encodings.
 Pickle object is loaded up here, and is used for face recognition. Face labels and the respective encodings
  are extracted. For face detection purpose, cv2 is used and for recognition stuff, face_recognition is used.
  Cascade face classifier is used for is used to detect faces. Rest all are same. '''


# Load all the libraries
import numpy as np
import pickle
import face_recognition
import cv2

# List for holding on the names
empList = []

# clone the opencv github repo, goto data--> haarcascades--> haarcascade_frontalface_default.xml


# create face cascade classifier
face_cascade = cv2.CascadeClassifier(
    'add-your-path/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')

# Loading the dataset pickle and comparing the face encodings

# read the pickle file
with open('dataset_faces.pickle', "rb") as f:
    unpickler = pickle.Unpickler(f)
    all_face_encodings = unpickler.load()

# extract all the names and their encodings
face_names = list(all_face_encodings.keys())
all_face_encodings = np.array(list(all_face_encodings.values()))

# video capture using opencv
video = cv2.VideoCapture(0)

process_this_frame = True

# __________________DETECT FACES_________________ #

while True:

    # Grab a single frame of video
    check, frame = video.read()

    # Resize frame of video to almost 1/4 size for faster face recognition processing
    frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the frame of video
    if process_this_frame:

         # Get the face location and its encodings

        face_locations = face_recognition.face_locations(rgb_frame)  # face locations
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # face encodings

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(all_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(all_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:  #
                name = face_names[best_match_index]
                empList.append(name)

            # create a box around the face detected
            faces = face_cascade.detectMultiScale(frame,
                                                  scaleFactor=1.05,
                                                  minNeighbors=5,
                                                  flags=cv2.CASCADE_SCALE_IMAGE)

            # # For each face draw rectangle around it
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 1)

                # Draw a label with a name below the face

                # cv2.rectangle(frame, (left+10, bottom-10), (right,bottom), (0, 255, 0), cv2.FILLED)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left, right), font, 1.0, (0, 0, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video.release()
cv2.destroyAllWindows()

# Set of Detected image labels
print(set(empList))

