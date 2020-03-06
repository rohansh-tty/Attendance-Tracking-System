# Load all the libraries
import os
import cv2
import time
import pickle
import sqlite3
import argparse
import datetime
import numpy as np
import tkinter as tk
import face_recognition
from imutils import paths
import tkinter.messagebox
from PIL import ImageTk, Image



#import faceEncoding() from PiCameraTest
# from FaceEncodings import addNewFace


# # import insertData() from InsertData.py file
# from InsertData import insertData

# # import updateData() fro UpdateData.py file
# from UpdateData import updateCheckout

#import sqliteObject class from SQL_Query file
from SQL_Query import sqliteObject

st = ""
face_locations = []



# read the pickle file
with open('newfaceEncoding.pickle', "rb") as f:
    unpickler = pickle.Unpickler(f)
    all_encodings = unpickler.load()

known_face_names = list(all_encodings.keys())
all_face_encodings = np.array(list(all_encodings.values()))
print(known_face_names)




# main_ dict holding up the detected face names with values as check in time
main_ = {}

currentTime = datetime.datetime.now()
def compliment():
    a = " "
    hello = 'Hello'
    if currentTime.hour <= 12:
        a = 'Good Morning, Have a nice day!'
    elif currentTime.hour in (12, 16):
        a = 'Good Afternoon, Have a nice day!'
    elif currentTime.hour > 16:
        a = 'Good Evening, Have a nice day!'   
    return a



notify = None
checkoutTime = None
x = None



# sqlite object
SQLITE = sqliteObject()
# this creates a new table called newSheet 
SQLITE.createTable()


# Set time limit for message box
timeDuration = 3000


# list of checkIns
checkIn = []


# MAIN BUTTON: Recognize Me(Face Recognition Function)
def recognizeMe():
    # checkoutTime by default set to NONE
	checkoutTime = None

    # set date 
	x = datetime.datetime.now()
	SQLITE.Date = x.strftime("%d-%m-%Y")# ---------------------------------------------------- DATE
   
   
	left = right = top = bottom = 0
    # Get a reference to webcam #0 (the default one)
	video_capture = cv2.VideoCapture(-1)
    # Set FPS limit to 6
	video_capture.set(cv2.CAP_PROP_FPS, 6) 
    

	while True:
			ret, frame = video_capture.read()
			frame = cv2.resize(frame, (0, 0), fx=0.40, fy=0.40)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
			rgb_frame = frame[:, :, ::-1]
    # Find all the faces and face enqcodings in the frame of video
			face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample = 2)
			face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


    # Loop through each face in this frame of video
			for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the faqce is a match for the known face(s)
				matches = face_recognition.compare_faces(all_face_encodings, face_encoding)
    				# Draw a box around the face
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
				name = "Unknown"
        			# Or instead, use the known face with the smallest distance to the new face
				face_distances = face_recognition.face_distance(all_face_encodings, face_encoding)
				best_match_index = np.argmin(face_distances)
                

				if matches[best_match_index]:
					name = known_face_names[best_match_index]
					SQLITE.name = name # ----------------------------------------------------------- name
                   
                    			# append recognized face name to checkIn if not already present
					if name not in checkIn:
						checkIn.append(name)
						SQLITE.checkout = None# -------------------------------------------CHECKOUT-TIME
						SQLITE.checkin = str(datetime.datetime.now().hour) +':'+ str(datetime.datetime.now().minute)#------------CHECKIN-TIME
                         
					elif checkIn.count(name) == 1: #if present set the checkout time to current time
						print('This name is already entered')
						MsgBox = tk.messagebox.askquestion ('Notification',str(name)+ ' are you checking out?',icon = 'warning')
						if MsgBox == 'yes':
							SQLITE.checkoutTime =  str(datetime.datetime.now().hour) +':'+ str(datetime.datetime.now().minute)# ------CHECKOUT TIME
							SQLITE.updateCheckout(SQLITE.name, SQLITE.checkoutTime)# ---------------------------------------------updateCheckout()
							tk.messagebox.showinfo('Notification',str(name) + ' attendance for the day has been recorded.\nThank You')
 
					elif checkIn.count(name) >1:
						break

					if name not in list(main_.keys()): 
						main_[name] = str(datetime.datetime.now().hour) +':'+ str(datetime.datetime.now().minute)
           
