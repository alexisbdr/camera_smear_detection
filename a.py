#!/usr/bin/env python
import numpy as np
import cv2
import glob

images=[]


def read_images(path,n):

  i=0 #testing
  for image_path in glob.glob(path + '/*.jpg'):
    images.append(cv2.imread(image_path,0))
    # print(image_path)
    #testing... limitting the number of input images
    i+=1
    if(i>n):
        break
    #testing


def average_images(path,n):

  first_img=cv2.imread(glob.glob(path + '/*.jpg')[0],0)

  avg =np.zeros(first_img.shape,np.float)     #float for accumulated function, uint8 for normal addition
  i =0

  for image_path in glob.glob(path + '/*.jpg'):
  # for image in images:
    if i<n:
      # avg = cv2.add(cv2.imread(image_path,1)/n , avg)
      # img = 255 - cv2.imread(image_path,0)
      img = cv2.imread(image_path,0)
      normalizer , inverse_normalizer = PCA_sphereing(img)
      print(i)
      img = normalizer(img)
      blur = cv2.blur(img, (5,5),0)
      cv2.accumulateWeighted(img,avg,0.01)
      res1 = cv2.convertScaleAbs(avg)
    else:
      break
    i+=1
  return res1


def display(obj):

  cv2.namedWindow('image',cv2.WINDOW_NORMAL)
  cv2.resizeWindow('image', 600,600)
  # cv2.imshow("image", cv2.subtract(images[49],images[48]))
  cv2.imshow('image', obj)
  cv2.waitKey(0)                   # Wait for a keystroke in the window
  # cv2.destroyAllWindows()



# compute eigendecomposition of data covariance matrix for PCA transformation
def PCA(x,**kwargs):
    # regularization parameter for numerical stability
    lam = 10**(-7)
    if 'lam' in kwargs:
        lam = kwargs['lam']

    # create the correlation matrix
    P = float(x.shape[1])
    Cov = 1/P*np.dot(x,x.T) + lam*np.eye(x.shape[0])

    # use numpy function to compute eigenvalues / vectors of correlation matrix
    d,V = np.linalg.eigh(Cov)
    return d,V

# PCA-sphereing - use PCA to normalize input features
def PCA_sphereing(x,**kwargs):
    # Step 1: mean-center the data
    x_means = np.mean(x,axis = 1)[:,np.newaxis]
    x_centered = x - x_means

    # Step 2: compute pca transform on mean-centered data
    d,V = PCA(x_centered,**kwargs)

    # Step 3: divide off standard deviation of each (transformed) input, 
    # which are equal to the returned eigenvalues in 'd'.  
    stds = (d[:,np.newaxis])**(0.5)
    normalizer = lambda data: np.dot(V.T,data - x_means)/stds

    # create inverse normalizer
    inverse_normalizer = lambda data: np.dot(V,data*stds) + x_means

    # return normalizer 
    return normalizer,inverse_normalizer


def main():

  # path = '/home/suhailps/Documents/Assignments/Spring_18/Geospatial/Assignment1/sample_drive/cam_0'
  # Please add the images files
  path = r'C:\Users\Alexis\Downloads\sample_drive\cam_3'
  num_images = len(glob.glob(path + "/*.jpg"))*1.0
  desired_number_images = 500.0
  read_images(path,desired_number_images)
  
  # avg = np.zeros(images[0].shape,np.float)     #float for accumulated function, uint8 for normal addition

  # cv2.accumulate(images[1]/100, avg)
  avg1 = average_images(path,desired_number_images)
  # res1 = cv2.convertScaleAbs(avg1)
  # laplacian = cv2.Laplacian(avg1,cv2.CV_64F)
  # avg2 = average_images(path,110)
  display(avg1)
  avg1 = cv2.GaussianBlur(avg1, (7,7),0)
  display(avg1)
  clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(6,6))
  cl1 = clahe.apply(avg1)
  display(cl1)
  # ret,th1 = cv2.threshold(avg1,100,255,cv2.THRESH_BINARY)
  # th1 = cv2.threshold(avg1, 130,255,cv2.THRESH_BINARY)

  # display(th1)
  # display(cv2.Canny(th1,100,200))

  # display(res1)
  # display(laplacian*100)
  # display(avg2)
  # display(cv2.subtract(avg2, avg1))
  # display(cv2.absdiff(images[2] , images[1]))
  # display(cv2.absdiff(images[3] , images[2]))


  # display(cv2.subtract(images[5],images[4]))
  # display(cv2.subtract(images[7],images[6]))



if __name__ == "__main__":
  main()