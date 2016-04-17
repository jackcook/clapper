import pyupm_mic as microphone
import requests
import time
import pyupm_grove as grove
import mraa
import sys
import pyupm_grove

mic = microphone.Microphone(0)

threshContext = microphone.thresholdContext()
threshContext.averageReading = 0
threshContext.runningAverage = 0
threshContext.averagedOver = 2

values = []
average = 0
clap = 0
last = 0

def read_sound_sensor():
    global average, clap, last, values

    buffer = microphone.uint16Array(128)
    length = mic.getSampledWindow(2, 128, buffer)
    if length:
        thresh = mic.findThreshold(threshContext, 30, buffer, length)
        if thresh:
            if average > 0 and thresh > average * 1.1 and thresh > last:
                clap += 1
                print "claps: %d" % clap
            values.append(thresh)
            if len(values) >= 3:
                if values[-1] == values[-2] == values[-3]:
                    if clap > 0:
                        try:
                            requests.get("http://172.20.10.1:12345/clap?n=%d" % clap)
                        except:
                            print "host is down"
                    print "threshold established: %d" % values[-1]
                    average = values[-1]
                    clap = 0
        last = thresh
"""
def read_light_sensor():
    print "light"

while 1:
    read_sound_sensor()
    read_light_sensor()

del mic

light=grove.groveLight(3)

while 1:
    print light.name() + "raw value is %d" % light.raw_value()+\
        ", which is roughly %d" %light.value() + " lux";
    time.sleep(3)

del light"""


LIGHT_SENSOR_PIN=3
MAX_LIGHT = 50
LED_PWM_PIN=5

def main(): 
    light = pyupm_grove.GroveLight(LIGHT_SENSOR_PIN)
    pwm = mraa.Pwm(LED_PWM_PIN)
    pwm.period_us(5000) # Set the period as 5000 us or 5ms
    pwm.enable(True)    # enable PWM
    pwm.write(0)    
    print "Light sensor bar:"
    while True:
        ambientLight = light.value()
        sys.stdout.write("Light sensor: %02d " %ambientLight)
        sys.stdout.write("[")
        tempLight = ambientLight
        if tempLight > MAX_LIGHT:
            tempLight = MAX_LIGHT      # Nromalize the value
            
        pwmValue = (MAX_LIGHT - tempLight)/float(MAX_LIGHT)

        pwm.write(pwmValue)
        
        for i in range(0, MAX_LIGHT):
            if ambientLight > i:
                sys.stdout.write("=")
            elif ambientLight == i:
                sys.stdout.write("|")
            else:
                sys.stdout.write(" ")
            sys.stdout.write("]  \r")
        sys.stdout.flush()
        time.sleep(0.1)
if __name__ == "__main__":
    main()
