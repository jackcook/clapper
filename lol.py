import pyupm_mic as upmMicrophone
import requests
import time

myMic = upmMicrophone.Microphone(0)
threshContext = upmMicrophone.thresholdContext()
threshContext.averageReading = 0
threshContext.runningAverage = 0
threshContext.averagedOver = 2

values = []
average = 0
clap = 0
last = 0

while(1):
  buffer = upmMicrophone.uint16Array(128)
  length = myMic.getSampledWindow(2, 128, buffer)
  if length:
    thresh = myMic.findThreshold(threshContext, 30, buffer, length)
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

del myMic

