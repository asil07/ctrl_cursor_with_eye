import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) # to get eye landmarks
                                                                    # refine_landmarks true
# to get screen size
screen_w, screen_h = pyautogui.size()

while True:
    grabbed, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_img)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark

        # looping through to draw circle on detected face landmarks
        for id, landmark in enumerate(landmarks[474:478]):  # 474 : 478 landmarks for eye
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            # to move cursor
            if id == 1:
                # to get proper ratio of screen and mouse
                screen_x = int(landmark.x * screen_w)
                screen_y = int(landmark.y * screen_h)
                pyautogui.moveTo(screen_x, screen_y)
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            cv2.circle(frame, (x, y), 3, (0, 0, 255))

        # to detect winks we need difference of two landmarks below
        if (left[0].y - left[1].y) < 0.01:
            pyautogui.click()
            print("click")
            pyautogui.sleep(1)


    cv2.imshow("EYe controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break