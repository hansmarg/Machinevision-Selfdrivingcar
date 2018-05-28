import sys
import tensorflow as tf
import numpy as np
import cv2 as cv


def 



if __name__ == "__main__":

	grad_x, grad_y = 1,1
	sobel_image = None
	image = cv.imread("easy.jpg")

	cv.imshow("image",image)
	cv.waitKey()

	pts_src = np.array([(803, 666), (1154, 666), (1910, 970), (236, 973)])
	pts_dst = np.array([(0, 0), (600, 0), (600, 600), (0, 600)])



	h, status = cv.findHomography(pts_src, pts_dst)			#
	im_dst = cv.warpPerspective(image.copy(), h, (600,600))	#	generate and show homographic transform from original to warped
	cv.imshow('perspective', im_dst)						#
	cv.waitKey(0)											#




	h, status = cv.findHomography(pts_dst, pts_src)						#
	im_org_warped = cv.warpPerspective(im_dst.copy(), h, (1920,1200))	#	generate and show homographic transform from warped to original
	cv.imshow("im_org_warped", im_org_warped)							#
	cv.waitKey(0)														#


#	sobel_image	= cv.GaussianBlur( image, (7,7), 2, sobel_image, 2, cv.BORDER_DEFAULT)


#	sobel_image	= cv.Sobel(	image, cv.CV_64F, grad_x, grad_y, sobel_image, ksize = 3, scale = 1, delta = 0, borderType = cv.BORDER_DEFAULT)


'''	


################################


img_path = './easy.jpg'
#img_path = sys.argv[1]
img = cv.imread(img_path)

if img is None:
    print ("could not load image: "+img_path)
    exit(1)

org_img = img.copy()

points = []

def event_handler(event, x, y, flags, param):
    global points
    if event == cv.EVENT_LBUTTONDOWN:
        img = org_img.copy()
        points.append((x, y))
        create_polygon(img, points)
        cv.imshow('image', img)

    elif event == cv.EVENT_LBUTTONUP:
        print("up nigguh", x, y, flags, param)


def create_polygon(img, fig):
    points = fig[:]
    if len(points) <= 1:
        return

    points.append(points[0])
    a = points[0]
    for b in points[1:]:
        cv.line(img, a, b, (255,0,0), 5)
        a = b

def my_resize(img, axis1):
    r = float(axis1) / img.shape[1]
    dim = (axis1, int(img.shape[0] * r))
    return cv.resize(img, dim, interpolation = cv.INTER_AREA)

# add window
cv.namedWindow("image", cv.WINDOW_NORMAL)
cv.namedWindow("perspective", cv.WINDOW_NORMAL)
cv.setMouseCallback("image", event_handler)

# add trapazoid and show image
fig = [(803, 666), (1154, 666), (1910, 970), (236, 973)]
create_polygon(img, fig)
#cv.imshow('image', my_resize(img, 900))
cv.imshow('image', img)
#cv.waitKey(0)

# do homography shit
pts_src = np.array([(803, 666), (1154, 666), (1910, 970), (236, 973)])
pts_dst = np.array([(0, 0), (600, 0), (600, 600), (0, 600)])
h, status = cv.findHomography(pts_src, pts_dst)
im_dst = cv.warpPerspective(org_img.copy(), h, (600,600))
cv.imshow('perspective', im_dst)
cv.waitKey(0)

# add square and show image
#img = org_img.copy()
#fig = [(340, 120), (840, 120), (840, 620), (340, 620)]
#create_polygon(img, fig)
#cv.imshow('image',img)
#cv.waitKey(0)

# do homography shit
pts_src = np.array(points)
pts_dst = np.array([(0, 0), (600, 0), (600, 600), (0, 600)])
h, status = cv.findHomography(pts_src, pts_dst)
im_dst = cv.warpPerspective(org_img.copy(), h, (600,600))
cv.imshow('perspective', im_dst)
cv.waitKey(0)

# destroy all windows
cv.destroyAllWindows()


'''