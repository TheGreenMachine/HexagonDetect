import argparse
import cv2
import numpy as np
import math

oldframe = 0
count = 0
def make_hex_shape():
    pts = []
    for ang in range(0, 355, 60):
        ang_r = math.radians(ang)
        x1 = int(100.0 * math.cos(ang_r) + 100.5)
        y1 = int(100.0 * math.sin(ang_r) + 100.5)
        pts.append([x1, y1])
    shape_np = np.array(pts, np.int32)
    shape_np = np.reshape(shape_np, (-1, 1, 2))
    return shape_np
def procImage(img):
    global oldframe, count, centerframex, centerframey, cx, cy
    centerframey = img.shape[0] * 0.5
    centerframex = img.shape[1] * 0.5
    edges = cv2.Canny(img, 100, 300)

    cv2.imshow("edges", edges)
    edges = np.uint8(edges * 255)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    centerpoints = []
    hexes = []
    for cont in contours:
        rect = cv2.boundingRect(cont)
        # only process larger areas with at least 5 points in the contour
        if len(cont) > 80 and rect[2] > 55 and rect[3] > 55:
            match = cv2.matchShapes(cont, hex, cv2.CONTOURS_MATCH_I2, 0.0)
            if 0.01 < match < 1:
                print("SKIP")
                if oldframe == 0:
                    continue
                img = cv2.drawContours(img, oldframe[0], -1, (0, 255, 0), 3)
                img = cv2.drawContours(img, oldframe[1], -1, (0, 0, 255), 20)
                cv2.line(img, (int(cx), int(cy)), (int(centerframex), int(centerframey)), (0, 0, 255), thickness=5)
                if count > 2:
                    oldframe = 0
                    count = 0
                count += 1
                return img


            # .0165 if not working
            if match < .01:
                print(count)
                count = 0
                cx = rect[0] + (rect[2] * .5)
                cy = rect[1] + (rect[3] * .5)
                centerpoints = (cx, cy)
                print(f"len(cont)={len(cont):3d}:  match={match:.4f}")
                hexes.append(cont)
                img = cv2.drawContours(img, hexes, -1, (0, 255, 0), 3)
                ctr = np.array(centerpoints).reshape((-1, 1, 2)).astype(np.int32)
                img = cv2.drawContours(img, ctr, -1, (0, 0, 255), 20)
                line = cv2.line(img, (int(cx), int(cy)), (int(centerframex), int(centerframey)), (0, 0, 255), thickness=5)

                oldframe = [hexes, ctr, line]

    return img
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("--source", default=0,
                        help="Input Source")
    parser.add_argument("--save", action="store_true", help="save video to file")
    args = parser.parse_args()
    src = 0
    out = 0

    hex = make_hex_shape()
    print(args)
    if args.source != None:
        src = args.source

    cap = cv2.VideoCapture("autovideosrc ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
    if args.save:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
    cv2.namedWindow("edges")
    while True:
        retr, img = cap.read()
        # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        # img = cv2.resize(img, None, fx=0.25, fy=0.25)
        img = img[0:360, 0:1280]
        img = procImage(img)
        if args.save:
            out.write(img)
        cv2.imshow("contours", img)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
