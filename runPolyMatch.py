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
    for image in images:

        in_img = cv2.imread(image, 0)
        r_img = cv2.imread(image, 0)

        #polyLineMatch(in_img, r_img)

        print("COMPLETED THE", str(i), "IMAGE")
        i+= 1

    print("done")


if __name__ == "__main__":
    runPM()
