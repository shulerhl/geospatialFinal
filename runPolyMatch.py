import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import os
import glob
from classProject import testPlot, getSegmentsWithMatchingAngleAndPos, constructPolyline
from findPoly import polyLineMatch

def runPM():
    curr_dir = os.getcwd()
    dir_jpg = str(curr_dir) + '/cube/*.jpg'
    #print(str(dir_jpg))
    images = glob.glob(dir_jpg)
    im_len = len(images)
    #print("LENGTH")
    #print(str(im_len))
    i = 0
    polyLines = []
    for image in images:

        in_img = cv2.imread(image, 0)
        r_img = cv2.imread(image, 0)

        currLine = polyLineMatch(in_img, r_img)
        polyLines.append(currLine)
        #writeCSV(currLine)
        print("COMPLETED THE", str(i), "IMAGE")
        i+= 1
    writeCSV(polyLines)
    print("done")

def writeCSV(pl, filename = "PolyLinesGeoFinal.csv"):

    f = open(filename, 'w')
    for image in pl:
        f.write("  ".join("NEW IMAGE") + "\n")
        for line in image:
            p = line
            p = [str(item) for item in p]

            f.write(",".join(p) + "\n")

    f.close()
    return 0

if __name__ == "__main__":
    runPM()
