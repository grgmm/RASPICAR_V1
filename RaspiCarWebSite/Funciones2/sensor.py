from gpiozero import DistanceSensor
import redis, random, time
from colorzero import color
sensor = DistanceSensor(trigger=18, echo=24) #BCM gpio18 == FISICO(pin12), BCM gpio24 == FISICO(pin18)



def proximidad():
    promediar = False
    iteracion=0
    distanceCm=0
    try:
        while not (promediar):
            iteracion+=1
            distanceCmtemp =  sensor.distance*100
            distanceCm=(distanceCm+distanceCmtemp)/2
            distanceCm=round(distanceCm, 2)
            time.sleep(0.3)
            if iteracion ==3:
                promediar = True
        sensor_when_out_of_range=sensor.when_out_of_range
        s = redis.Redis(host='127.0.0.1', port=6379, db=1)
        s.set('distanceCm', distanceCm)
        s.set('sensor_when_out_of_range', str(sensor_when_out_of_range))
        return(distanceCm , sensor_when_out_of_range)
    except ValueError as er:
        return(er)

    



