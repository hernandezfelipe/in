import os
from time import sleep
import psutil

p = psutil.Process(os.getpid())
p.nice(18)

path_sd_raw = '/media/felipe/8C0B-E857/raw/'
path_sd_cropped = '/media/felipe/8C0B-E857/cropped/'

path_hd_raw = '/home/felipe/Desktop/web/raw/'
path_hd_cropped = '/home/felipe/Desktop/web/cropped/'


def send(lista, path):
    lista = lista[:20]
    lista = [path+x for x in lista]
    lista = ' '.join(lista)
    print(lista)
    res = os.system('sshpass -p fe123 scp '+lista+' pi@192.168.15.55:/home/pi/Desktop/web/raw/')
    if res != 0:
        print('error sending file')
        sleep(5)

    else:
        os.system('rm '+lista)
        #sleep(20)

while True:
    try:
        lista_sd_raw = os.listdir(path_sd_raw)
        lista_hd_cropped = os.listdir(path_hd_cropped)
        if len(lista_hd_cropped) > 0:
            print("Cleaning cropped from HD")
            os.system("mv "+path_hd_cropped+"* "+path_sd_cropped)

    except:
        lista_sd_raw = []

    lista_hd_raw = os.listdir(path_hd_raw)
    if len(lista_sd_raw) == 0 and len(lista_hd_raw) == 0:
        print("Empty dir - SCP")
        sleep(10)

    elif len(lista_hd_raw) != 0:
        print("HD", path_hd_raw)
        print("Sending from HD_RAW to HD2_RAW")
        send(lista_hd_raw, path_hd_raw)

    else:
        print("SD", path_sd_raw)
        print("Sending from SD_RAW to HD2_RAW")
        send(lista_sd_raw, path_sd_raw)

