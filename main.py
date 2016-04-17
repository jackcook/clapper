import time
import pyupm_mic as upmMicrophone
from statistics import mean
from datetime import datetime
from threading import Timer
import time
def timeout():
	print("Five Seconds Are Over")
t=Timer(5,timeout)
t.start()

myMic = upmMicrophone.Microphone(0)
"""
threshContext = upmMicrophone.thresholdContext()
threshContext.averageReading = 0
threshContext.runningAverage = 0
threshContext.averagedOver = 2
"""
def counting():
  buffer = upmMicrophone.uint16Array(128)
  length = myMic.getSampledWindow(2, 128, buffer)
  if length:
    thresh = myMic.findThreshold(threshContext, 30, buffer, length)
    if thresh:
      if average > 0 and thresh > average * 1.1 and not clap:
        print("clap")
        print average
        clap = True
      else:
        clap = False
  return clap

def count():
  y=counting()
  x=0
  if y==True:
    x+=1
    y=counting()
  else:
    pass
  return x

"""
myTime=datetime.now()
averageValues=[]
theTime="it is %s o'clock %s minutes and %s seconds" %(myTime.hour,
myTime.minute, myTime.second)
print theTime
"""
myMic = upmMicrophone.Microphone(0)
threshContext = upmMicrophone.thresholdContext()
threshContext.averageReading = 0
threshContext.runningAverage = 0
threshContext.averagedOver = 2
"""
values = []
average = 0
clap = False"""

while(1):
  """ buffer = upmMicrophone.uint16Array(128)
  length = myMic.getSampledWindow(2, 128, buffer)
  if length:
    thresh = myMic.findThreshold(threshContext, 30, buffer, length)
    if thresh:
      if average > 0 and thresh > average * 1.1 and not clap:
        print("clap")
        print average
        clap = True
      values.append(thresh)"""
  x=counting()
  if x==0:
    print 'z'
  elif x==1:
    print 'a'
  elif x==2:
    print 'b'
  elif x==3:
    print 'c'
  else:
    print 'd'
  x=0


"""      if len(values) >= 5:
        if values[-1] == values[-2] == values[-3] == values[-4] == 
values[-5]:
          print("threshold established: %d" % values[-1])
          average = values[-1]
          clap = False
"""
del myMic





myTime=datetime.now()
timeData=[]
myTimeSeconds=myTime.second()
#timeData.append(myTime.second)
def average(values):
   sum=0
   count=0
   for i in values:
      sum+=int(i)
      count+=1
   mean=sum/count
   print mean

def findaverage():
   values=[]
   for i in range(0,10):
      threshContent=upmMicrophone.thresholdContext()
      values+=[threshContent]
   #mymean=average(values)
   return values

myTime=dateTime.now()
def ifclap():
   mymean=findaverage()
   count=0
   while(1):
      while myTime.second+3>myTime:
         threshcontent=upmMicrophone.threshholdContext()
         if threshcontent>=mymean*1.1:
            clap=true
         else:
            pass
         if clap==true:
            count+=1
         else:
            pass
   return count

