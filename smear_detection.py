#!/usr/bin/env python
import numpy as np
import cv2
import glob
import sys
import scipy.ndimage as scpy
from skimage.filter import threshold_adaptive

#function to find the Average image
def average_images(path,n):

  first_img=cv2.imread(glob.glob(path + '/*.jpg')[0],0)
  avg =np.zeros(first_img.shape,np.float)     #float for accumulated function, uint8 for normal addition
  i =0

  for image_path in glob.glob(path + '/*.jpg'):
    print i#For getting the status in terminal
    i=i+1
    img = cv2.imread(image_path,0)
    blur = cv2.blur(img, (5,5),0)
    if True:#np.sum(img)<507000000 and np.sum(img)>410000000:
        cv2.accumulateWeighted(img,avg,0.01)
        res = cv2.convertScaleAbs(avg)

    #For testing
    if i>500:
        break
  return res

def path_array(path):

  i = []
  for image_path in glob.glob(path + '/*.jpg'):
    i.append(image_path)
  i.sort()
  return i





def subtract(path,n):

    first_img=cv2.imread(glob.glob(path + '/*.jpg')[0],0)
    avg =np.zeros(first_img.shape,np.float)     #float for accumulated function, uint8 for normal addition
    diff =np.zeros(first_img.shape,np.float)
    sum =np.zeros(first_img.shape,np.float)
    i =0

    for image_path in glob.glob(path + '/*.jpg'):
        print i#For getting the status in terminal

        if i%2==0:
            img1 =  cv2.imread(image_path,0)
        else:
            img2 =  cv2.imread(image_path,0)

            diff=cv2.subtract(img1,img2)
            if i==1:
                sum=diff*0.00001
            # display(diff,'difference')

        cv2.accumulateWeighted(diff,avg,0.01)
        res = cv2.convertScaleAbs(avg)
        if i>1:
            sum=cv2.add(sum,diff*0.00001)

        display(sum,'res')
        i+=1
        #For testing
        # if i>500:
        #     break
    cv2.imwrite('output2.jpg',sum)
    return sum



def subtract_new(path,n,paths):

    first_img=cv2.imread(glob.glob(path + '/*.jpg')[0],0)
    avg =np.zeros(first_img.shape,np.float)     #float for accumulated function, uint8 for normal addition
    diff =np.zeros(first_img.shape,np.float)
    sum =np.zeros(first_img.shape,np.float)
    i =0

    for image_path in paths:
        print i       #For getting the status in terminal

        if i%2==0:
            img1 =  cv2.imread(image_path,0)
        else:
            img2 =  cv2.imread(image_path,0)

            diff=cv2.subtract(img1,img2)
            if i==1:
                sum=diff*0.00001
            # display(diff,'difference')

        # cv2.accumulateWeighted(diff,avg,0.01)
        # res = cv2.convertScaleAbs(avg)
        if i>1:
            sum=cv2.add(sum,diff*0.00001)

        display(sum,'res')
        i+=1
    cv2.imwrite('output2.jpg',sum)
    return sum






#Fucntion to display an image
def display(image,window_name):

  cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
  cv2.resizeWindow(window_name, 600,600)
  cv2.imshow(window_name, image)
  cv2.waitKey(10)                   # Wait for a keystroke in the window
  # cv2.destroyAllWindows()




