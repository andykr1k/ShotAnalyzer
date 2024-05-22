import cv2
import os

shots = {}

directory = './data/videos/'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    file_name_without_ext, _ = os.path.splitext(filename)
    shots[file_name_without_ext] = file_path


for key, value in shots.items():
    cap = cv2.VideoCapture(value)

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        position = (0, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 0, 255)
        thickness = 2
        text = key

        cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow('Video', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()