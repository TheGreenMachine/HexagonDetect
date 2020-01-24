import cv2

img2 = cv2.imread('image2.png', cv2.IMREAD_COLOR)

img = cv2.imread('image2.png', cv2.IMREAD_GRAYSCALE)
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
            cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)


cv2.imshow('image2', img2)


if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()