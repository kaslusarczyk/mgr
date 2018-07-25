import cv2
import sys
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

person_name = sys.argv[1]
faces_collection_path = os.environ['FACES_COLLECTION_PATH']
dest_size = (200, 200)

for picture_number in range(0, 5):
    img = cv2.imread(faces_collection_path + person_name + '/photos/' + person_name + '_' + str(picture_number)
                     + '.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        roi_color = cv2.resize(roi_color, dest_size)
        cv2.imwrite(faces_collection_path + person_name + '/photos/' + person_name + '_faces/' + person_name + '_'
                    + str(picture_number) + '_face.jpg', roi_color)
