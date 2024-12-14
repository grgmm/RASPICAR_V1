from Funciones2.acq_RASPI import fRASPI
from Funciones2.gestionBD import fgestionBD
from Funciones2.acq_mode01 import fOBD2Mode01
from Funciones2.Gest_Files import read_DataFile as Readfiles
from Funciones2.Rutas import path
import threading, time, logging, os, redis
r = redis.Redis(host='127.0.0.1', port=6379, db=1)

def t_raspi():
    h_raspi = threading.currentThread()
    while getattr(h_raspi, "activar_raspi" , True):
        fRASPI()
def t_GestionBD():
    h_GestionBD = threading.currentThread()
    while getattr(h_GestionBD, "activar_GestionBD", True): 
        fgestionBD()
def t_obdauto(): #OBD MODE01 PROTOCOLO AUTO SELECCCIÓN
    #h_obdauto = threading.currentThread()
        fOBD2Mode01()
def t_Camera():
    def fcamera():
        os.system('python /home/morenomx/Documents/Soluciones_MM/OBD2MM/FORK/OBD2MM_v1/OBD2MM/RaspiCarWebSite/Funciones2/Camera.py')
    htt_Camera = threading.Thread(target=fcamera)
    try:
        htt_Camera.start()
    except:
        logging.warning('error abriendo Funcion FCAMERA')
def t_cam_auto():
    def fCameraAuto():
        os.system('python /home/morenomx/Documents/Soluciones_MM/OBD2MM/FORK/OBD2MM_v1/OBD2MM/RaspiCarWebSite/Funciones2/Camera_Auto.py')
    htt_CameraAuto = threading.Thread(target=fCameraAuto)
    try:
        htt_CameraAuto.start()
    except:
        logging.warning('error abriendo Funcion FCAMERA')    
            