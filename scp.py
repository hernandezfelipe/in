import os
from time import sleep
import psutil
from url import internet_on

p = psutil.Process(os.getpid())
p.nice(18)

path_hd_raw = '/home/felipe/Desktop/web/raw/'
path_hd_cropped = '/home/felipe/Desktop/web/cropped/'

try:

    print("Is the SD OK?")

    sd_name = os.listdir('/media/felipe/')[0]

    print("Yes, the name is {}".format(sd_name))

    print("Are there raw and cropped folders? {}".format(os.path.isdir(os.path.join('/media/felipe/',sd_name,'raw'))))

    if not os.path.isdir(os.path.join('/media/felipe/',sd_name,'raw')):

        print("Creating raw and cropped on {}".format(os.path.join('/media/felipe/',sd_name)))

        print("OK" if not os.mkdir(os.path.join('/media/felipe/',sd_name,'raw')) else "ERROR MAKING FOLDER")
        print("OK" if not os.mkdir(os.path.join('/media/felipe/',sd_name,'cropped')) else "ERROR MAKING FOLDER")

    path_sd_raw = os.path.join('/media/felipe/',sd_name,'raw')
    path_sd_cropped = os.path.join('/media/felipe/',sd_name,'cropped')

except Exception as e:

    print(e)
    sd_name = "error"

print("ALL SET")

def send(lista, path):
    lista = lista[:20]
    lista = [path+"/"+x for x in lista]
    lista = ' '.join(lista)
    print(lista)
    res = os.system('sshpass -p fe123 scp '+lista+' pi@192.168.15.55:/home/pi/Desktop/web/raw/')
    if res != 0:
        print('error sending file')
        sleep(5)

    else:
        os.system('rm '+lista)
        sleep(20)

n = 0
nmax = 300

while True:


    lista_hd_raw = os.listdir(path_hd_raw)


    lista_sd_raw = os.listdir(path_sd_raw)


    lista_hd_cropped = os.listdir(path_hd_cropped)


    if len(lista_hd_cropped) != 0:
        os.system('mv '+path_hd_cropped+'* '+path_sd_cropped)
        print("Cleaning cropped images")

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

    sleep(1)
   
    n+=1
    
    if n == nmax:

        n = 0
        
        if not internet_on():

            os.system('sudo reboot now')

    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    

