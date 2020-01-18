import argparse
import cv2

edge_params = {
    'min_val': 200,
    'max_val': 300,
    'aperture_size': 3
}
gray = None

def min_change(new_val):
    change_params('min_val', new_val)

def max_change(new_val):
    change_params('max_val', new_val)

def change_params(name, value):
    global edge_params
    edge_params[name] = value
    print(edge_params)
    redraw_edges()

def redraw_edges():
    edges = cv2.Canny(gray,
                      edge_params['min_val'],
                      edge_params['max_val'],
                      edge_params['aperture_size'])
    cv2.imshow('Edges', edges)

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', default='fb_profile.jpg',
                    help='Image to use for edge detection')
    args = vars(ap.parse_args())
    file_name = args['image']
    image = cv2.imread(file_name)
    image = cv2.resize(image, None, fx=0.5, fy=0.5)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow('Original')
    cv2.createTrackbar('Min', 'Original', 0, 800, min_change)
    cv2.createTrackbar('Max', 'Original', 100, 800, max_change)
    cv2.imshow('Original', image)
    redraw_edges()

    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            exit()