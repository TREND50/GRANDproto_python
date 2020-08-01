# Base script to analyse standard data written in txt (yaml) format
# OMH Aug 29, 2018

import os
import time
import sys
import math
import yaml  # To read data in txt format
import numpy as np
import pylab as pl
from scipy.optimize import curve_fit

# Binary dat ainterpreter: pyef
# module. Do ./setup.py build & ./setup.py install if not loadable [email Gu Junhua Sept 27 2017]
#import pyef

DISPLAY = 0
print 'DISPLAY = ',DISPLAY 
pl.ion()

def loopEvents(RUNID,boardID,TYPE):
   #datadir = "/home/pastsoft/data"
   datadir = "/home/martineau/GRAND/GRANDproto35/data/"
   filename = datadir+TYPE+RUNID+".data.yaml"
   if os.path.isfile(filename) is False:
     print 'File ',filename,'does not exist. Aborting.'
     return

   datafile = filename.split('/')
   if TYPE == 'C':
     nch = 4   # Plot calibrator channel
   else:
     nch = 3
   
   # Read data
   print 'Scanning data file',filename
   print "Loading data..."
   dataf=yaml.load_all(open(filename))
   print "Done."
   
   data = list()
   freq=50e6  # Sampling Frequency
   dt=1.0/freq
   tdeb = 0
   tend = 0   
   date = []
   IP = []
   TS1Trig = []
   SSS = []
   TS2 = []
   TS1PPS = []
   EvtId = []
   TrigPattern = []
   board = []
   imax = []
   Amax = []
   mub = []
   sigb = []
	   
   # Loop on events
   j = 0;  # Index of array filling (because date & data are "append")
   #try:
   if 1:
     for d in dataf:
       #determine whether it is a data:
       if d['msg_type']=='DATA':
           #print d.keys()
	   print "Event",j,"from ID ",d['source_ip']
   	   print d['event_count']
	   IP.append(d['source_ip'])
	   board.append(int(d['source_ip'][-1])-100)
   	   TS1Trig.append(d['ts1trigger'])
	   SSS.append(d['sss'])
	   TS2.append(d['ts2'])
	   TS1PPS.append(d['ts1pps'])
	   EvtId.append(d['event_count'])
	   TrigPattern.append(d['trig_pattern'])
	   date.append(d['received_timestamp_str'])
	   raw=d['data']
	   #raw2 = raw[0].split(" ") # Cut raw data list into samples
	   #raw2 = raw2[0:np.size(raw2)-1]   # Remove last element (empty)
   	   raw2 = raw
	   if TYPE == "P":  # Pattern run, keep data value in binary format
	        draw = [int(a) for a in raw2] 
	   else:  # Other run types
  	        hraw2 = [hex(int(a)) for a in raw2]  # Transfer back to hexadecimal
	        draw = [twos_comp(int(a,16), 12) for a in hraw2] #2s complements		   
           if TYPE != "P":  # Transfer data to volts 
	     draw = np.array(draw)*1./2048  # in Volts
	   
   	   nsamples = len(draw)/4  # draw corresponds to 4 channels
   	   offset = int(nsamples/2.0)  # Offset position at center of waveform
   	   #print nsamples,"samples per channel --> offset = ",offset
	   thisEvent = np.reshape(draw,(4,nsamples));
   	   data.append(thisEvent) # Write to data list
	   #print 'Sampling frequency=',freq,'MHz, time step=',dt,'s'
	   
	   if DISPLAY:
	     print 'Event ',j
	     thisEv = pow(10,(thisEvent+np.min(thisEvent)))
	     t = dt*np.array(range(np.shape(thisEvent)[1]))
 	     t = t* 1e6  #in mus
 	     pl.figure(j)
	     if TYPE == "C":
   	       pl.subplot(221)
 	     else:
	       pl.subplot(311)
 	     #pl.plot(t[3:],thisEvent[0][3:])
	     pl.plot(t[3:],thisEv[0][3:])
 	     pl.xlim(t[3],max(t))
 	     pl.xlabel('Time ($\mu$s)')
 	     if TYPE == "P":
	       pl.ylabel('LSB')
	     else:
	       pl.ylabel('Amplitude (V)')
 	     pl.grid(True)
	     if TYPE == "C":
   	       pl.subplot(222)
 	     else:
	       pl.subplot(312)
 	     pl.xlabel('Time ($\mu$s)')
 	     pl.xlim(t[3],max(t))
 	     if TYPE == "0":
	       pl.ylabel('LSB')
	     else:
	       pl.ylabel('Amplitude (V)')
	     #pl.plot(t[3:],thisEvent[1][3:])
 	     pl.plot(t[3:],thisEv[1][3:])
 	     pl.grid(True)
	     if TYPE == "C":
   	       pl.subplot(223)
 	     else:
	       pl.subplot(313)
 	     #pl.plot(t[3:],thisEvent[2][3:])
             pl.plot(t[3:],thisEv[2][3:])
             pl.xlim(t[3],max(t))
 	     pl.xlabel('Time ($\mu$s)')
 	     if TYPE == "P":
	       pl.ylabel('LSB')
	     else:
	       pl.ylabel('Amplitude (V)')
 	     pl.grid(True)
	     if TYPE == "C":
 	       pl.subplot(224)
 	       pl.plot(t[3:],thisEvent[3][3:])
 	       pl.xlabel('Time ($\mu$s)')
 	       pl.ylabel('Amplitude (V)')

 	     pl.grid(True)
             pl.suptitle('Board {0} Event {1}'.format(board[j],EvtId[j]))
	     
	     if TYPE == "C":  # Plotting calibrator signal in Calibration mode
 	       pl.plot(t[3:],thisEvent[3][3:],'s')
	       # Fit calibration signal with sine wave
  	       xr = t[3:]  #mus
 	       w = 2*np.pi*66.666666  #rad/mus
	       yr = thisEvent[3][3:]
	       fitfunc = lambda xr, a, b, c: a*np.sin(w*xr+b)+c   # Create fit function
	       abeg = float(np.max(yr)-np.min(yr))
	       p, pcov = curve_fit(fitfunc,xr,yr,p0 = [abeg,0.0,0.0])  #Perform fit
 	       print 'Fit results:',p,np.sqrt(np.diag(pcov))
	       xf=np.linspace(xr[0],xr[-1],10000)  # Display fit result wuith nice thinning
	       pl.plot(xf,fitfunc(xf,p[0],p[1],p[2]))
	     
	     pl.show()
	     raw_input()
 	     pl.close(j)
	   
	   # Assemble stat for summary plots
	   iimax = np.zeros(shape=(1,nch),dtype=int)
	   iAmax = np.zeros(shape=(1,nch),dtype=float)
   	   imub = np.zeros(shape=(1,nch))
  	   isigb = np.zeros(shape=(1,nch))	   
	   for k in range(nch):
	     iimax[0,k] = np.argmax(thisEvent[k][3:])+3;  # Skip 1st 3 points because could be left overs from previous events
	     iAmax[0,k] = thisEvent[k][iimax[0,k]];
	     imub[0,k] = np.mean(thisEvent[k][1:offset-5])
	     isigb[0,k] = np.std(thisEvent[k][1:offset-5])	
	   #print iimax[0]
	   imax.append(iimax[0])
	   Amax.append(iAmax[0])
	   mub.append(imub[0])
	   sigb.append(isigb[0])
	   j = j+1

   #except NameError:
   #  print "NameError"
 
   #except:
   #  print "Unknown error while reading data (end of file?) ==> abort reading."
    
   if TYPE == "P":
     return
   
   SSS = np.array(SSS)
   IP = np.array(IP)
   TS1Trig = np.array(TS1Trig)
   SSS = np.array(SSS)
   TS2 = np.array(TS2)
   TS1PPS = np.array(TS1PPS)
   EvtId = np.array(EvtId )
   TrigPattern = np.array(TrigPattern)
   board = np.array(board)
   imax = np.array(imax)
   Amax = np.array(Amax)
   mub = np.array(mub)
   sigb = np.array(sigb)
   board = np.array(board)

   nevts = np.size(SSS)
   print "Nb events=", nevts
   # Now display summary plots
   trigtime = np.zeros(shape=(np.size(SSS))) 
   
   timein = np.where(SSS>0)  
   if np.size(timein) > 0:  # GPS timing info is available
     tdeb = min(SSS[timein])
     tend = max(SSS)
   dur = tend-tdeb+1 # Run duration [seconds]
   t = range(dur)
   boards = set(board[np.where(board>0)])
   DataRate = np.zeros(shape=(dur,len(boards)))
   TrigRate = np.zeros(shape=(dur,len(boards)))
   
   print 'Run start:', date[0]
   print 'Boards in run:',list(boards)
   j = 0
   #for id in boards:  # Loop on all boards in run
   for id in [int(boardID)]:  # Loop on all boards in run
     sel = np.where(board == id)
     date_end = date[sel[0][-1]]
     print 'Run stop:',date_end,'for board',id,' (',np.size(sel),'measurements)'
     if np.size(timein) > 0:
       # To be implemented: read MaxCoarse info from slow control data and define correction factor accordingly cor = 125e6/MaxCoarse
       # See anaTiming.py line 133 and following for guidance
       cor = 1.0
     else:
       cor=1.0
     print 'Correction factor for 125MHz clock for board',id,':',cor
     # Build trig time
     trigtime[sel] = SSS[sel]+(TS2[sel]*4+TS1PPS[sel]-TS1Trig[sel])*2e-9*cor  #second. 
     
     # Compute trig rate
     for i in range(dur):
	ts = tdeb+i
	thisSec = np.where(SSS[sel]==ts)
	thisEvtId = EvtId[sel]
	if np.size(thisSec) > 0:
	  thisSec=thisSec[:][0]
	  DataRate[i,j] = np.size(thisSec)
	  TrigRate[i,j] = thisEvtId[thisSec[-1]]-thisEvtId[thisSec[0]]+1   #Nb of events rigged in that second --> trigrate
     
     pl.figure(2)
     pl.plot(t,TrigRate[:,j],label='Trig rate - Board '+str(id))     
     pl.plot(t,DataRate[:,j],label='Data rate - Board '+str(id))
     pl.grid(True)
     pl.xlabel('Run time (s)')
     pl.ylabel('Data rate (Hz)')
     pl.legend()
     pl.title('Data rate')    
     
     # Displays
     for k in range(nch):
      if 1:
       good = np.where( (imax[sel,k][0]>104) & (imax[sel,k][0]<108))
       abline = np.where( (Amax[sel,k][0]<0))
       azero = np.where( (Amax[sel,k][0]==0))
       print 'Channel',k,': good events=',np.size(good),'/',np.size(sel),'=',float(np.size(good))/np.size(sel)
       print 'Channel',k,': Max at zero=',np.size(azero),'/',np.size(sel),'=',float(np.size(azero))/np.size(sel)
       print 'Channel',k,': Max < zero=',np.size(abline),'/',np.size(sel),'=',float(np.size(abline))/np.size(sel)
       
       pl.figure(id*100+21+k)
       
       pl.subplot(231)
       pl.hist(mub[sel,k][0],offset*2)
       pl.xlabel('Baseline mean')
       pl.title('Board {0}'.format(id))
       pl.grid(True)

       pl.subplot(235)
       pl.plot(mub[sel,k][0],'+')
       pl.plot(Amax[sel,k][0],'o')
       pl.xlabel('Event ID')
       pl.ylabel('Mean amp (bline & max)')
       pl.title('Board {0}'.format(id))
       pl.grid(True)

       pl.subplot(234)
       pl.xlabel('Index of signal max')
       pl.hist(imax[sel,k][0],offset*2)
       pl.title('Board {0}'.format(id))
       pl.grid(True)
       
       pl.subplot(236)
       pl.xlabel('Max amplitude')
       pl.hist(Amax[sel,k][0],offset*2)
       pl.title('Board {0}'.format(id))
       pl.grid(True)
              
       pl.subplot(232)
       diffAmp = Amax[sel,k][0]-mub[sel,k][0]
       pl.hist(sigb[sel,k][0],offset*2)
       pl.xlabel('Bline std dev')
       pl.title('Board {0}'.format(id))
       pl.grid(True)
       
       print 'Channel',k,': bline @ ',np.mean((mub[sel,k][0])),'pm',np.std((mub[sel,k][0])),'V. Std dev=',np.mean((sigb[sel,k][0])),'V'
       print 'Channel',k,': Peak @ ',np.mean((Amax[sel,k][0])),'V, std dev=',np.std((Amax[sel,k][0])),'V, rel error=',np.std((Amax[sel,k][0]))/np.mean((Amax[sel,k][0]))*100,'%'
       print 'Channel',k,': Peak - bline @ ',np.mean((diffAmp)),'V, std dev=',np.std((diffAmp)),'V, rel error=',np.std((diffAmp))/np.mean((diffAmp))*100,'%'
       
       pl.subplot(233)
       pl.plot(mub[sel,k][0],sigb[sel,k][0],'+')
       pl.xlabel('Baseline mean')
       pl.ylabel('Bline std dev')
       pl.title('Board {0}'.format(id))
       pl.grid(True)
       
     j = j+1

   
   sel = np.where(trigtime>0)  #GPS time info present
   if np.size(sel)>0:
     first = trigtime[sel[0][0]] 
     last = trigtime[sel[0][-1]]
     dur = last-first
     print 'Nevents = ',np.size(sel)
     print 'Duration [s]',first,last,dur   
     rate = np.size(sel)/dur
     print 'Rate=',rate,'Hz'
     pl.figure(18)
     pl.plot(trigtime)
     pl.xlabel('Evt ID')
     pl.ylabel('Trig time [s]')
       
  
def get_1stone(val):
    if val == '0x1':
    	return 0
    if val == '0x3':
    	return 1
    if val == '0x7':
    	return 2
    if val == '0xf':
    	return 3
    if val == '0x1f':
    	return 4
    if val == '0x3f':
    	return 5
    if val == '0x7f':
    	return 6
    if val == '0xff':
    	return 7
    return 8	
	
	
    
def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val   
    
   

if __name__ == '__main__':
     if len(sys.argv)!=4:
       print "Usage: >loopEvents RUNID boardID TYPE"
     else:  
       loopEvents(sys.argv[1],sys.argv[2],sys.argv[3])
