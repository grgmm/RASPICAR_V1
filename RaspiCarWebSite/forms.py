from flask_wtf import FlaskForm
#from wtforms.validators import DataRequired
from wtforms import BooleanField, SubmitField, validators
class Modulos_form(FlaskForm):
    OBD2_AUTO  = BooleanField(label = 'OBD2 (COCHES NUEVOS)', )
    OBD2_AUTO_DEBUGGER = BooleanField(label = 'Activar DEBUGGER OBD2_AUTO', )
    OBD2_P4 = BooleanField(label ='OBD2 (COCHES ANTIGUOS)',)
    OBD2_P4_DEBUGGER = BooleanField(label = 'Activar DEBUGGER OBD2_P4', )
    Integridad_Raspi = BooleanField(label ='INTEGRIDAD RASPI ')
    Integridad_Raspi_DEBUGGER  = BooleanField(label ='Activar DEBUGGER de Integridad de la RASPI B3')
    GestionBD = BooleanField(label ='DATABASE')
    GestionBD_DEBUGGER  = BooleanField(label ='Activar DEBUGGER de Gestión de la Base de Datos')
    Camera_Auto=BooleanField(label ='ACTIVAR CAMARA')
    SALIR  = BooleanField(label ='DETENER RASPICAR')   
    submit = SubmitField('Aceptar')