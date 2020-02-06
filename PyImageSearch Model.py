import cv2
import numpy as np
import dlib
import os
import face_recognition
import pickle


# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []
images = []

imagePaths = '/home/rohan/FacialRecognition/Dataset/'

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

# for filename in os.listdir('Dataset'):
# 	im = face_recognition.load_image_file('Dataset/' + filename, 0)
# 	knownEncodings[filename.split('.')[0][0]] = face_recognition.face_encodings(im)[0]
# 	images.append(im)
# print("[INFO] processing image {}/{}".format(filename + 1,
	# 										 len(imagePaths)))
# name = imagePath.split(os.path.sep)[-2]


# load the input image and convert it from RGB (OpenCV ordering)
# to dlib ordering (RGB)

	image = cv2.imread(im)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb)
	# model=args["detection_method"])

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		# knownNames.append(name)



print(encodings)
# #
with open('dataset_faces.pickle', 'wb') as f:
	pickle.dump(encodings, f)
# # dump the facial encodings + names to disk
# print("[INFO] serializing encodings...")
# data = {"encodings": knownEncodings, "names": knownNames}
# f = open(args["encodings"], "wb")
# f.write(pickle.dumps(data))
# f.close()