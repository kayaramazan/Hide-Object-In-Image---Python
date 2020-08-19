
import numpy as np
import cv2 
import matplotlib.pyplot as plt
from random import *

def centroid_histogram(clt): 
    
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
 
    hist = hist.astype("float")
    hist /= hist.sum()

    # Olusturulan histogrami donduruyor
    return hist


def plot_colors(hist, centroids):
    # olusucak patternin boyutlari
    newPatternWidth = 1500
    newPatternHeight = 1500

    #baskin renkleri olusturmak icin bos canvas olustuluyor
    #patterni olusturmank icin canvas olusturuluyor
    bar = np.zeros((300, 300, 3), dtype="uint8") 
    img2 = np.zeros((newPatternWidth, newPatternHeight, 3), dtype="uint8")
    startX = 0

    ColorBalanceArray = []

    # baskin renkleri olusturan donguyu aciyor 
    for (percent, color) in zip(hist, centroids):
        
        # baskin renkleri olusturan sekli ciziyor
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 300),
                      color.astype("uint8").tolist(), -1)
 
        # baskin renklerin orantisina gore diziye renkleri dolduruyor
        for i in range(int(endX)-int(startX)):
            if(color.astype(np.uint8)[0]<250 or color.astype(np.uint8)[0]<250 or color.astype(np.uint8)[0]<250):
                ColorBalanceArray.append(color.astype("uint8").tolist() ) 

        startX = endX 

        #  Patternin her bir karesine baskin renklerden birini restgele seciyor
    for a in range(newPatternHeight):
        for i in range(newPatternWidth):
            cv2.rectangle(img2,(int(i),a),(int(i+1),a+1),choice(ColorBalanceArray),-1)
        
    plt.figure("Pattern")
    plt.axis("off")
    plt.imshow(img2) 
    
    # pattern save
    plt.savefig('images/pattern.png')
    # return the bar chart

    return bar
