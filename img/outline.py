import cv2

img_origin = cv2.imread('1.png')
# cv2.imshow('origin', img_origin)

img_gray = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray', img_gray)

img_blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
#cv2.imshow('blurred', img_blurred)

img_threshold1 = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)
#cv2.imshow('img_threshold1', img_threshold1)

img_threshold1_blurred = cv2.GaussianBlur(img_threshold1, (5, 5), 0)
#cv2.imshow('img_threshold1_blurred', img_threshold1_blurred)

_, img_threshold2 = cv2.threshold(img_threshold1_blurred, 200, 255, cv2.THRESH_BINARY)
#cv2.imshow('img_threshold2', img_threshold2)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
img_opening = cv2.bitwise_not(cv2.morphologyEx(cv2.bitwise_not(img_threshold2), cv2.MORPH_OPEN, kernel))
#cv2.imshow('img_opening', img_opening)

img_opening_blurred = cv2.GaussianBlur(img_opening, (3, 3), 0)
cv2.imshow('img_opening_blurred', img_opening_blurred)

cv2.waitKey(0)
cv2.destroyAllWindows()