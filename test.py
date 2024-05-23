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

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read video frame.")
        exit()

    # Detect Rim
    rim_roi = cv2.selectROI('Select ROI around rim', frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow('Select ROI around rim')

    makes = 0
    misses = 0

    rim_roi = tuple(map(int, rim_roi))
    roi_frame = frame[rim_roi[1]:rim_roi[1] + rim_roi[3], rim_roi[0]:rim_roi[0] + rim_roi[2]]
    roi_frame_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    initial_avg_pixel_value = cv2.mean(roi_frame_gray)[0]

    frame_counter = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_counter += 1

        # Shot Name Text
        position = (0, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 0, 255)
        thickness = 2
        text = key

        cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

        # Detect Shots
        if frame_counter % 10 == 0:
            roi_frame = frame[rim_roi[1]:rim_roi[1] + rim_roi[3], rim_roi[0]:rim_roi[0] + rim_roi[2]]
            roi_frame_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

            avg_pixel_value = cv2.mean(roi_frame_gray)[0]

            if avg_pixel_value < initial_avg_pixel_value - 10:
                makes += 1
            elif avg_pixel_value < initial_avg_pixel_value - 2:
                misses += 1

        position = (0, 100)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 0, 255)
        thickness = 2
        text = f"Makes - {makes}, Misses - {misses}"

        cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

        # Play Video
        cv2.imshow(key, frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"For {key}: Makes - {makes}, Misses - {misses}")