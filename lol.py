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
        if thresh:
            if average > 0 and thresh > average * 1.1 and not clap:
                print "clap"
                clap = True
                try:
                    requests.get("http://172.20.10.1:12345/clap")
                except:
                    print "host is down"
            values.append(thresh)
            if len(values) >= 3:
                if values[-1] == values[-2] == values[-3]:
                    print "threshold established: %d" % values[-1]
                    average = values[-1]
                    clap = False

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

def read_angled_sensor():
    abs = knob.abs_value()
    absdeg = knob.abs_deg()
    absrad = knob.abs_rad()
    rel = knob.rel_value()
    reldeg = knob.rel_deg()
    relrad = knoob.rel_rad()
    print "Abs values: %4d" %int(abs), "raw %4d" % int(absdeg)
    print "Rel values: %4d" %int(rel), "raw %4d" %int(reldeg)


while 1:
    read_sound_sensor()
    read_light_sensor()
    read_temp_sensor()
    read_angled_sensor()
