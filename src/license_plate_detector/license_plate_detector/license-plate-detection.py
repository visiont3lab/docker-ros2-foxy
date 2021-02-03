import sys, os
import keras
import cv2
import traceback

from utils.keras_utils 			import load_model
from glob 						import glob
from os.path 					import splitext, basename
from utils.utils 				import im2single,getWH
from utils.keras_utils 			import load_model, detect_lp
from utils.label 				import Shape, writeShapes

import numpy as np

def adjust_pts(pts,lroi):
	return pts*lroi.wh().reshape((2,1)) + lroi.tl().reshape((2,1))

def getPoints(pts):
	rtl = np.int(ppts[0][0]  )
	ctl = np.int(ppts[1][0] )
	tl = (rtl,ctl)

	rtr = np.int(ppts[0][1]  )
	ctr = np.int(ppts[1][1] )
	tr = (rtr,ctr)

	rbr = np.int(ppts[0][2] )
	cbr = np.int(ppts[1][2] )
	br = (rbr,cbr)

	rbl = np.int(ppts[0][3] )
	cbl = np.int(ppts[1][3] )
	bl = (rbl,cbl)

	return tl,bl,tr,br
	
if __name__ == '__main__':

	try:
		
		input_dir  = "datasets/inputs" # sys.argv[1]
		output_dir = "datasets/outputs" #input_dir

		lp_threshold = .5

		wpod_net_path ="data/lp-detector/wpod-net_update1.h5" #sys.argv[2]
		wpod_net = load_model(wpod_net_path)

		imgs_paths = glob('%s/*.jpg' % input_dir)

		print('Searching for license plates using WPOD-NET')

		for i,img_path in enumerate(imgs_paths):

			print('\t Processing %s' % img_path)

			bname = splitext(basename(img_path))[0]
			Ivehicle = cv2.imread(img_path)

			ratio = float(max(Ivehicle.shape[:2]))/min(Ivehicle.shape[:2])
			side  = int(ratio*288.)
			bound_dim = min(side + (side%(2**4)),608)
			print("\t\tBound dim: %d, ratio: %f" % (bound_dim,ratio))

			Llp,LlpImgs,_ = detect_lp(wpod_net,im2single(Ivehicle),bound_dim,2**4,(240,80),lp_threshold)

			if len(LlpImgs):
				Ilp = LlpImgs[0]
				Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
				Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)
				s = Shape(Llp[0].pts)

				pts = Llp[0].pts # percentage values
				ppts = pts*getWH(Ivehicle.shape).reshape((2,1)) # pixels values

				tl,bl,tr,br = getPoints(pts)

				cv2.line(Ivehicle,tl,tr,(255,0,0),1)
				cv2.line(Ivehicle,tr,br,(255,0,0),1)
				cv2.line(Ivehicle,br,bl,(255,0,0),1)
				cv2.line(Ivehicle,bl,tl,(255,0,0),1)
				
				#cv2.rectangle(Ivehicle,tl,br,(0,255,0),1)
				cv2.imshow("Detection",Ivehicle)
				cv2.imshow("LicensePlate",Ilp)
				cv2.waitKey(0)
				
				#cv2.imwrite('%s/%s_lp.png' % (output_dir,bname),Ilp*255.)
				#writeShapes('%s/%s_lp.txt' % (output_dir,bname),[s])

	except:
		traceback.print_exc()
		sys.exit(1)

	sys.exit(0)


