from imutils.video import WebcamVideoStream
import numpy as np
import cv2
from math import fabs
from datetime import datetime
from time import time, sleep
import cv2
import psutil
import os

p = psutil.Process(os.getpid())
p.nice(0)

vs = WebcamVideoStream(src=0).start()

now = datetime.now()

pic_id = 0
for i in range(20): image = vs.read()
old_frame = None
diff = 0

try:

    print("Is the SD OK?")
    
    sd_name = os.listdir('/media/felipe/')[0]
    
    print("Yes, the name is {}".format(sd_name))
    
    print("Are there raw and cropped folders? {}".format(os.path.isdir(os.path.join('/media/felipe/',sd_name,'raw'))))
    
    if not os.path.isdir(os.path.join('/media/felipe/',sd_name,'raw')):
    
        print("Creating raw and cropped on {}".format(os.path.join('/media/felipe/',sd_name)))
        
        print("OK" if not os.mkdir(os.path.join('/media/felipe/',sd_name,'raw')) else "ERROR MAKING FOLDER")
        print("OK" if not os.mkdir(os.path.join('/media/felipe/',sd_name,'cropped')) else "ERROR MAKING FOLDER")
        
except Exception as e:

    print(e)
    sd_name = "error"
 
print("ALL SET")

while True:

    if  datetime.now().hour >= 18:  break

    t1 = time()

    image = vs.read()

    if old_frame is not None:

        frame = image[:,:,2]
        diff = np.mean(cv2.subtract(cv2.resize(old_frame, (100,100)), cv2.resize(image, (100,100))))

        if diff > 4:

            res = cv2.imwrite(os.path.join('/media/felipe',sd_name,'raw',str(now.day)+str(now.hour)+str(pic_id).zfill(10)+'.png'), image)
            p = os.path.join('/media/felipe',sd_name,'raw',str(now.day)+str(now.hour)+str(pic_id).zfill(10)+'.png')
            
            if not res:
                cv2.imwrite('/home/felipe/Desktop/web/raw/'+str(now.day)+str(now.hour)+str(pic_id).zfill(10)+'.png', image)
                p = '/home/felipe/Desktop/web/raw/'+str(now.day)+str(now.hour)+str(pic_id).zfill(10)+'.png'

            pic_id+=1

            print(p)

    old_frame = image

    while time() - t1 < 1/120: pass

    #cv2.imshow('x', image)
    #cv2.waitKey(1)

    #print(diff)

"""

    cv2.imshow('x',temp)
    key = cv2.waitKey(1)

    if key == ord('q') and br > 0.01:
        br -= 0.01
        vs.set(10, br) #
        print('br', br)
    elif key == ord('e') and br < 0.8:
        br += 0.01
        vs.set(10, br) #
        print('br', br)
    elif key == ord('a') and cont > 0.01:
        cont -= 0.01
        vs.set(11, cont) #
        print('cont', cont)
    elif key == ord('d') and cont < 0.8:
        cont += 0.01
        vs.set(11, cont) #
        print('cont', cont)
    elif key == ord('z') and sat > 0.01:
        sat -= 0.01
        vs.set(12, sat) #
        print('sat', sat)
    elif key == ord('c') and sat < 0.8:
        sat += 0.01
        vs.set(12, sat) #
        print('sat', sat)

    print(diff, time()-t1, temp.shape)

"""

#cv2.destroyAllWindows()
vs.stop()




