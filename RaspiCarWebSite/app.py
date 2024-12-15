from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, redirect,  url_for
from forms import Modulos_form
import os, json, threading, logging, time
from logging.handlers import RotatingFileHandler
from Funciones2.Rutas import path
from Funciones2.GestHilos.hilos import t_Camera, t_raspi, t_GestionBD, t_obdauto, t_cam_auto
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
import redis
r = redis.Redis(host='127.0.0.1', port=6379, db=1)
##########################################################################################################################################################################
#LOGGING CONFIGURATION
logger = logging.getLogger('app_logger ')
handler = RotatingFileHandler(path()['p_data']+'app.log', maxBytes=2000, backupCount=10)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
############################################################## 
# Handler para log en archivo
file_handler = logging.FileHandler(path()['p_data']+'app.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
#############################################################
###### Handler para logs en consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
##########################################################################################################################################################################
logging.basicConfig(level = logging.DEBUG, format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,filename=path()['p_data']+'app.log',filemode='a')
Flags_Data= {'SALIR':False}
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'
app.config['SECRET_KEY'] = SECRET_KEY
Salir_Data= {'SALIR':False,'SALIR_RASPI':False, 'SALIR_BD':False, 'SALIR_OBDAUTO':False,'SALIR_CAMARA_AUTO':False }
Camera_Data= {'Camera_Activa':False}
Salir_Dic= {'SALIR':'False','SALIR_RASPI':'False', 'SALIR_BD':'False', 'SALIR_OBDAUTO':'False','SALIR_CAMARA_AUTO':'False' }
r.mset(Salir_Dic)
r.set('Camera_Activa','False')
@app.route('/')
def Index():
    menu=['MODULOS', 'GRAFICOS', 'CAMARA(5min)', 'SALIR']
    return render_template('/Principal/index.html', menu=menu)
######################################### SALIR #############################
@app.route('/Salir')
def Salir():
    r.set("SALIR", "True")
    r.set("Camera_Activa", "False")
    return render_template('/Principal/salir.html')
@app.route('/Modulos', methods=['GET', 'POST'])
def Modulos():
    form = Modulos_form()
    if form.validate_on_submit():
        #print(form.data)
        Flags_Data=form.data
################## OBD COCHES NUEVOS(Mode 01 PROTOCOLO: AUTO SELECCION) #######################
        global ht_obdauto
        ht_obdauto = threading.Thread(target=t_obdauto)
        if Flags_Data['OBD2_AUTO']:
            logger.info('app-I05: INICIANDO MÓDULO OBD AUTO')
            r.mset({"SALIR":"False", "SALIR_OBDAUTO":"False"})
            activar_obdauto = True
            ht_obdauto.start()
            if ht_obdauto.is_alive:
                obdauto_run= True
            else:
                obdauto_run= False
            #ht_obdauto.join()
        else:
            activar_obdauto =  False
            r.set("SALIR_OBDAUTO", "True")
################## PARAMETROS DE LA RASPI     #######################
        global ht_raspi
        ht_raspi = threading.Thread(target=t_raspi)
        if Flags_Data['Integridad_Raspi']:
            logger.info('app-I06: INICIANDO MÓDULO INTEGRIDAD RASPI')
            r.mset({"SALIR":"False", "SALIR_RASPI":"False"})
            activar_raspi = True
            ht_raspi.start()
            if ht_raspi.is_alive:
                raspi_run= True
            else:
                raspi_run= False
        else:
            activar_raspi =  False
            Salir_Data['SALIR_RASPI']=True
            r.set("SALIR_RASPI", "True")
################## BASE DE DATOS  #######################
        global ht_GestionBD
        ht_GestionBD = threading.Thread(target=t_GestionBD)
        if Flags_Data['GestionBD']:
            logger.info('app-I03: INICIANDO ALMACENAMIENTO EN BD')
            r.mset({"SALIR":"False", "SALIR_BD":"False"})
            activar_GestionBD = True
            ht_GestionBD.start()
            if ht_GestionBD.is_alive:
                GestionBD_run= True
            else:
                GestionBD_run= False
        else:
            r.set('SALIR_BD', 'True')
            ht_GestionBD.activar = False
            if ht_GestionBD.is_alive():
                GestionBD_run =True
                ht_GestionBD.join()
            else:
                GestionBD_run =False
                activar_GestionBD = False
      ################## CAMARA ACTIVACION AUTO (SENSOR DE PROXIMIDAD) #######################
        global ht_cam_auto
        ht_cam_auto = threading.Thread(target=t_cam_auto)
        if Flags_Data['Camera_Auto']:
            logger.info('app-I04: INICIANDO MÓDULO CAMARA AUTO')
            r.mset({'SALIR':'False', 'SALIR_CAMARA_AUTO':'False'})
            activar_cam_auto = True
            ht_cam_auto.start()
            if ht_cam_auto.is_alive:
                cam_auto_run= True
            else:
                cam_auto_run= False
        else:
            activar_cam_auto =  False
            r.set('SALIR_CAMARA_AUTO', 'True')
        return redirect(url_for('Index'))
    return render_template("/Principal/Forms/modulos.html", form=form)
@app.route('/Cam')
def Cam():
     ################## COMANDO DE LA CAMARA ACTIVACION MANUAL   #######################
    ht_Camera = threading.Thread(target= t_Camera)
    ht_Camera.daemon=True
    ht_Camera.start()
    return redirect(url_for('Index'))   
    #return render_template('/Principal/salir.html')
if __name__ == '__main__':
    logger.info('app-I00: GRG SYSTEMS BIENVENIDO A RASPICAR')
    try:
        app.run(debug=True, host='0.0.0.0')
        app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'solar'
    except ValueError as er:
        logger.warning('app-W00: '+ str(er))