import os
from model import segmentation
import cv2
from random import randint
from time import sleep
import psutil

p = psutil.Process(os.getpid())
p.nice(1)

source_sd = '/media/felipe/8C0B-E857/raw/'
plates_sd = '/media/felipe/8C0B-E857/cropped/'
plates_backup = '/home/felipe/Desktop/web/cropped/'
source_backup =  '/home/felipe/Desktop/web/raw/'
#scanned = './SCANNED/'

while True:

    try:
        lista = os.listdir(source_sd)
        source = source_sd
        plates = plates_sd

    except:

        lista = os.listdir(source_backup)
        source = source_backup
        plates = plates_backup

    lista.reverse()

    if len(lista) == 0:

        print("Empty dir - placa_split")
        sleep(10)

    else:

        for i in lista:

            try:

                img = cv2.imread(source+i)
                res = segmentation(img)
                print(i, res[1], res[-1])

                if res[1] >= 1:
                    ret = cv2.imwrite(plates+i, res[2])

                    if not ret:
                        ret = cv2.imwrite(plates_backup+i, res[2])

            except Exception as e:

                print(e)

            try:

                #os.rename(source+i, scanned+i)
                os.remove(source+i)

            except Exception as e:

                print(e)

