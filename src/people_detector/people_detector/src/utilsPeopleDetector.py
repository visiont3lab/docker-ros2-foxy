import os
import numpy as np
import cv2 
import time
from datetime import datetime
from people_detector.src.myLibYolo import *
import imutils

def pyramid(image, scale=2, minSize=(100, 100)):
	# yield the original image
	yield image
	# keep looping over the pyramid
	while True:
		# compute the new dimensions of the image and resize it
		w = int(image.shape[1] / scale)
		image = imutils.resize(image, width=w)
		# if the resized image does not meet the supplied minimum
		# size, then stop constructing the pyramid
		if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
			break
		# yield the next image in the pyramid
		yield image

def splitImages(im):
    # 3*3 = 9  square
    num=2
    width =  int(im.shape[0]/num)
    height = int(im.shape[1]/num)

    imgwidth =  im.shape[0]
    imgheight = im.shape[1]
    
    imgs = []
    for j in range(0,imgheight,height):   # row
        for i in range(0,imgwidth,width): # col

            imCrop = im[i:i+width,j:j+height]
            imgs.append(imCrop)
            #cv2.rectangle(im,(j,i),(j+height,i+width), [0,255,255], 2)
            
            if ((j+height)<imgheight):
                overlapImCropH = im[i:i+width,j+int(0.5*height):j+int(1.5*height)]
                imgs.append(overlapImCropH)
                #cv2.imshow("overlapImCropH", overlapImCropH)
            if ((i+width)<imgwidth):
                overlapImCropW = im[i+int(0.5*width):i+int(1.5*width),j:j+height]
                imgs.append(overlapImCropW)
                #cv2.imshow("overlapImCropW", overlapImCropW)
                #cv2.rectangle(im,(j+int(0.5*width),i),(j+int(1.5*width),i+height), [0,255,0], 2)
            #cv2.imshow("ims", im)
            #cv2.imshow("imCrop", imCrop)    
            #cv2.waitKey(0)
    return imgs

class PeopleDetector:
    def __init__(self, model_path_folder):
        self.heightYolo = 416
        self.widthYolo = 416
        self.overlapImage = 50
        self.detect=detectorYolo(model_path_folder)   

    def processImageSplit(self,im):
        listImages=splitImage(im.shape[0],im.shape[1],self.heightYolo,self.widthYolo,self.overlapImage)
        img_hole= im.copy()
        img_Yolo=im.copy()
        mask = np.zeros((im.shape[0],im.shape[1],3), np.uint8)

        allDetectionCoordinates=[]
        allScoresCoordinates=[]
        for index,coordinates in enumerate(listImages):
            #cut in single image of dimension yolo 
            crop_img = im[coordinates[0]:coordinates[0]+self.heightYolo,coordinates[1]:coordinates[1]+self.widthYolo]     
            detectionCoordinates,scoresCoordinates=self.detect.doDetection(crop_img,coordinates)
            if(len(detectionCoordinates)):  
                allDetectionCoordinates.extend(detectionCoordinates)
                allScoresCoordinates.extend(scoresCoordinates)
            
        #check if have found some coordinates
        res = False
        if(len(allDetectionCoordinates)):
            res = True
            for detectedCoordinates,scores in zip(allDetectionCoordinates,allScoresCoordinates):
                #detectedCoordinatesFormat= row(0),column(1),h(2),w(3) 
                increaseRoi(detectedCoordinates,0.1)                 
                cv2.rectangle(img_Yolo, (detectedCoordinates[1], detectedCoordinates[0]), (detectedCoordinates[1] + detectedCoordinates[3], detectedCoordinates[0] + detectedCoordinates[2]), [0,255,0], 2)
                text = "{}: {:.4f}".format("Person",scores)
                cv2.putText(img_Yolo, text, (detectedCoordinates[1], detectedCoordinates[0] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,255,0], 2)
                createImageHole(img_hole,detectedCoordinates[1], detectedCoordinates[0], detectedCoordinates[1] + detectedCoordinates[3], detectedCoordinates[0] + detectedCoordinates[2])
                createMask(mask,detectedCoordinates[1], detectedCoordinates[0], detectedCoordinates[1] + detectedCoordinates[3], detectedCoordinates[0] + detectedCoordinates[2])

        #pathSaving=os.path.join(output_folder,os.path.splitext(os.path.basename(pathImage))[0])
        #cv2.imwrite(pathSaving+"_yolo.jpg",img_Yolo,[int(cv2.IMWRITE_JPEG_QUALITY), 80])
        return res, img_Yolo, allDetectionCoordinates

    def processImage(self,im):
        img_hole= im.copy()
        img_Yolo=im.copy()
        mask = np.zeros((im.shape[0],im.shape[1],3), np.uint8)

        allDetectionCoordinates=[]
        allScoresCoordinates=[]
        crop_img =  cv2.resize(im,(self.heightYolo,self.widthYolo))
        detectionCoordinates,scoresCoordinates=self.detect.doDetection(crop_img)
        if(len(detectionCoordinates)):  
            allDetectionCoordinates.extend(detectionCoordinates)
            allScoresCoordinates.extend(scoresCoordinates)
            
        #check if have found some coordinates
        res = False
        if(len(allDetectionCoordinates)):
            res = True
            for detectedCoordinates,scores in zip(allDetectionCoordinates,allScoresCoordinates):
                #detectedCoordinatesFormat= row(0),column(1),h(2),w(3) 
                increaseRoi(detectedCoordinates,0.1)                 
                cv2.rectangle(img_Yolo, (detectedCoordinates[1], detectedCoordinates[0]), (detectedCoordinates[1] + detectedCoordinates[3], detectedCoordinates[0] + detectedCoordinates[2]), [0,255,0], 2)
                text = "{}: {:.4f}".format("Person",scores)
                cv2.putText(img_Yolo, text, (detectedCoordinates[1], detectedCoordinates[0] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,255,0], 2)
                createImageHole(img_hole,detectedCoordinates[1], detectedCoordinates[0], detectedCoordinates[1] + detectedCoordinates[3], detectedCoordinates[0] + detectedCoordinates[2])
                createMask(mask,detectedCoordinates[1], detectedCoordinates[0], detectedCoordinates[1] + detectedCoordinates[3], detectedCoordinates[0] + detectedCoordinates[2])

        #pathSaving=os.path.join(output_folder,os.path.splitext(os.path.basename(pathImage))[0])
        #cv2.imwrite(pathSaving+"_yolo.jpg",img_Yolo,[int(cv2.IMWRITE_JPEG_QUALITY), 80])
        return res, img_Yolo, allDetectionCoordinates

                        