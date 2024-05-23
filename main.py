import cv2

cap = cv2.VideoCapture('./data/videos/final.mov')

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
    text_name = "Shot Analyzer"

    cv2.putText(frame, text_name, position, font, font_scale, color, thickness, cv2.LINE_AA)

    # Detect Shots
    if frame_counter % 4 == 0:
        roi_frame = frame[rim_roi[1]:rim_roi[1] + rim_roi[3], rim_roi[0]:rim_roi[0] + rim_roi[2]]
        roi_frame_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        avg_pixel_value = cv2.mean(roi_frame_gray)[0]

        if avg_pixel_value < initial_avg_pixel_value - 5:
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
    cv2.imshow(text_name, frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()