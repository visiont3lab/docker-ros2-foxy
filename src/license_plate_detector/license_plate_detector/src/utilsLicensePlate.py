import sys, os
import keras
import cv2
import traceback
from glob 						import glob
from os.path 					import splitext, basename
import numpy as np
import imutils

#from utils.keras_utils 			import load_model, detect_lp
#from utils.label 				import Shape, writeShapes
#from utils.utils 				import im2single,getWH

from license_plate_detector.src.utils 				import im2single,getWH
from license_plate_detector.src.keras_utils 		import load_model, detect_lp
from license_plate_detector.src.label 				import Shape, writeShapes

from datetime import datetime 

class LicensePlateDetector:
    
	def __init__(self,model_path="data/lp-detector/wpod-net_update1.h5"):
		self.wpod_net = load_model(model_path)
		#self.processing = False

	def getPoints(self,pts):
		rtl = np.int(pts[0][0]  )
		ctl = np.int(pts[1][0] )
		tl = (rtl,ctl)

		rtr = np.int(pts[0][1]  )
		ctr = np.int(pts[1][1] )
		tr = (rtr,ctr)

		rbr = np.int(pts[0][2] )
		cbr = np.int(pts[1][2] )
		br = (rbr,cbr)

		rbl = np.int(pts[0][3] )
		cbl = np.int(pts[1][3] )
		bl = (rbl,cbl)

		return tl,tr,br,bl

	def predict(self,im, lp_threshold = 0.5):
		#img = imutils.resize(im,width=320)
		# --- Network Prediction
		ratio = float(max(im.shape[:2]))/min(im.shape[:2])
		side  = int(ratio*288.)
		bound_dim = min(side + (side%(2**4)),608)
		#print("\t\tBound dim: %d, ratio: %f" % (bound_dim,ratio))
		# LpPtsPerc --> 4 License Plate Coordinate given as percentagle values
		# LpImgs --> Associated cropped License Plate images 
		LpPtsPerc,LpImgs,_ = detect_lp(self.wpod_net,im2single(im),bound_dim,2**4,(240,80),lp_threshold)
		# --- Get Results
		res=False
		imDraw=None
		Lpts=None
		if  len(LpImgs):
			res = True 
			Lpts = self.getPts(LpPtsPerc,im.shape)  # ListOf[tl,tr,br,bl]
			imDraw = self.getDrawImage(im,Lpts)
		return res,imDraw,Lpts,LpImgs

	def getPts(self,LpPtsPerc,imshape):
		pts = []
		for i in range(0,len(LpPtsPerc)):
			LpPts = LpPtsPerc[i].pts*getWH(imshape).reshape((2,1)) # C License Plate Coordinate coordinate given as pixel values
			tl,tr,br,bl = self.getPoints(LpPts) # top-left,bottom-left,top-right,bottom-right
			pts.append([list(tl),list(tr),list(br),list(bl)])
		return pts

	def getDrawImage(self,imDraw,LpPts,thickness=3):
		for i in range(0,len(LpPts)):
			tl,tr,br,bl = LpPts[i] # top-left,bottom-left,top-right,bottom-right
			#cv2.line(imDraw,tuple(tl),tuple(tr),(0,0,255),thickness)
			#cv2.line(imDraw,tuple(tr),tuple(br),(0,0,255),thickness)
			#cv2.line(imDraw,tuple(br),tuple(bl),(0,0,255),thickness)
			#cv2.line(imDraw,tuple(bl),tuple(tl),(0,0,255),thickness)

		# Create Mask
		mask = np.zeros(imDraw.shape,np.uint8)
		polyPoints = np.array(LpPts) #.reshape((-1, 1, 2)) 
		mask = cv2.fillPoly(mask, pts=polyPoints, color=(255,255,255))
		#mask = cv2.dilate(mask,kernel=np.ones((15,15), np.uint8) ,iterations = 1)		
		
		# BLurring
		imLpMask = cv2.bitwise_and(imDraw,mask)		
		kernel = np.ones((12,12),np.float32)/25
		imLpMask = cv2.filter2D(imLpMask,-1,kernel,borderType=cv2.BORDER_CONSTANT)
		#imLpMask = cv2.medianBlur(imLpMask, 31)
		#imLpMask = cv2.GaussianBlur(imLpMask, (31,31),0)
		
		imDrawMask = cv2.bitwise_and(imDraw,cv2.bitwise_not(mask))	
		#imDraw = imDrawMask + imLpMask
		imDraw = cv2.addWeighted(imDrawMask, 1, imLpMask, 1, 0)
		
		#imDraw = np.where(mask==np.array([0, 0, 0]),imDraw,imBlurred)
		return imDraw

	def processVideo(self,inp_path,out_path):
		cap = cv2.VideoCapture(os.path.join(inp_path))

		now = datetime.now()
		name = now.strftime("%m/%d/%Y %H:%M:%S")
		cv2.namedWindow(name, cv2.WINDOW_NORMAL)

		frame_width = int(cap.get(3))
		frame_height = int(cap.get(4))
		fourcc = cv2.VideoWriter_fourcc(*'mp4v')# cv2.VideoWriter_fourcc('M','J','P','G')
		outVideo = cv2.VideoWriter(out_path,fourcc, 10, (frame_width,frame_height))

		while(cap.isOpened()): # and self.processing==True):
			ret, frame = cap.read()
			if ret==True: 
				# Cool FIlter for emphasize detail (OCR)
				#mask = np.zeros(frame.shape, frame.dtype)
				#mask = cv2.bitwise_and(frame,mask)			
				#frame = cv2.bitwise_not(frame,mask)				

				res,frame,Lpts,LpImgs = self.predict(frame)

				if res:				
					cv2.imshow(name,frame)
					cv2.waitKey(1)
				else:
					pass
			
				outVideo.write(frame)			
			else:
				break

		#self.processing = False
		# Release everything if job is finished
		cap.release()
		cv2.destroyAllWindows()
	