# Inserts data into the Attendance Table in Employee Database
						try:
							print('Try Block')
							SQLITE.ID = len(checkIn)#-------------------------------------------------ID
							SQLITE.insertData(SQLITE.ID, SQLITE.Date, SQLITE.name, SQLITE.checkin, SQLITE.checkout)# -----------------------------------------insertData()
							print('Data Inserted Successfully...')
                            				# insertData(1, Date, name, main_[name], checkoutTime)    
                           
          						# Draw a label with a name below the face
						except Exception as e:
							print(e)
                            
                        
						cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 1)
						font = cv2.FONT_HERSHEY_DUPLEX
						cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                    # show the detected frame
						cv2.imshow('Video', frame)
                    # hold it for 2 secs
						cv2.waitKey(2000)
						cv2.destroyAllWindows()
                    # notification
						
						tkinter.messagebox.showinfo('Notification',
                                                str(name) + ' your attendance has been recorded in the DB.\nThank You!')
						if cv2.waitKey(5000):
							break
                    
                    

				else:
                                       # By default set the name to Unknown
					name = 'Unknown'
					cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
					font = cv2.FONT_HERSHEY_DUPLEX
					cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                                       # show the detected frame
					cv2.imshow('Video', frame)
                                       # hold it for 2 secs
					cv2.waitKey(2000)
					cv2.destroyAllWindows()
                                       # notification
					tkinter.messagebox.showinfo('Notification',
                                                'No face detected.\nPlease try again or \ntry contacting AI Team.\nThank You!')
					if cv2.waitKey(5000):
						break    # Hit 'q' on the keyboard to quit!
			if cv2.waitKey(1000):
				break

# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()


# for digital clock
time1 = ''
                
                

class GUI(tk.Tk):

    def __init__(self):

# TKINTER Object
        self.root = tk.Tk()
        self.root.configure(background='white')
        self.root.geometry("800x480")
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.root.resizable(0, 0)
        lmain = tk.Label(self.root)
        imagecounter = int(0)
        lmain.pack()


    def tkWindow(self):

        l1 =tk.Label(master=self.root, text = 'Makonis Software Solutions', bg= 'Blue').pack()#, height = 1, width = 40)#.pack(side = 'top')
        # l1.place(x=260, y=90)
        # tk.Label(self.root, text = 'Attendance System').pack(side = 'bottom')
        r = tk.Entry(self.root)
        self.root.title('Attendance System ---- Face Recognition ')
        r.focus_set()

        #------------ Logo
            
        filename = ImageTk.PhotoImage(Image.open('logo.jpeg' ))
        background_label = tk.Label(self.root, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Makonis Label
        text = tk.Label(self.root, text="Makonis Software Solutions", height = 5, font = 'TimesNewRoman 15 bold')
        text.place(x=240,y=50)


        # Date Label
        dateLabel = tk.Label(self.root, text=f"{datetime.datetime.now():%a, %b %d %Y}", fg="white", bg="black", font=("helvetica", 10))
        dateLabel.place(x=10, y=10)



    # RECOGNIZE ME BUTTON
        click_recognize = tk.Button(master=self.root, text = 'Recognize Me', height = 3,
                                 bg='Lawn Green', fg = 'Black'  , command= recognizeMe)
        click_recognize.place(x=345, y=354)
	    # NEW DATASET
    #click_recognize = tk.Button(master=root, text='New Data',
     #                           bg='Yellow', command = newImage)
    #click_recognize.pack(side='top')

# 0------------NOT REQUIRED ---- ADD LATER
        # click_recognize = tk.Button(master=self.root, text='Exit',
        #                         bg='Grey', fg = 'Black' ,
        #                         command = EXIT)
        # click_recognize.pack(side='bottom')


    # TIME GREETING
    #     text = tk.Text(self.root, height = 2, width =32, bg = 'mint cream', fg='black')

    # # T = tk.Text(root, height=10, width=30)
    #     text.pack()
    #     TimeGreeting = compliment()
    #     text.insert(tk.END, TimeGreeting)
    #     text.pack(side = 'top')
    
    #     # mainloop here, shift to bottom later
        self.root.mainloop()



# 0------------NOT REQUIRED ---- ADD LATER
         
        # tk.Label(self.root, text="First Name").pack()
        # e = Entry(self.root)
        # e.pack()
        # e.focus_set()
        # click_button = Button(master=self.root, text='Start',
        #                    bg='Black', fg = 'White' , command=name_portal)
        # click_button.pack(side="top")
attendanceApp = GUI()
attendanceApp.tkWindow()
# recognizeMe()
# root.mainloop()

# this is the infinite loop that helps in running the GUI application

