import json, time, logging
import gpiozero as gz
from vcgencmd import Vcgencmd
from Funciones2.Gest_Files import read_DataFile as Readfiles
#from Funciones2.Gest_Files import write_DataFile as Writefiles
#from Funciones.Gest_Files import read_DataFile  #para probar localmente:// from Gest_Files import read_DataFile
from Funciones2.Rutas import path  #ej: print(path()['p_media'])  Para probar localmente:// from Rutas import path 
import psutil, redis
salir=False
bStartDdebugRASPI=False #COLOCAR EN TRUE VIA CÓDIGO PARA EL DEBUGGER.
r = redis.Redis(host='127.0.0.1', port=6379, db=1)

#logging.basicConfig(level = logging.INFO, format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,filename=path()['p_data']+'raspi.log',filemode='a')

def fRASPI():

    if (r.get('SALIR')) == b'True' or (r.get('SALIR_RASPI'))== b'True':
        logging.info('raspi-W01: SALIENDO DE ADQUISICION DE PARAMAETROS RASPI')
        exit()
    else:
        Data01={}
    #Data_Flags=read_DataFile(path()['p_data'], 'flags.json', 'Error abirendo fichero json para lectura de orden de Inicio/Apagado de módulos y0')
        disk_usage = psutil.disk_usage("/")
        UsedHDD=round((disk_usage.used/1024**3),2)
        FreeHDD=round((disk_usage.free/1024**3),2)
        PercentHDD =disk_usage.percent
        TempCPU = round(gz.CPUTemperature().temperature,2)
        TempGPU= round(Vcgencmd().measure_temp(),2)
        Data01={"TempCPU":str(TempCPU),"TempGPU":str(TempGPU), "UsedHDD":str(UsedHDD), "FreeHDD": str(FreeHDD), "PercentHDD":str(PercentHDD)}
        if bStartDdebugRASPI:
            logging.info('raspi-W02: ' + str(Data01))
            logging.info('raspi-W03: '+ str(UsedHDD) + ' Gb' +str(FreeHDD)+ ' Gb' + str(PercentHDD) +' %')
        time.sleep(0.3)
        r.mset(Data01)
       
        

        



   
    
         
       