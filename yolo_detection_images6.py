import os
from PIL import Image
count=0
list = os.listdir('tripleride') # dir is your directory path
number_files = len(list)
print(number_files)
img_dir = r"tripleride"
c=0
while(c!=number_files):
    c+=1
    for filename in os.listdir(img_dir):
        filepath = os.path.join(img_dir, filename)
        try:
            with Image.open(filepath) as im:
                x, y = im.size
        except:
            os.remove(filepath)

import numpy as np
import cv2
from glob import glob

confidenceThreshold = 0.0
NMSThreshold = 0.6

modelConfiguration = 'cfg/yolov3.cfg'
modelWeights = 'yolov3.weights'

labelsPath = 'coco.names'
labels = open(labelsPath).read().strip().split('\n')

np.random.seed(10)
COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
count=0
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
for fn in glob('tripleride/*.jpg'):
    image = cv2.imread(fn)
    (H, W) = image.shape[:2]

    #Determine output layer names
    layerName = net.getLayerNames()
    layerName = [layerName[i - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB = True, crop = False)
    net.setInput(blob)
    layersOutputs = net.forward(layerName)

    boxes = []
    confidences = []
    classIDs = []

    for output in layersOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidenceThreshold:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY,  width, height) = box.astype('int')
                x = int(centerX - (width/2))
                y = int(centerY - (height/2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    #Apply Non Maxima Suppression
    detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)
    k=[]
    if(len(detectionNMS) > 0):
        for i in detectionNMS.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[classIDs[i]]]
            #cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            print(labels[classIDs[i]])
            k.append(labels[classIDs[i]])
            #text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
            #cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('Image', image)
    print(k)
    if(k.count('person')==3):
        count+=1
        cv2.imwrite("test_out//framet%d.jpg" % count,image)
    cv2.waitKey(500)
