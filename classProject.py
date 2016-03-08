__author__ = 'Misha Kushnir'
import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
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
    return math.atan(float(ydiff)/float(xdiff))
    

# given list of segments, returns a list of lists of matching segments
def getSegmentsWithMatchingAngleAndPos(segments, tolerance = math.pi/36):

    matchLists = []

    while len(segments) > 0:

        # pick a totally arbitrary reference segment
        referenceSegment = segments[0]
        # print segments
        segments = np.delete(segments,0,0)
        matches = [referenceSegment]
        # first sweep (filter just by angle)
        angle = getAngle(referenceSegment[0],referenceSegment[1],referenceSegment[2],referenceSegment[3])
        # print len(segments)
        # print segments
        for segment in segments:
            # print len(segments)
            # print segment
            a = getAngle(segment[0],segment[1],segment[2],segment[3])
            if abs(a-angle) < tolerance:
                # second sweep (check angles of both endpoints of candidate segment compared to initial segment,
                # takes position into account)
                angle1 = getAngle(referenceSegment[0], referenceSegment[1], segment[0], segment[1])
                angle2 = getAngle(referenceSegment[0], referenceSegment[1], segment[2], segment[3])
                if abs(angle1-angle) < tolerance and abs(angle2-angle) < tolerance:
                    matches.append(segment)
                    # remove segment from segments
                    segments = segments[(segments != segment).any(axis=1)]
                    #segments = np.delete(segments,np.where(segments==segment),0)

        matchLists.append(np.array(matches))

    return np.array(matchLists)


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
            segments = np.insert(segments,i+1, segment,0)
            i += 1

    return segments

# simple merge sort that sorts a list of segments by the X value of their first point
# still have to rewrite for np.array
def sortSegmentsByX(segments):

    length = len(segments)

    print "Length: " + str(length)

    if length == 1:
        return segments
    else:
        pivot = length/2
        print "Pivot: " + str(pivot)

        left = sortSegmentsByX(segments[0:pivot])
        right = sortSegmentsByX(segments[pivot:length])

        sorted = []

        print "Left: " + str(left)
        print "Right: " + str(right)

        while len(left) > 0 or len(right) > 0:
            if len(left) == 0:
                firstRight = right[0]
                sorted.append(firstRight)
                right = np.delete(right, 0, 0)
            elif len(right) == 0:
                firstLeft = left[0]
                sorted.append(firstLeft)
                left = np.delete(left, 0, 0)
            else:
                firstLeft = left[0]
                firstRight = right[0]

                if (firstLeft[0] < firstRight[0]):
                    sorted.append(firstLeft)
                    left = np.delete(left, 0, 0)
                else:
                    sorted.append(firstRight)
                    right = np.delete(right, 0, 0)

        return np.array(sorted)


if __name__=="__main__":
    #testPlot("../cube/7350.jpg")
    #print getAngle(0,0,1,2)
    #print getAngle(0,0,1,-1)

    a = np.array([1,2,3,4,5])
    segments = np.array([[0,0,1,1], [1,1,2,2], [0,0,3,5], [0,0,1,0], [0,3,1,2], [2,1,3,0], [4,0,5,0], [9,15,12,20]])
    print "\n\n"
    print getSegmentsWithMatchingAngleAndPos(segments)
