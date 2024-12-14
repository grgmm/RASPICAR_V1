import serial
import json
import time
#MODULO ADAPTADO PARA EL CITROEN SAXO 1.5V SOLO OBTENEMOS LAS RPM Y EL TIPOD EL TIPO DE OBD COMPLIANCE"

def fOBDmode01_p4(bStartOBD_P4, bimprmirvalores_p4):
    if bStartOBD_P4:
        PIDS = {
            "SUPPORTED":b"00",
            #"THROTTLE_POS":b"11",
            "RPM":b"0C",
            #"SPEED":b"0D",
            #"COOLANT_TEMP":b"05",
            #"INTAKE_TEMP":b"0f",
            #"ENGINE_LOAD":b"04",
            "PIDS_A":b"00",
            "OBD2_COMPLIANCE":b"1C",
            }
        def mode1(pid, ser):
                res = cmd(b"01"+PIDS[pid], ser).split(b"\r")
            
                data = res[1].split()
                print(data)
                if data != []:
                
                    if data[0] == b"41" and data[1] == PIDS[pid]:
                        
                            vs = b"".join(data[2:]).decode('ascii')
                            value = int(vs, 16)
            
                            return value
                    else:
                        
                        return 0

        def cmd(cmd, ser):
            out=b'';prev=b'101001011'
            ser.flushInput();ser.flushOutput()
            ser.write(cmd+b'\r');
            while True:
                try:
                    out+= ser.read(1)
                    if prev == out: return out
                    prev=out
                except:
                    print ('FALLA EN LECTURA DEL SCNNER ELM327, REINTENTANDO')
                    break
                      
            return out
        def init(port, ser):
        
                ser.timeout= 1.0 #0.3
                print( cmd(b"ATZ", ser))
                print( cmd(b"ATTP4", ser))
                print( cmd(b"ATKW0", ser)) 
                print(cmd(b"ATRV", ser)) 
                ser.timeout=1.0 
        
                print( cmd(b"0100", ser) )
                ser.timeout=1.0   #0.3
        #if __name__ == '__main__':
                #port = sys.argv[1]
        port='/dev/rfcomm0'
        ser = serial.Serial(port, 38400, timeout=1.0)
        init(port, ser)   
        ser.timeout= 1.0   #0.3
        supported = mode1("SUPPORTED", ser)
        print( "PIDS supported: %s " % supported)
        time.sleep(1)
        while True:
                    pida=mode1("PIDS_A",ser)
                    pidabin=bin(int(pida))[2:] 
                    rpm = mode1("RPM", ser) / 4
                    rpm=rpm*100
                    ObdCompliance= mode1("OBD2_COMPLIANCE", ser)
                    if bimprmirvalores_p4 and bStartOBD_P4:
                        print( "PIDS_A: %s " % pidabin)
                        print( "Engine RPM: %s [rpm]" % rpm)
                        print( "ObdCompliance: %s" % str(ObdCompliance)+" = EOBD (Europe)") #https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_01_PID_1C
                    #pos = mode1("THROTTLE_POS", ser) *100/255
                    #print( "Throttle position: %s [%%]" % pos)
                    #speed = mode1("SPEED", ser)
                    #print( "Vehicle speed: %s [km/h]" % speed)
                    #oil_temp = mode1("OIL_TEMP", ser)
                    #print( "OIL_TEM`P: %s [Grados]" % oil_temp)  
                    #ctemp = mode1("COOLANT_TEMP", ser) 
                    #print( "Engine coolant temperature: %s [C]" % ctemp)   
                    #eload = mode1("ENGINE_LOAD", ser) *100/255
                    #print( "Engine load: %s [%%]" % eload)
                    Data={'mode01_p4':
                             {'rpm':str(rpm),"OBD2_COMPLIANCE": ObdCompliance, "pida":pidabin
                              }                             
                              } 
                    try:
                            with open ('/home/morenomx/Documents/Soluciones_MM/OBD2MM/OBD2MM/Data/mode01_P4.json', 'w') as jmode01_P4:
                                json.dump(Data , jmode01_P4)
                                #print(json.dump.Data)
                    except:
                            print ('Error abirendo afichero json para escritura mode01_p4, posible ignitción en Off')
        ser.close()
#fOBDmode01_p4(bStartOBD_P4=True, bimprmirvalores_p4=True)