import time, logging, picamera, os, json
#from gpiozero import DistanceSensor
from sensor import proximidad
from Rutas import path
from Gest_Files import read_DataFile as Readfiles
import pygame as pygame 
import threading, redis, random
#sensor = DistanceSensor(trigger=18, echo=24) #BCM gpio18 == FISICO(pin12), BCM gpio24 == FISICO(pin18)
#LOGGING CONFIGURATION
logging.basicConfig(level = logging.DEBUG, format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,filename=path()['p_data']+'camera_auto.log',filemode='a')
r = redis.Redis(host='127.0.0.1', port=6379, db=1)
def CameraAuto(lolo, lo, hi):
    #if r.get('Camera_Activa') == 'True':
        #Camara_Disponible=False
    #else:
    if r.get('Camera_Activa') == b'False':
        print('PASO')
        Camara_Disponible=True
        camera=picamera.PiCamera(resolution=(1024, 768), framerate=24)
        pygame.init()
        while True:
            if (r.get('SALIR')) == b'True' or (r.get('SALIR_CAMARA_AUTO'))== b'True':
                if camera.previewing:  
                    camera.stop_preview()
                    camera.close()
                    logging.warning('camera_auto-W10: DESACTIVANDO CAMARA' )
                r.set('Camera_Activa', 'False')
                logging.warning('camera_auto-W11: SALIENDO DE CAMARA AUTO' )
                time.sleep(1)
                exit()
            distancenormalizada=100
            iteraint=0
            iteracion=0
            cerrar=10
            CamaraOffTime =10
            CerrarIteraciones=15
            UltimaIteracion=20
            try:
                distanceCmx =  proximidad()[0]
                sensor_when_out_of_range=proximidad()[1]
            except ValueError as er:
                logging.warning('camera_auto-W01: '+ er )
            #if (distanceCmx < 100 and Camara_Disponible):
            if (distanceCmx < 100):
                while iteraint < cerrar:
                    iteracion+=1
                    if not camera.previewing:
                        camera.start_preview()
                        r.set('Camera_Activa', 'True')
                        camera.annotate_background = picamera.Color('black')
                    if (distanceCmx < distancenormalizada):
                        if (iteracion < CerrarIteraciones):
                            iteraint=0
                            CamaraOffTime=10
                        if distanceCmx >= hi:
                            logging.warning('camera_auto-W02: ' + str(distanceCmx))
                        if (distanceCmx < hi ) and (distanceCmx >= lo ):
                            logging.warning('camera_auto-W03, sensor: ' + str(distanceCmx))
                            pygame.mixer.music.load(path()['p_media']+"p1.wav")
                            pygame.mixer.music.play(2)
                            logging.warning('camera_auto-W04: ' + 'Alarma de Proximidad nivel Advertencia(Menos de 70 cm)' )
                        if (distanceCmx < lo ) and (distanceCmx >= lolo):
                            logging.warning('camera_auto-W05:  sensor: ' + str(distanceCmx))
                            pygame.mixer.music.load(path()['p_media']+"p1.wav")
                            pygame.mixer.music.play(2)
                            logging.warning('camera_auto-W06: Alarma de Proximidad nivel Advertencia(Menos de 65 cm)' )
                        if (distanceCmx < lolo ):
                            logging.warning('camera_auto-W07:  ' + str(distanceCmx))
                            pygame.mixer.music.load(path()['p_media']+"p2.wav")
                            pygame.mixer.music.play(2)
                            logging.warning('camera_auto-W08: '+ 'Alarma de Proximidad nivel Advertencia(Menos de 25 cm)' )
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
                                camera.annotate_text = 'CERRANDO CAMARA EN '+ str(CamaraOffTime)+' Seg'
                            if CamaraOffTime<=0:
                                #if iteraint >= cerrar or iteracion >= UltimaIteracion:
                                distanceCmx= distancenormalizada
                                iteraint=cerrar + 1 # Para cerrar el ciclo en la proxima iteracion
                                logging.warning('camera_auto-W09: DESACTIVANDO CAMARA' )
                                camera.annotate_text = 'CERRANDO CAMARA EN '+ str('CamaraOffTime')+' Seg'
                                if   camera.previewing:  
                                    camera.stop_preview()
                                    r.set('Camera_Activa', 'False')
                                time.sleep(3)
                                        #camera.close()
                            time.sleep(1)
            time.sleep(1)
    logging.warning('camera_auto-W12: SALIENDO DE CAMARA AUTO, RECURSO NO DISPONIBLE' )
CameraAuto(lolo=25, lo=65, hi=70)
 
    