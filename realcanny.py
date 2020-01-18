import argparse
import torch
import torchvision
import cv2
from torch.autograd import Variable
import numpy as np
import math

lowerbound = 0
# create an array of points in the shape of a hexagon

def sliderUpdate(val):
    global lowerbound
    lowerbound = val
    print(lowerbound)
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
def procImage(img, shape, val):
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
            if match < 0.08:
                print("SKIP")
            if match < .0165:
                cx = rect[0] + (rect[2] * .5)
                cy = rect[1] + (rect[3] * .5)
                centerpoints = (cx, cy)
                print(f"len(cont)={len(cont):3d}:  match={match:.4f}")
                hexes.append(cont)
    img = cv2.drawContours(img, hexes, -1, (0, 255, 0), 4)
    ctr = np.array(centerpoints).reshape((-1, 1, 2)).astype(np.int32)
    img = cv2.drawContours(img, ctr, -1, (0, 255, 0), 20)
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

    cap = cv2.VideoCapture(src)
    if args.save:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
    cv2.namedWindow("edges")
    cv2.createTrackbar("lower", "edges", 0, 100, sliderUpdate)
    while True:
        retr, img = cap.read()
        img = img[0:360, 0:1280]

        img = procImage(img, hex, lowerbound)
        if args.save:
            out.write(img)
        cv2.imshow("contours", img)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()