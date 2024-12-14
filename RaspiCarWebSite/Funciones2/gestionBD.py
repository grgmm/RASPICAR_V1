from datetime import datetime
import psycopg2, json, time, re, logging, redis
from Funciones2.Gest_Files import read_DataFile  as  Readfiles #para robar localmente:// from Gest_Files import read_DataFile
from Funciones2.Rutas import path
r = redis.Redis(host='127.0.0.1', port=6379, db=1)
Datamode01_p4={'mode01_p4':{}}
bStartOBD_DEBUGGER= False #Colocar en true via código para debugger
bStartOBD_p4_DEBUGGER= False #Colocar en true via código para debugger
bStartRASPI_DEBUGGER= False #Colocar en true via código para debugger
#logging.basicConfig(level = logging.INFO, format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,filename=path()['p_data']+'bd.log',filemode='a')
bStartOBD= False
bStartAcqRaspi= True
bStartOBD_P4 = False
fcoolanttemp=0
def fgestionBD():
        

        
        if (r.get('SALIR')) == b'True' or (r.get('SALIR_BD'))== b'True':
                logging.info('DB-I01: SALIENDO DE GESTION DE BASE DE DATOS')
                exit()
        #bStartOBD_P4 = bStartOBD_P4 = Data_Flags['OBD2_P4']
        #bStartAcqRaspi= Data_Flags['Integridad_Raspi']
        #bStartOBD = Data_Flags['OBD2_AUTO']
        Values=""
        ValuesTemp=Values
        Values1=""
        ValuesTemp1=""
        Values2=""
        ValuesTemp2=Values2
        #if bStartAcqRaspi:
        if r.get('SALIR_RASPI')==b'False':
                        try:
                                db=psycopg2.connect(database="obd2mm", user="morenomx", password="Mm262517")
                                while db:
                                        #TempCPU=DataRaspi['raspi']['TempCPU']
                                        TempCPU=r.get('TempCPU')
                                        TempCPU=float(TempCPU.decode('utf-8'))
                                        #print(TempCPU, type(TempCPU))
                                        #TempGPU=DataRaspi['raspi']['TempGPU']
                                        TempGPU=r.get('TempGPU')
                                        TempGPU=float(TempGPU.decode('utf-8'))
                                        #UsedHDD=DataRaspi['raspi']['UsedHDD']
                                        UsedHDD=r.get('UsedHDD')
                                        UsedHDD=float(UsedHDD.decode('utf-8'))
                                        #FreeHDD= DataRaspi['raspi']['FreeHDD']
                                        FreeHDD=r.get('FreeHDD')
                                        FreeHDD=float(FreeHDD.decode('utf-8'))
                                        #PercentHDD=DataRaspi['raspi']['PercentHDD']
                                        PercentHDD=r.get('PercentHDD')
                                        PercentHDD=float(PercentHDD.decode('utf-8'))
                                        cursor= db.cursor()
                                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                        sql="insert into raspi(tempcpu, tempgpu, usedhdd, freehdd, percenthdd, timestamp) values (%s,%s,%s,%s,%s,%s)"
                                        datos=(TempCPU,TempGPU, UsedHDD, FreeHDD, PercentHDD,  timestamp)
                                        Values=(TempCPU, TempGPU, UsedHDD, FreeHDD, PercentHDD)
                                        #print(Values)
                                        #cursor.execute("SELECT * FROM raspi ORDER BY timestamp LIMIT 1")
                                        #lastrow = cursor.fetchone()
                                        #print(lastrow)
                                        #column_names = [desc[0] for desc in cursor.description]
                                        #print(column_names)
                                        #lastregister= dict(zip(column_names,lastrow))
                                        #lastregister=lastregister.pop('jdata')
                                        #print(lastregister['raspi'])
                                        time.sleep(2)
                                        if (Values != ValuesTemp):
                                                cursor.execute(sql, datos)
                                                time.sleep(5)
                                                ValuesTemp=Values
                                                if bStartRASPI_DEBUGGER:
                                                         logging.info(datos)
                                                try:
                                                        db.commit() 
                                                        logging.info('DB-I01: ALMACENANDO EN BD '+ 
                                                        'TempCPU=' +str(TempCPU)+' '
                                                        + 'TempGPU='+str(TempGPU)+' '
                                                        + 'UsedHDD='+str(UsedHDD)+' '
                                                        + 'FreeHDD='+str(FreeHDD)  +' '
                                                        + 'PercentHDD='+str(PercentHDD)
                                                        )
                                                        #db.close()
                                                
                                                except Exception as e:
                                                        logging.warning('DB-W01: Error Conectando con BD'+ str(e))
                                        else:
                                                logging.info('DB-I02: Data repetida No se almacema en BD')
                        except Exception as e:
                                logging.warning('DB-W02: Error Conectando con BD'+ str(e))
        #if bStartOBD:
        if r.get('SALIR_OBDAUTO')==b'False':
                '''fcoolanttemp=0
                fruntime=0
                fintakepressure=0
                fdistancesincedtcclear=0
                frpm=0'''
                try:
                        db1=psycopg2.connect(database="obd2mm", user="morenomx", password="Mm262517")
                        while db1:
                                try: 
                                        time.sleep(5)
                                       
                                        keys = r.keys('*')
                                        #for key in keys: 
                                                #value = r.get(key) 
                                                #print(f'{key}:')
                                        if (b'COOLANT_TEMP') in keys:
                                                scoolanttemp=r.get('COOLANT_TEMP')
                                                fcoolanttemps=([float(s) for s in re.findall(r"-?\d+\.?\d*", str(scoolanttemp))]) # Obtiene en una lista los numeros presentes en una cadena
                                                fcoolanttemp=fcoolanttemps[0]
                                                

                                        if (b'RUN_TIME') in keys:
                                                sruntime=r.get('RUN_TIME')
                                                fruntimes=([float(s) for s in re.findall(r"-?\d+\.?\d*", str(sruntime))])
                                                fruntime=fruntimes[0]

                                        if (b'INTAKE_PRESSURE') in keys:
                                                sintakepressure=r.get('INTAKE_PRESSURE')
                                                fintakepressures=([float(s) for s in re.findall(r"-?\d+\.?\d*", str(sintakepressure))])
                                                fintakepressure=fintakepressures[0]
                                                

                                        if (b'DISTANCE_SINCE_DTC_CLEAR') in keys:
                                                sdistancesincedtcclear=r.get('DISTANCE_SINCE_DTC_CLEAR')
                                                fdistancesincedtcclears=([float(s) for s in re.findall(r"-?\d+\.?\d*", str(sdistancesincedtcclear))])
                                                fdistancesincedtcclear=fdistancesincedtcclears[0]
                                        
                                        if (b'DISTANCE_SINCE_DTC_CLEAR') in keys:
                                                srpm=r.get('RPM')
                                                frpms=([float(s) for s in re.findall(r"-?\d+\.?\d*", str(srpm))])
                                                frpm=frpms[0]

                                        cursor1= db1.cursor()
                                        timestamp1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                        Values1=(fcoolanttemp, fruntime, fintakepressure, fdistancesincedtcclear, frpm )
                                        sql1 = "INSERT INTO mode01(coolanttemp, runtime, intakepressure, distancesincedtcclear, rpm, timestamp) VALUES (%s,%s,%s,%s,%s,%s)"
                                        datos1 =(fcoolanttemp, fruntime, fintakepressure, fdistancesincedtcclear, frpm, timestamp1)
                                        if (Values1 != ValuesTemp1):
                                                #print('almacenando en BD..............')
                                                cursor1.execute(sql1,datos1)
                                                time.sleep(2)
                                                ValuesTemp1=Values1
                                                try:
                                                        db1.commit()
                                                        logging.info('DB-I03: Almacenando en BD')
                                                except Exception as e:
                                                        logging.warning('DB-W03: '+ str(e))
                                        else:
                                                logging.info('DB-I04: Data repetida No se almacema en BD')
                                except Exception as e: 
                                        logging.warning('DB-W05: '+ str(e))
                except Exception as e:
                        logging.warning('DB-W06: Error Conectando con BD ' + str(e))
        
                
                