def testFromFolder():
	try:	
		Lpd = LicensePlateDetector()

		input_dir  = "datasets/inputs" # sys.argv[1]
		output_dir = "datasets/outputs" #input_dir
		imgs_paths = glob('%s/*.jpg' % input_dir)

		print('Searching for license plates using WPOD-NET')

		for i,img_path in enumerate(imgs_paths):

			#print('\t Processing %s' % img_path)

			Ivehicle = cv2.imread(img_path)
			
			res,imDraw,Lpts,LpImgs = Lpd.predict(Ivehicle)
			if res:				
				cv2.imshow("Results",imDraw)
				cv2.waitKey(0)
			else:
				print('\t Not Found: %s' % img_path)

	except:
		traceback.print_exc()
		sys.exit(1)

	sys.exit(0)

def testRealTime():
	# Reduce video frame rate --> ffmpeg -i parking.mp4 -filter:v fps=fps=10 parking10.mp4
	Lpd = LicensePlateDetector()

	cap = cv2.VideoCapture(os.path.join("datasets","video","parking10.mp4"))

	cv2.namedWindow('Results', cv2.WINDOW_NORMAL)

	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
	fourcc = cv2.VideoWriter_fourcc(*'MP4V')# cv2.VideoWriter_fourcc('M','J','P','G')
	outVideo = cv2.VideoWriter('video.mp4',fourcc, 10, (frame_width,frame_height))

	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret==True:
			
			# Cool FIlter for emphasize detail (OCR)
			#mask = np.zeros(frame.shape, frame.dtype)
			#mask = cv2.bitwise_and(frame,mask)			
			#frame = cv2.bitwise_not(frame,mask)				

			res,frame,Lpts,LpImgs = Lpd.predict(frame)

			if res:				
				cv2.imshow("Results",frame)
				cv2.waitKey(1)
			else:
				pass

			outVideo.write(frame)			

	# Release everything if job is finished
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':

	testRealTime()

