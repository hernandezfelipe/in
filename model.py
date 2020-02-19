import os
import numpy as np
from keras.models import model_from_json
from keras.optimizers import Adam
import cv2
from time import time
import sys
import psutil
from collections import Counter
from scipy import stats
import matplotlib.pyplot as plt

def entropy_calc(img):
    ent = stats.entropy(list(Counter(img.flatten()).values()), base=2)
    return ent

p = psutil.Process(os.getpid())
p.nice(0)  

path = os.path.dirname(__file__)+'/'

HEIGHT = 32
WIDTH = 64
h = HEIGHT
w = WIDTH
slide_y = h // 4
slide_x = w // 4

def load_model():

    json_file = open(path+'1_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    opt = Adam(lr = 0.0001)
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path+'1_best_model.h5')
    loaded_model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

    return loaded_model

md_pred = load_model()

def predict(img):
    if type(img) == str:    img = cv2.imread(img,0)
    elif img.ndim > 2:  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img[0][0] > 1: img = img / 255.
    prediction = md_pred.predict(img.reshape(1, HEIGHT, WIDTH, -1))[0]
    return prediction


def segmentation(img, show=False):

    t1 = time()

    if type(img) == str:    img = cv2.imread(img,0)
    elif img.ndim > 2:  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img[0][0] > 1: img = img / 255.
    
    backup = img.copy()
    img = cv2.resize(img,(img.shape[1]//2, img.shape[0]//2))   
    
    r, gray = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    x1 = 1e9
    x2 = 0
    y1 = 1e9
    y2 = 0
    cutout = -1
    n = 0

    for j in np.linspace(0,img.shape[0]-h,(img.shape[0]-h)//slide_y+1).astype('uint16'):
        for i in np.linspace(0,img.shape[1]-w,(img.shape[1]-w)//slide_x+1).astype('uint16'):

            pred = -1
            temp = img.copy()
            splice_ = temp[j:j+h, i:i+w]

            t = gray[j:j+h, i:i+w]

            entropy = entropy_calc(t)

            if entropy > 0.8:

                pred = predict(splice_)
                pred = round(pred[0],2)

                if pred >= 0.8:

                    n+= 1

                    if i < y1:  y1 = i
                    if (i+w) > y2:  y2 = i+w
                    if j < x1:  x1 = j
                    if (j+h) > x2:  x2 = j+h

            if show:

                print(pred, entropy)
                cv2.imshow('x', t)
                cv2.waitKey(100)
                
    if n > 0:

        cutout = backup.copy()
        cutout = cutout[x1*2:x2*2,y1*2:y2*2]   
        cv2.rectangle(backup, (y1*2,x1*2),(y2*2,x2*2),(0,255,0), 5)     

    return backup, n, cutout, (x1+x2), (y1+y2), time() - t1


def segmentation2(img, show=False):

    if type(img) == str:    img = cv2.imread(img)

    img = cv2.resize(img,(img.shape[1]//2, img.shape[0]//2))

    out = []

    for j in np.linspace(0,img.shape[0]-h,(img.shape[0]-h)//slide_y+1).astype('uint16'):
        for i in np.linspace(0,img.shape[1]-w,(img.shape[1]-w)//slide_x+1).astype('uint16'):

            splice_ = img[j:j+h, i:i+w]

            out.append(splice_)

    return out



if __name__ == "__main__":

    if len(sys.argv) > 1:   img = cv2.imread(sys.argv[1])    
    else:   img = cv2.imread('./test12.png')
    
    if len(sys.argv) > 2:   
    
        s = not bool(sys.argv[2])
        
    else:   s = True    

    res = segmentation(img,show=s)
    print(res)
    plt.imshow(res[0])
    plt.show()
    plt.imshow(res[2])
    plt.show()
    cv2.destroyAllWindows()
