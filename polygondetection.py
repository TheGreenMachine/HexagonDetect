import cv2

cap = cv2.VideoCapture("test.mp4")
while True:
    retr, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img, 100, 300)

    #_, threshold = cv2.threshold(img, 100, 255,cv2.THRESH_BINARY)
    cv2.imshow('thres', img)

    contours, _ = cv2.findContours(img, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Shortlisting the regions based on there area.
        if area > 100:
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
            if (len(approx) == 6):
                cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)
                print("DRAW")


    cv2.imshow('image2', img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()