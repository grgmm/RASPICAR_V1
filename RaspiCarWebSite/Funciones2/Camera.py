import time, logging, picamera, os, json
#from gpiozero import DistanceSensor
from sensor import proximidad
from Rutas import path
from Gest_Files import read_DataFile as Readfiles
import pygame as pygame 
import threading, redis, random
r = redis.Redis(host='127.0.0.1', port=6379, db=1)
logging.basicConfig(level = logging.DEBUG, format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,filename=path()['p_data']+'camera_manual.log',filemode='a')
def camera(lolo, lo, hi):
    pygame.init()
    distancenormalizada=100
    iteraint=0
    iteracion=0
    cerrar=10
    CamaraOffTime =10
    CerrarIteraciones=15
    UltimaIteracion=20
    Camara_Disponible=True
    if r.get('Camera_Activa') == b'False':
        Camara_Disponible=True
    else:
        Camara_Disponible=False
    if (Camara_Disponible):
                camera=picamera.PiCamera(resolution=(1024, 768), framerate=24)
                r.set('Camera_Activa', 'True')
                while iteraint < cerrar:
                    iteracion+=1
                    #print('iteracion: '+str(iteracion))
                    if not camera.previewing:
                        camera.start_preview()
                        camera.annotate_background = picamera.Color('black')
                    try:
                        distanceCmx =  proximidad()[0]
                        logging.info('camera-I01: ' + str(distanceCmx))
                    except Exception as er:
                        logging.warning('camera-W01: '+ er)
                    sensor_when_out_of_range=proximidad()[1]
                    if (distanceCmx < distancenormalizada):
                        if (iteracion < CerrarIteraciones):
                            iteraint=0
                            CamaraOffTime=10
                        #if distanceCmx >= hi:
                            #logging.info('camera-I01, sensor: ' + str(distanceCmx))
                        if (distanceCmx < hi ) and (distanceCmx >= lo ):
                            pygame.mixer.music.load(path()['p_media']+"p1.wav")
                            pygame.mixer.music.play(2)
                            logging.warning('camera-W01 '+ 'Alarma de Proximidad nivel Advertencia(Menos de 70 cm)' )
                        if (distanceCmx < lo ) and (distanceCmx >= lolo):
                            pygame.mixer.music.load(path()['p_media']+"p1.wav")
                            pygame.mixer.music.play(2)
                            logging.warning('W0-02: '+ 'Alarma de Proximidad nivel Advertencia(Menos de 65 cm)' )
                        if (distanceCmx < lolo ):
                            pygame.mixer.music.load(path()['p_media']+"p2.wav")
                            pygame.mixer.music.play(2)
                            logging.warning('camera-W03: '+ 'Alarma de Proximidad nivel Advertencia(Menos de 25 cm)' )
                        if not camera.previewing:
                            camera.start_preview()
                            camera.annotate_background = picamera.Color('black')      
                            camera.annotate_text = str(distanceCmx) +' Cm'
                        else:
                            camera.annotate_text = str(distanceCmx) +' Cm'
                    if distanceCmx >= distancenormalizada or  sensor_when_out_of_range or iteracion >= CerrarIteraciones:
                        iteraint+=1
                        CamaraOffTime-=1
                        if not camera.previewing:
                            camera.start_preview()
                            camera.annotate_background = picamera.Color('black')      
                        camera.annotate_text = 'CERRANDO CAMARA MANUAL EN '+ str(CamaraOffTime)+' Seg'
                        if CamaraOffTime<=0:
                            distanceCmx= distancenormalizada
                            iteraint=cerrar + 1 # Para cerrar el ciclo en la proxima iteracion
                            logging.info('camera-I02,  DESACTIVANDO CAMARA MANUAL' )
                            camera.annotate_text = 'CERRANDO CAMARA EN '+ str('CamaraOffTime')+' Seg'
                            camera
                            if   camera.previewing:  
                                camera.stop_preview()
                                camera.close()
                                Camara_Disponible=False
                                r.set('Camera_Activa', 'False')
                    time.sleep(1)
    else:
        logging.warning('camera-I03: SALIENDO DE CAMARA MANUAL, RECURSO NO DISPONIBLE' )
camera(lolo=25, lo=65, hi=70)    