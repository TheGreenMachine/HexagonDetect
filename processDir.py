import argparse
import cv2
import numpy as np
import math
import glob
import shutil
import os

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
def procImage(img, shape, name):
    edges = cv2.Canny(img, 100, 300)
    match = 100
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
            # .0165 if not working
            if match < .0165:

                cx = rect[0] + (rect[2] * .5)
                cy = rect[1] + (rect[3] * .5)
                centerpoints = (cx, cy)
                print(f"len(cont)={len(cont):3d}:  match={match:.4f}")
                hexes.append(cont)
                print("Moved")
                img = cv2.drawContours(img, hexes, -1, (0, 255, 0), 4)
                ctr = np.array(centerpoints).reshape((-1, 1, 2)).astype(np.int32)
                img = cv2.drawContours(img, ctr, -1, (0, 255, 0), 20)
                shutil.move(file, os.path.dirname(os.path.abspath(file)) + "/FOUNDTARGETS")
                break


    return img
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("--source", default=0,
                        help="Input Source")
    args = parser.parse_args()
    hex = make_hex_shape()
    print(args)
    files = glob.glob(args.source + "/*.JPG")
    print(files)
    cv2.namedWindow("edges")
    for file in files:
        img = cv2.imread(file)
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        img = procImage(img, hex, file)
        cv2.imshow("contours", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break