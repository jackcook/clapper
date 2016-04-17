import pyupm_mic as microphone
import requests
import time
import pyupm_grove as grove

mic = microphone.Microphone(0)
light = grove.GroveLight(3)
temp = grove.GroveTemp(2)

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

def read_light_sensor():
    try:
        requests.get("http://172.20.10.1:12345/light?n=%d" % light.value())
    except:
        print "host is down"

    print "%s raw value is %d lux" % (light.name(), light.value())

def read_temp_sensor():
    celcius=temp.value()
    fahrenheit=celcius*9.0/5.0+32.0;
    print "%d degrees Fahrenheit" % fahrenheit
    try:
        request.get("http://172.20.10.1:12345/temperature?n=%d" % fahrenheit)
    except:
        print "host is down"

while 1:
    read_sound_sensor()
    read_light_sensor()
    read_temp_sensor()
