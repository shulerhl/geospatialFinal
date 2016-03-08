import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
from classProject import testPlot, getSegmentsWithMatchingAngleAndPos, constructPolyline, sortSegmentsByX


def houghT(input_img, run_img, img_edges, h_array):
	h_lines = cv2.HoughLinesP(img_edges, 1, np.pi/180, 80, 30000, 45)
	if h_lines.size == 0:
		print("Hough found no lines")
	else:
		#[r,c] = input_img.shape()
		print("LINES SIZE", h_lines.shape)
		print(str(h_lines))

	h_lines = removeHoriz(h_lines)
	h_lines = makeLines(h_lines)
	# print h_lines
	for h in h_lines:
		for x1,y1,x2,y2 in h:
		    cv2.line(h_array,(x1,y1),(x2,y2),(0,255,0),2)
	cv2.imwrite('houghlines3.jpg', h_array)
	return h_lines


def removeHoriz(houghL):
	h_lines = houghL[0]
	length = len(h_lines)
	print("SHAPEEE")
	print(h_lines.shape)
	good_lines = []
	#xHalf = 2048/2  #change 2048 to image size dimensions

	for i in range(0,length):
		currSeg = h_lines[i]
		print("YOOOOO")
		print(str(currSeg))
		currAngle = getAngle(currSeg[0], currSeg[1], currSeg[2], currSeg[3])
		currDist = math.sqrt(math.pow((currSeg[2] - currSeg[0]) , 2) + math.pow((currSeg[2] - currSeg[0]), 2))
		print("CURR ANGLE", str(currAngle))
		if (abs(currAngle) > math.pi/12):
			good_lines.append(h_lines[i])
	return np.array(good_lines)


def getAngle(x1, y1, x2, y2):
	xdiff = x2 - x1
	ydiff = y2 - y1
	return math.atan(float(ydiff)/xdiff)

def makeLines(h_lines):
    lines_segments = getSegmentsWithMatchingAngleAndPos(h_lines)
    ls_length = len(lines_segments)
    sorted_segments = []
    for segment_group in lines_segments:
        sorted_group = sortSegmentsByX(segment_group)
        sorted_segments.append(sorted_group)
    # print ls_length, len(sorted_segments)
    final_lines = []
    for row in sorted_segments:
        final_lines.append(constructPolyline(row))
    return np.array(final_lines)


def displayIMG(input_img, img_edges, output_img_h):
    input_fig = plt.figure(1)
    # plt.subplot(221)
    plt.imshow(input_img, cmap='gray')
    plt.title('Original Image')
    plt.xticks([]), plt.yticks([])
    input_fig.show()

    edge_fig = plt.figure(2)
    # plt.subplot(222)
    plt.imshow(img_edges, cmap='gray')
    plt.title('Edge Image')
    plt.xticks([]), plt.yticks([])
    edge_fig.show()

    # plt.subplot(223)
    h_fig = plt.figure(3)
    plt.imshow(output_img_h, cmap='gray')
    plt.title('Hough Lines Image')
    plt.xticks([]), plt.yticks([])
    h_fig.show()

    # KEEP IMAGES OPEN
    print("Press any character and enter to close")
    raw_input()

    return 0


def polyLineMatch(input_img, run_img):
    h_array = np.ones((2048, 2048))

    if input_img.size == 0:
        print("Could not find image")
    else:
        print(" IMAGE SIZE", input_img.shape)

    kernel = np.ones((10, 10), 'uint8')
    input_img = cv2.dilate(input_img, kernel)
    run_img = cv2.dilate(run_img, kernel)
    # input_img = cv2.equalizeHist(input_img)
    # run_img = cv2.equalizeHist(run_img)
    # input_img = scipy.ndimage.morphology.binary_dilation(input_img)
    # input_img = np.array(input_img, dtype=np.uint8)
    # edge detection
    img_edges = cv2.Canny(run_img, 100, 250, 5)
    if img_edges.size == 0:
        print("Canny found no edges")
    else:
        # [r,c] = input_img.shape()
        print("EDGES SIZE", img_edges.shape)

    # img_edges2 = scipy.ndimage.morphology.binary_dilation(img_edges, iterations=1)
    # img_edges2 = np.array(img_edges2, dtype=np.uint8)
    kernel = np.ones((4, 4), 'uint8')
    img_edges2 = cv2.dilate(img_edges, kernel)
    hough_lines = houghT(input_img, run_img, img_edges2, h_array)
    # hough_lines = houghT(input_img, run_img, img_edges, h_array)
    output_img_h = cv2.imread('houghlines3.jpg', 0)
    # output_img_h = scipy.ndimage.morphology.binary_dilation(output_img_h, iterations=2)
    # print abs(output_img_h - 1)
    kernel = np.ones((2, 2), 'uint8')
    output_img_h = abs(output_img_h - 1)
    # th, output_img_h = cv2.threshold(output_img_h,250,255,cv2.THRESH_BINARY)
    output_img_h = cv2.dilate(output_img_h, kernel)
    # output_img_h = np.array(output_img_h, dtype=np.uint8)
    d = displayIMG(input_img, img_edges2, output_img_h)
    return 0


if __name__ == "__main__":
    input_img = cv2.imread('cube/7360.jpg', 0)
    run_img = cv2.imread('cube/7360.jpg', 0)
    polyLineMatch(input_img, run_img)
