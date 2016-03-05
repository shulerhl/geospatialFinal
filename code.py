__author__ = 'Misha Kushnir'

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

def testPlot(path):

    plt.interactive(True)

    img = cv2.imread(path, 0)
    if img.size == 0:
    	print "could not find image"

    edges = cv2.Canny(img,100,200)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]),plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show(block=True)

# assumes point 1 (x1, y1) is the left point
def getAngle(x1, y1, x2, y2):
    xdiff = x2 - x1
    ydiff = y2 - y1
    return math.atan(ydiff/xdiff)

# given list of segments, returns a list of lists of matching segments
def getSegmentsWithMatchingAngleAndPos(segments, tolerance = math.pi/12):

    matchLists = []

    while len(segments) > 0:

        # pick a totally arbitrary reference segment
        referenceSegment = segments[0]
        segments.remove(0)
        matches = [referenceSegment]
        # first sweep (filter just by angle)
        angle = getAngle(referenceSegment)
        for segment in segments:
            a = getAngle(segment)
            if abs(a-angle) < tolerance:
                # second sweep (check angles of both endpoints of candidate segment compared to initial segment,
                # takes position into account)
                angle1 = getAngle(referenceSegment[0], referenceSegment[1], segment[0], segment[1])
                angle2 = getAngle(referenceSegment[0], referenceSegment[1], segment[2], segment[3])
                if abs(angle1-angle) < tolerance and abs(angle2-angle) < tolerance:
                    matches.append(segment)
                    segments.remove(segment)

        matchLists.append[matches]

    return matchLists


# takes an array of segments (x1, y1, x2, y2) that are already
# assumed to be in the same line, in order
def constructPolyline(segments):
    i = 0
    while i < len(segments) - 1:
        first = segments[i]
        next = segments[i+1]

        if first[2] == next[0] and first[3] == next[1]: # x2, y2 from first and x1, y1 from next
            # do nothing, these two segments are already connected
            i += 1
        else: # insert connecting segment
            segment = [first[2], first[3], next[0], next[1]]
            segments.insert(i+1, segment)
            i += 1

    return segments


if __name__=="__main__":
    #testPlot("../cube/7350.jpg")
    print getAngle(0,0,1,2)
    print getAngle(0,0,1,-1)

    segments = [[0,0,1,1], [1,1,2,3], [3,4,5,5]]
    print constructPolyline(segments)
