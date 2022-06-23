import numpy as np
import cv2
from glob import glob

confidenceThreshold = 0.5
NMSThreshold = 0.3

modelConfiguration = 'obj.cfg'
modelWeights = 'obj_60000.weights'

labelsPath = 'obj3.names'
labels = open(labelsPath).read().strip().split('\n')

np.random.seed(10)
COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
for fn in glob('test_out/*.jpg'):
    c=0
    from PIL import Image, ImageEnhance 
    im = Image.open(fn)
    enhancer = ImageEnhance.Sharpness(im)
    enhanced_im = enhancer.enhance(10.0)
    fn=fn.replace('test_out','test_out1')
    enhanced_im.save(fn)
    
count=0   
for fn in glob('test_out1/*.jpg'):
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

    if(len(detectionNMS) > 0):
        for i in detectionNMS.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[classIDs[i]]]
            if(labels[classIDs[i]]=="LP"):
                cv2.imwrite("LP//frame%d.jpg" % count, image[y-10:y+h+5, x:x+w])
                count+=1
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                cv2.imshow('Image', image[y-10:y+h+5, x:x+w])
                cv2.waitKey(500)


