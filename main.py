from __future__ import print_function
import time
import pyupm_mic as upmMicrophone

myMic = upmMicrophone.Microphone(0)
threshContext = upmMicrophone.thresholdContext()
threshContext.averageReading = 0
threshContext.runningAverage = 0
threshContext.averagedOver = 2

values = []
average = 0
clap = False

while(1):
  buffer = upmMicrophone.uint16Array(128)
  length = myMic.getSampledWindow(2, 128, buffer)
  if length:
    thresh = myMic.findThreshold(threshContext, 30, buffer, length)
    if thresh:
      if average > 0 and thresh > average * 1.1 and not clap:
        print("clap")
        clap = True
      values.append(thresh)
      if len(values) >= 5:
        if values[-1] == values[-2] == values[-3] == values[-4] == values[-5]:
          print("threshold established: %d" % values[-1])
          average = values[-1]
          clap = False

del myMic

