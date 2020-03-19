# Load all the libraries
import os
import cv2
import time
import sqlite3
import pickle
import datetime
import numpy as np
import tkinter as tk
import face_recognition
from imutils import paths
import tkinter.messagebox
from PIL import ImageTk, Image


#import faceEncoding() from PiCameraTest
from FaceEncodings import addNewFace

# import insertData() from InsertData.py file
from InsertData import insertData

# import updateData() fro UpdateData.py file
from UpdateData import updateCheckout

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

notify = None


connectObject = sqlite3.connect('EmployeeCpy1.db')
crsr = connectObject.cursor()



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
    Date = x.strftime("%x")
   
   # Set FaceLocations to 0
    left = right = top = bottom = 0
   
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(-1)
    
    # Set FPS limit to 6
    video_capture.set(cv2.CAP_PROP_FPS, 6) 
    
    while True:
            ret, frame = video_capture.read()
            frame = cv2.resize(frame, (0, 0), fx=0.45, fy=0.45)
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

                    # append recognized face name to checkIn if not already present
                    if name not in checkIn:
                        checkIn.append(name)
                        checkoutTime = None

                    else: #if present set the checkout time to current time
                        print('This name is already entered')
                        checkoutTime = str(datetime.datetime.now().hour) +':'+ str(datetime.datetime.now().minute) 
                        updateCheckout(1, Date, name, main_[name], checkoutTime)
                        crsr.execute("SELECT * FROM NEWATTENDANCE6")
                        print(crsr.fetchall )


                    if name not in list(main_.keys()): 
                        main_[name] = str(datetime.datetime.now().hour) +':'+ str(datetime.datetime.now().minute)
           
# Inserts data into the Attendance Table in Employee Database
                        try:
                            print('*****')
                            insertData(1, Date, name, main_[name], checkoutTime)
                            crsr.execute("SELECT * FROM NEWATTENDANCE6")
                            print(crsr.fetchall())
                            print(checkIn)
                        
                        #print(main_)
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
                                                str(name) + ' detected!')
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
                    cv2.waitKey(2000)
                    cv2.destroyAllWindows()
                    # notification
                    tkinter.messagebox.showinfo('Notification',
                                                'No face detected.')
                    if cv2.waitKey(5000):
                        break    # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1000):
                break

# Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


# NEW IMAGE FUNCTION()
def newImage(name):
        video_capture = cv2.VideoCapture(-1)
        while True:
        # Grab a single frame of video
            ret, frame = video_capture.read()
            rgb_frame = frame[:, :, ::-1]
            #cv2.imshow('NewFace', frame)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                newpath = f'/home/pi/Prototype1-FaceRec/Dataset/{name}'
                #if not os.path.exists(newpath):
                 #   os.makedirs(newpath)
                for i in range(1, 2):
                    ret, frame = video_capture.read()
                    #time.sleep(3)
                    img_name = "{}.png".format(i)
                    path = f'/home/pi/Prototype1-FaceRec/Dataset/{name}'
                    cv2.imwrite(os.path.join(path, img_name), frame)
                    print("{} written!".format(img_name))
                
                

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

        tk.Label(self.root, text = 'FaceRec', bg= 'Blue', height = 5, width = 40).pack(side = 'top')
        r = tk.Entry(self.root)
        self.root.title(' Face Recognition ')
        r.focus_set()

        #------------ Logo
  # if you want to add any image
       # filename = ImageTk.PhotoImage(Image.open('index.png' ))
        #background_label = tk.Label(self.root, image=filename)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)






    # RECOGNIZE ME BUTTON
        click_recognize = tk.Button(master=self.root, text = 'Recognize Me', height = 3,
                                 bg='Grey', fg = 'Black'  , command= recognizeMe)
        click_recognize.pack(side= 'top')

    # TIME GREETING
        text = tk.Text(self.root, height = 1, width =30)

    # T = tk.Text(root, height=10, width=30)
        text.pack()
        TimeGreeting = compliment()
        text.insert(tk.END, TimeGreeting)
        text.pack(side = 'top')
    
        # mainloop here, shift to bottom later
        self.root.mainloop()

# 0------------NOT REQUIRED ---- ADD LATER
         
        # tk.Label(self.root, text="First Name").pack()
        # e = Entry(self.root)
        # e.pack()
        # e.focus_set()
        # click_button = Button(master=self.root, text='Start',
        #                    bg='Black', fg = 'White' , command=name_portal)
        # click_button.pack(side="top")

# 0------------NOT REQUIRED ---- ADD LATER

    # def name_portal():
    #     def save_name():
    #         name=e.get()
    #         print( name+" is Saved with us.")  
    #         newImage(name)
   
   
    # def EXIT():
    #     try:
    #         cv2.destroyAllWindows()
    #     except Exception as e:
    #         print(e)
#name_portal()
attendanceApp = GUI()
attendanceApp.tkWindow()
# recognizeMe()
# root.mainloop()

# this is the infinite loop that helps in running the GUI application
