#from gpiozero import DistanceSensor
import redis, random
def proximidad():
    try:
        #sensor = DistanceSensor(trigger=18, echo=24) #BCM gpio18 == FISICO(pin12), BCM gpio24 == FISICO(pin18)
        #distanceCm =  round(sensor.distance*100,2)
        distanceCm= random.uniform(1.5 , 30.0)
        #sensor_when_out_of_range=sensor.when_out_of_range
        sensor_when_out_of_range = False
        s = redis.Redis(host='127.0.0.1', port=6379, db=1)
        s.set('distanceCm', distanceCm)
        s.set('sensor_when_out_of_range', str(sensor_when_out_of_range))
    except ValueError as er:
    #except DistanceSensorNoEcho as er:
        print(er)
        return(er)
    return(distanceCm , sensor_when_out_of_range)