def threshold(path):
    i=0
    for image_path in glob.glob(path + '/*.png'):
        print i, image_path
        img = cv2.imread(image_path,0)
        kernel = np.ones((5,5 ),np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        display(img,'erosion')
        clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(6,6))
        img = clahe.apply(img)
        display(img, 'clahe')
        # img = cv2.erode(img,kernel,iterations = 1)
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,0)
        kernel = np.ones((3,3),np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        # gaussian = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,51,0)
        display(img,'mean')
        cv2.destroyAllWindows()
        i+=1

    # return mean , gaussian



def threshold2(path):
    i=0
    for image_path in glob.glob(path + '/*.png'):
        print i, image_path
        img = cv2.imread(image_path,0)

        gaussian_image = scpy.gaussian_filter(img, (10,10))
        display(gaussian_image,'gaussian_image')

        threshold_image = threshold_adaptive(gaussian_image, 255, offset = 10)
        threshold_average_image = threshold_image.astype(np.uint8) * 255
        display(threshold_average_image,'threshold_average_image')


        edge_detection_image = cv2.Canny(threshold_average_image, 200, 200)
        display(edge_detection_image,'edge_detection_image')

        (_,cnts,_) = cv2.findContours(edge_detection_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        cv2.drawContours(img,cnts,-1, (0,255,0) ,6)
        display(img,'final')
        # ret,th1 = cv2.threshold(img,180,255,cv2.THRESH_BINARY)
        # display(edge_detection_image,'edge_detection_image')
        # median = cv2.medianBlur(gaussian,9)
        # edged = cv2.Canny(median, 30, 200)

        # image, contours, hier = cv2.findContours(median, cv2.RETR_TREE,
        #                 cv2.CHAIN_APPROX_SIMPLE)

        # print 'Contours=', len(contours)

        # # display(gaussian,'gaussian')
        # # display(median,'blur')
        # # display(edged,'edged')
        # # display(image,'image')



        # for cnt in contours:
        #     print  'here'
        #     epsilon = 0.1*cv2.arcLength(cnt,True)
        #     approx = cv2.approxPolyDP(cnt,epsilon,True)
        #     print  'here2'
        #     M = cv2.moments(approx)
        #     # print( M )
        #     area = cv2.contourArea(approx)
        #     if area>500 :#and area <22000:
        #         print 'area= ',area
        #         mask = np.zeros(image.shape, dtype = "uint8")
        #         cv2.drawContours(img, approx, -1, (255, 0, 0), -1)
        #         display(img,'mask')
        # display(mean, 'mean')
        # display(gaussian,'gaussian')
        cv2.destroyAllWindows()
        i+=1



def main():
    # arguments = sys.argv[1:]

    #Checking if path is entered
    if len(sys.argv) < 2:
        path = '/home/kashish/Downloads/sample_drive/cam_5'
        print 'No path given, using defaut path'
        # sys.exit(0)
    else:
        path =sys.argv[1]

    #Number of images in the folder
    n_of_images=glob.glob(path + '/*.jpg')

    # threshold2(path)
    paths = path_array(path)
    sum = subtract_new(path, n_of_images,paths)
    cv2.imwrite('new_cam5.png',sum)
    cv2.imshow('sum', sum)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    sys.exit(0)


    #New approach
    sum = subtract(path,n_of_images)
    cv2.imshow('sum', sum)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    sys.exit(1)
    #New approach

    #Finding the average image and
    avg_image=average_images(path,n_of_images)
    display(avg_image,'Average image')#Display the average image

    #Applying Gaussian Blur
    avg_blurred = cv2.GaussianBlur(avg_image, (7,7),0)
    display(avg_blurred,'Blurred Image')

    clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(6,6))
    cl1 = clahe.apply(avg_blurred)
    display(cl1,'After CLAHE'
)
    ret,th1 = cv2.threshold(cl1, 50,255,cv2.THRESH_BINARY)
    display(th1,'Threshold img')


    image, contours, hier = cv2.findContours(th1, cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(image, contours, -1, (255,0,0), 10)
    display(image,'Contours')

    print 'Number of contours= ',len(contours)

    # with each contour, draw boundingRect in green
    # a minAreaRect in red and
    # a minEnclosingCircle in blue
    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        # draw a green rectangle to visualize the bounding rect
        if x!=0 and y!=0:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # get the min area rect
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            # convert all coordinates floating point values to int
            box = np.int0(box)
            # draw a red 'nghien' rectangle
            cv2.drawContours(img, [box], 0, (0, 0, 255))


    #     else:
    #         contours.remove(c)

if __name__=="__main__":
    main()
