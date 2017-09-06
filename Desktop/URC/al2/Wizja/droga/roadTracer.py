import cv2
from cv2 import imread, imshow, waitKey
import numpy as np


def getCanny(img, draw=True):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, 100, 200)
    if draw:
        imshow("canny", edges)
    return edges


imgsPath = "imgs\\"

img = imread(imgsPath + "1.jpg")
imshow("orginal", img)

contursImg = np.zeros(img.shape, np.uint8)

edges = getCanny(img)

im2, conturs, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(contursImg, conturs, -1, (0, 255, 0), 2)
imshow("conturs", contursImg)

kernel = np.ones((3, 3), np.uint8)
contursImg = cv2.cvtColor(contursImg, cv2.COLOR_BGR2GRAY)
openedEdges = cv2.morphologyEx(contursImg, cv2.MORPH_HITMISS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_HITMISS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_CLOSE, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_CROSS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_CROSS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_HITMISS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_HITMISS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_HITMISS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_CROSS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_CROSS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_CROSS, kernel)
openedEdges = cv2.morphologyEx(openedEdges, cv2.MORPH_CROSS, kernel)
imshow("opened", openedEdges)
#
# for i in range(0, 1):
#     openedEdges = cv2.blur(openedEdges, (7, 7))
# imshow("openedEdges blured", openedEdges)
#
# contursImg2 = np.zeros(img.shape, np.uint8)
# im2, conturs, hierarchy = cv2.findContours(openedEdges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(contursImg2, conturs, -1, (0, 255, 0), -1)
# imshow("conturs of openEdges blured", contursImg2)

lineImg = img.copy()
# gray = cv2.cvtColor(openedEdges, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(openedEdges, 50, 150, apertureSize=3)
minLineLength = 10
maxLineGap = 1
lines = cv2.HoughLinesP(openedEdges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
for x1, y1, x2, y2 in lines[0]:
    cv2.line(lineImg, (x1, y1), (x2, y2), (0, 255, 0), 2)
imshow("lineImg", lineImg)

waitKey(0)
