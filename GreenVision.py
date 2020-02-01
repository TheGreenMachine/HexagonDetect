import cv2

# 2020 Green Machine main vision processing script
# Used to detect retroreflective tape


lower_color = (60, 106, 150)
upper_color = (130, 255, 255)

cap = cv2.VideoCapture("/home/ianmcvann/PycharmProjects/HexagonDetect/Test Videos/Left_Frame.avi")

while True:
    retr, frame = cap.read()
    frame = frame[0:360, 0:1280]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    cv2.imshow("test", mask)
    cv2.waitKey(1)