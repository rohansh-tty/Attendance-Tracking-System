'''This file actually pickles up the dataset encodings into one file named #'dataset_faces.pickle' # .
 Save all the images in the Dataset folder(Dataset should be a subdirectory in your current working directory.
  Also name the image properly i.e without using any special chars. In the pickle file, there
 are two objects all_face_encodings and images. Former on is a dict and images is a list consisting of images.
  All_face_encodings consists of keys which contains all images and their respective encodings is appended as values.'''

# load all the required libraries

import face_recognition
import pickle
import os
import cv2

# create an empty dict and list, to store encodings and images
all_face_encodings = {}
images = []


# now loop over the directory and get the face_encodings of diff images
for filename in os.listdir('NewTest'):
    im = face_recognition.load_image_file('NewTest/' + filename, 0)
    all_face_encodings[filename.split('.')[0]] = face_recognition.face_encodings(im)[0]
    images.append(im)

    # image = cv2.imread(im,1)
    rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes
# corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb)

# compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    print(encodings)
# loop over the encodings
    for encoding in encodings:
        all_face_encodings[filename.split('.')[0]] = encoding
        images.append(im)
    print(all_face_encodings)


# dump all the encodings and the images into a pickle
with open('dataset_faces101.pickle', 'wb') as f:
      pickle.dump(all_face_encodings, f)
