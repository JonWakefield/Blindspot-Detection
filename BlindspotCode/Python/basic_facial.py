import cv2

# Use Haarcascade classifier for facial recognition
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# If unable to open / locate file, end program
if face_cascade.empty():
    raise IOError('Unable to load the face cascade classifier xml file')

# Set the frame counter and frame skip interval
frame_counter = 0
frame_skip = 5

# Open webcam capture
cap = cv2.VideoCapture(0)

while True:

    # Read in the image
    _, img = cap.read()
    

    # Convert img to grayscale to allow for face classification
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # use face_cascade to look for faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # If theres a face, draw a square around it
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    


    # Display the frame
    cv2.imshow('Face detection', img)


    # Stop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break


# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()