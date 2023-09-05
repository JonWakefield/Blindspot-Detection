import sys
import random
import pygame
# import re
# import obd
import RPi.GPIO as GPIO
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
import cv2
from PyQt5.QtCore import Qt, QTimer

left = 27 #top two gpio pcb socket
right = 25 # bottom two gpio pcb socket
left45 = 22 # bottom two gpio pcb socket
right45 = 26 #top two gpio pcb socket

# Set up GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(left, GPIO.IN)
GPIO.setup(right, GPIO.IN) 
GPIO.setup(left45, GPIO.IN)
GPIO.setup(right45, GPIO.IN)


# Initlize our users score
user_score = 0
total_possible_score = 0
score_percentage = 0 

# Load the cascade classifiers for face and eye detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Set up the video capture
cap = cv2.VideoCapture(0)

# obd_connection = obd.OBD()




def update_score(num_eyes_detected: int, user_score:int, total_possible_score: int):
    """
        Scoring System: Represented as a percentage.

        Both eyes: +2
        One Eye: +1
        No eyes: +0

        +2 is added to total_possible_score regardless of eyes

    """

    # Need to determine the number of eyes detected:

    if(num_eyes_detected >= 2):
        user_score += 2
    elif(num_eyes_detected == 1):
        user_score += 1

    # Automatically add two to total score:
    total_possible_score += 2

    return user_score, total_possible_score


def facial_tracker():

    global user_score, total_possible_score, score_percentage

    # Initialize variables for eye tracking
    eye_x, eye_y = 0, 0
    prev_eye_x, prev_eye_y = 0, 0

    x = 0

    while True:
        # sleep(0.1)
        # Read the current frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except (Exception) as e:
            print(e)
            return 0

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Loop through each detected face
        # TODO: Only want to detect one face.
        # How can we make sure the face we detect is the driver
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extract the region of interest (ROI) which is the face
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Detect eyes in the face ROI
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Loop through each detected eye
            # We enter here when eye or eyes has been detected:
            #TODO: only grab first two eyes. (need to make sure eyes grabbed are the correct ones)

            for (ex, ey, ew, eh) in eyes:
                # Draw a rectangle around the eye
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

                # Calculate the center of the eye
                eye_x = int(x + ex + ew/2)
                eye_y = int(y + ey + eh/2)

                # Draw a circle at the center of the eye
                cv2.circle(frame, (eye_x, eye_y), 2, (0, 0, 255), 2)


        # Calculate the movement of the eye from the previous frame
        eye_movement_x = eye_x - prev_eye_x
        eye_movement_y = eye_y - prev_eye_y


        # After identifying and displaying eyes update the users score:
        try:
            if(eye_movement_x == 0 and eye_movement_y == 0):
                num_of_eyes_detected = 0 
            else:
                num_of_eyes_detected = eyes.shape[0]

            user_score, total_possible_score = update_score(num_of_eyes_detected, user_score, total_possible_score)
            # user_score = scores_tuple[0]
            # total_possible_score = scores_tuple[1]

            score_percentage = (user_score / total_possible_score) * 100

            
        except(NameError, AttributeError) as e:
            pass

        # Print the eye movement to the console
        # print(f"Eye movement: ({eye_movement_x}, {eye_movement_y})")

        # Update the previous eye position
        prev_eye_x, prev_eye_y = eye_x, eye_y

        # Display the frame
        # cv2.imshow('Eye Tracking', frame)

        # Check if the user has pressed the 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # x+= 1
        return score_percentage

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

    return score_percentage




class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the layout
        CCol = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        self.setLayout(hbox)

        # Set up the labels
        self.left_arrow = QLabel(self)
        self.right_arrow = QLabel(self)
        self.driver_score = QLabel(self)
        self.Score_label = QLabel(self)
        self.speed_label = QLabel(self)
        self.speed = QLabel(self)

        # Set up the images
        self.LeftEmp = QPixmap('LeftEmpty.png').scaled(300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation) #300,1000
        self.RightEmp = QPixmap('RightEmpty.png').scaled(300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.LeftRed = QPixmap('LeftRed.png').scaled(300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.RightRed = QPixmap('RightRed.png').scaled(300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        
        # Driver Score and its label
        self.Score_label.setAlignment(Qt.AlignCenter)
        self.Score_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.Score_label.setText('Attentiveness\n Score')
        self.driver_score.setAlignment(Qt.AlignCenter)
        self.driver_score.setStyleSheet("font-size: 100px; font-weight: bold;")
        
        # add speed
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.speed_label.setStyleSheet("font-size: 40px; font-weight: bold;")
        self.speed_label.setText('MPH')
        self.speed.setAlignment(Qt.AlignCenter)
        self.speed.setStyleSheet("font-size: 80PX; font-weight: bold;")

        # make the center column layout
        CCol.addWidget(self.Score_label)
        CCol.addWidget(self.driver_score)
        CCol.addWidget(self.speed)
        CCol.addWidget(self.speed_label)
        CCol.setSpacing(1)

        # Set up the GUI layout
        hbox.addWidget(self.left_arrow)
        hbox.addStretch(1)
        hbox.addLayout(CCol)
        hbox.addStretch(1)
        hbox.addWidget(self.right_arrow)
        hbox.setSpacing(5)
        vbox.addLayout(hbox)

        # Set up the timer to update the number label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_number)
        self.timer.start(500)

        # Set up the window
        self.setWindowTitle('Driver Score and speed')
        self.setGeometry(1, 50, 600, 600)


        self.update_left_image()
        self.update_right_image()
        GPIO.add_event_detect(left, GPIO.BOTH, callback=self.update_left_image)
        GPIO.add_event_detect(right, GPIO.BOTH, callback=self.update_right_image)
        GPIO.add_event_detect(left45, GPIO.BOTH, callback=self.update_left_image)
        GPIO.add_event_detect(right45, GPIO.BOTH, callback=self.update_right_image)

        self.show()

    def update_number(self):

        user_score_percent = facial_tracker()

        score_str = f"{user_score_percent:.1f}%"

        self.driver_score.setText(score_str)

        # self.driver_score.setText(score_str)
        speed_mph = "00"
        self.speed.setText(speed_mph)
    
        
        
        

    def update_left_image(self, channel=None):
        if GPIO.input(left) or GPIO.input(left45):
            self.left_arrow.setPixmap(self.LeftRed)
            pygame.mixer.music.load("Left.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        else:
            self.left_arrow.setPixmap(self.LeftEmp)
            
    def update_right_image(self, channel=None):
        if GPIO.input(right) or GPIO.input(right45):
            self.right_arrow.setPixmap(self.RightRed)
            pygame.mixer.music.load("Right.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        else:
            self.right_arrow.setPixmap(self.RightEmp)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pygame.mixer.init()
    ex = MyWidget()
    ex.showFullScreen()
    sys.exit(app.exec_())
    # obd_connection.close()
