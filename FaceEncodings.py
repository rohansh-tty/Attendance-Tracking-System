# import necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
    
# create an empty dict and list, to store encodings and images
all_face_encodings = {}
images = []

# now loop over the directory and get the face_encodings of diff images
for filename in os.listdir('Dataset'):
        im = face_recognition.load_image_file('Dataset/' + filename, 0)
        all_face_encodings[filename.split('.')[0]] = face_recognition.face_encodings(im)[0]
        images.append(im)

    # image = cv2.imread(im,1)
    # convert the image frame to RGB from BGR(Inverse)
        rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes
# corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb)

# compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        
# loop over the encodings
        for encoding in encodings:
            all_face_encodings[filename.split('.')[0]] = encoding
            images.append(im)
    #print(all_face_encodings)


# dump all the encodings and the images into a pickle
with open('newfaceEncoding.pickle', 'wb') as f:
            pickle.dump(all_face_encodings, f)
print('New Pickle file saved...')
