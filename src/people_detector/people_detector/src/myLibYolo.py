import cv2
import numpy as np
import os

def increaseRoi(yoloCoordinates,percentage):
    # increase every dimension of percentage of it
    # W=100 became 110 with a  percentage of 10% 
    yoloCoordinates[0]=round(yoloCoordinates[0]-(yoloCoordinates[2]*percentage)/2)
    yoloCoordinates[1]=round(yoloCoordinates[1]-(yoloCoordinates[3]*percentage)/2)
    yoloCoordinates[2]=round(yoloCoordinates[2]+(yoloCoordinates[2]*percentage))
    yoloCoordinates[3]=round(yoloCoordinates[3]+(yoloCoordinates[3]*percentage))

def createImageHole(image,x,y,x_plus_w,y_plus_h):
    color = (255,255,255) #self.COLORS[class_id]
    cv2.rectangle(image, (x,y), (x_plus_w,y_plus_h), color, thickness=-1)

def createMask(mask,x,y,x_plus_w,y_plus_h):
    thickness = -1
    color = (255,255,255)
    mask = cv2.rectangle(mask, (x,y),(x_plus_w,y_plus_h), color, thickness) 

def splitImage(imHeight,imWidth,heightYolo,widthYolo,overlap):   
    # height, width, number of channels in image
    imgheight = imHeight
    imgwidth = imWidth   
    #newImage = Image.new('RGB', (imgwidth, imgheight))
    #start = time.time()
    listCoordinates=[]
    for i in range(0,imgheight,heightYolo-overlap):
            for j in range(0,imgwidth,widthYolo-overlap): 
                '''    
                #single cropped image    
                if(j==0 and i==0):
                    crop_img = im[i:i+heightYolo,j:j+widthYolo] 
                    #print(i,i+heightYolo,j,j+widthYolo)
                elif(i==0 and j!=0):
                   crop_img = im[i:i+heightYolo,j:j+widthYolo] 
                   #print(i,i+heightYolo,j,j+widthYolo)
                elif(i!=0 and j==0):
                    crop_img = im[i:i+heightYolo,j:j+widthYolo] 
                    #print(i,i+heightYolo,j,j+widthYolo)
                else:
                  crop_img = im[i:i+heightYolo,j:j+widthYolo]
                  #print(i,i+heightYolo,j,j+widthYolo) 
                '''
                listCoordinates.append((i,j))
                              
    #stop = time.time()    
    #print("Total time=",stop-start,"s")       
    return listCoordinates

class detectorYolo:
    
    def __init__(self,model_path_folder):
        pathData= model_path_folder #os.path.join("models","yolo")
        self.config_path =  os.path.join(pathData,"yolov3-416.cfg")
        self.weights_path = os.path.join(pathData, "yolov3-416.weights")
        #threshold when applying non-maxima suppression
        #self.nms = nms_th # set threshold for non maximum supression
        # loading all the class labels (objects)
        pathNames=os.path.join(pathData,"coco.names")
        self.classes = open(pathNames).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        COLORS = np.random.randint(0, 255, size=(len(self.classes), 3),dtype="uint8")
        # load the YOLO network
        #net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)
        print(self.config_path, self.weights_path)
        self.net = cv2.dnn_DetectionModel(self.config_path, self.weights_path)
        #self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENcv2.)

    def doDetection(self, image,coordinates=[0,0],confidence_th=0.5,nms_th=0.3):
        #minimum probability to filter weak detections"
        self.c_threshold = confidence_th # set threshold for bounding box values
        #threshold when applying non-maxima suppression
        self.nms = nms_th # set threshold for non maximum supression
        #define the list of yolo coordinates
        yoloCoordinates=[]
        scoresCoordinates=[]
        #copy images
        image=image.copy()
        (H,W) = image.shape[:2]
        # Get the names of output layers
        ln = self.net.getLayerNames()
        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        # generate blob for image input to the network
        blob = cv2.dnn.blobFromImage(image,1/255,(416,416),swapRB=True, crop=False)
        self.net.setInput(blob)
        #start = time.time()
        layersOutputs = self.net.forward(ln)        
        boxes = []
        confidences = []
        classIDs = []
        for output in layersOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]            
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.c_threshold :              
                    box = detection[0:4]* np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)              
        # Remove unnecessary boxes using non maximum suppression
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.c_threshold, self.nms)
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                #filtro solo alla classe persona
                if(self.classes[classIDs[i]]=="person"):
                    # extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])            
                    # draw a bounding box rectangle and label on the image
                    #color = [int(c) for c in COLORS[classIDs[i]]]
                    color=(0,255,255)
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)
                    #text = "{}: {:.4f}".format(self.classes[classIDs[i]], confidences[i])
                    #cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
                    
                    #absolute coordinates
                    #Controllo dimensioni roi per evitare falsi positivi. Elimina rettangoli con h molto maggiore di w. E
                    #elimino rettangoli con score basso e Roi grande rispetto all'immagine elaborata
                    #if(w/h>0.3 and not (confidences[i]<0.5 and ((w/W>0.6) or (h/H>0.6)))):
                
                    yoloCoordinates.append([coordinates[0]+y,coordinates[1]+x,h,w])  
                    scoresCoordinates.append(confidences[i])  
                    #cv2.2.imshow("im", image)
                    #cv2.2.waitKey()
                    #print(h,w,H,W)
        
        #end = time.time()
        # print the time required
        #print("Time single image",end- start,"s")
        return yoloCoordinates,scoresCoordinates
