import pyupm_mic as microphone
import requests
import time
import pyupm_grove as grove

mic = microphone.Microphone(0)
light = grove.GroveLight(3)
temp = grove.GroveTemp(2)
knob= grove.GroveRotary(1)

threshContext = microphone.thresholdContext()
threshContext.averageReading = 0
threshContext.runningAverage = 0
threshContext.averagedOver = 2

values = []
average = 0
clap = False

def read_sound_sensor():
    global average, clap, values

    buffer = microphone.uint16Array(128)
    length = mic.getSampledWindow(2, 128, buffer)
    if length:
        thresh = mic.findThreshold(threshContext, 30, buffer, length)
        print thresh
        mic.printGraph(threshContext)
        if thresh:
            if average > 0 and thresh > average * 1.1 and not clap:
                print "clap"
                clap = True
                try:
                    requests.get("http://172.20.10.1:12345/clap")
                except:
                    pass
            values.append(thresh)
            if len(values) >= 2:
                if values[-1] == values[-2]:
                    print "threshold established: %d" % values[-1]
                    average = values[-1]
                    clap = False

def read_light_sensor():
    try:
        requests.get("http://172.20.10.1:12345/light?n=%d" % light.value())
    except:
        pass

def read_temp_sensor():
    celcius=temp.value()
    fahrenheit=celcius*9.0/5.0+32.0;
    try:
        requests.get("http://172.20.10.1:12345/temperature?n=%d" % 
fahrenheit)
    except:
        pass

def read_angled_sensor():
    absdeg = int(knob.abs_deg())
    try:
        requests.get("http://172.20.10.1:12345/flash?n=%d" % absdeg)
    except:
        pass

while 1:
    read_sound_sensor()
    read_light_sensor()
    read_temp_sensor()
    read_angled_sensor()
