import os
import time
import sys
import re
import math
import numpy as np
import pylab as pl

def loopEvents(RUNID,att):
   ext = 0	 
   DISPLAY = 0
   print 'DISPLAY = ',DISPLAY 
   pl.ion()
   if ext:
     filename = "sinCh1b1_"+att1+"dB.txt"
   else:
     filename = "C"+RUNID+"_b01.data"
   #datafile = '/root/GRANDproto/data/'+filename
   datafile = '../data/'+filename
   print 'Scanning',datafile

   with open(datafile,"r") as f:
   	   evts = f.read().split('-----------------')

   nevts = len(evts)-1
   print 'Number of events:',nevts
   time.sleep(1)
   date = []
   board = np.zeros(shape=(np.size(evts)),dtype = np.int32)
   
   TS2 = np.zeros(shape=(np.size(evts)))
   TS1PPS = np.zeros(shape=(np.size(evts)))
   TS1Trig = np.zeros(shape=(np.size(evts)))
   SSS = np.zeros(shape=(np.size(evts)),dtype = np.int32)
   EvtId = np.zeros(shape=(np.size(evts)),dtype = np.int32)
   TrigPattern = np.zeros(shape=(np.size(evts)))
   imax = np.zeros(shape=(nevts,3),dtype=int)
   Amax = np.zeros(shape=(nevts,3))
   mub = np.zeros(shape=(nevts,3))
   sigb = np.zeros(shape=(nevts,3))
   
   #data = list()

   j = 0;  # Index of array filling (because date & data are "append")
   for i in range(1,nevts+1):  
   	   if float(i)/100 == int(i/100):
	   	print 'Event',i,'/',nevts
   	   evt = evts[i]
   	   evtsplit = evt.split('\n')
 
   	   if np.size(evtsplit)>8:   # Event is of normal size
   		   date.append(evtsplit[1])
		   IP = evtsplit[2][3:]
		   board[j] = int(IP[-2:]);
		   		
   		   TS2[j]=int(evtsplit[3][4:])  # time elapsed since last PPS (125MHz clock <=> 8ns counter)
   		   tt=int(evtsplit[4][11:])  # phase in 8ns slot fr trigger
   		   TS1Trig[i] = get_1stone(hex(tt))
		   tpps=int(evtsplit[5][7:]) 
		   TS1PPS[j]=get_1stone(hex(tpps))  # phase in 8ns slot for PPS
   		   SSS[j]=int(evtsplit[6][4:])  # Elapsed seconds since start
   		   EvtId[j] = int(evtsplit[7][3:])
   		   TrigPattern[j] = int(evtsplit[8][12:])
   		   # Data
   		   raw=evtsplit[9:][:]  #raw data
   		   raw2 = raw[0].split(" ") # Cut raw data list into samples
		   raw2 = raw2[0:np.size(raw2)-1]   # Remove last element (empty)
		   hraw2 = [hex(int(a)) for a in raw2]  # TRansfer back to hexadecimal
   		   draw = [twos_comp(int(a,16), 12) for a in hraw2] #2s complements		   
 		   draw = np.array(draw)*1./2048  # in Volts
   		   nsamples = len(draw)/4  # Separate data to each channel
   		   offset = nsamples/2.0
		   thisEvent = np.reshape(draw,(4,nsamples));
   		   #data.append(thisEvent) # Write to data list ... Not needed here
		   if DISPLAY:
		     print 'Event ',j, 'at date',date[j]
		     t = np.array(range(np.shape(thisEvent)[1]))
 		     t = t* 10e-3  #in mus
 		     pl.figure(j)
 		     pl.subplot(311)
 		     pl.plot(t[3:],thisEvent[0][3:])
 		     pl.ylabel('Amplitude [LSB]')
 		     pl.grid(True)
 		     pl.subplot(312)
 		     pl.ylabel('Amplitude [LSB]')
 		     pl.plot(t[3:],thisEvent[1][3:])
 		     pl.grid(True)
 		     pl.subplot(313)
 		     pl.plot(t[3:],thisEvent[2][3:])
 		     pl.xlabel('Time [mus]')
 		     pl.ylabel('Amplitude [LSB]')
		     
 		     pl.grid(True)
 		     pl.suptitle('Board {0} Event {1}'.format(board[j],EvtId[j]))
 		     pl.show()
 		     raw_input()
 		     pl.close(j)

		   
		   for k in [0,1,2]:
		     nz = np.where(thisEvent[k][:]!=0)
		     imax[j,k] = np.argmax(thisEvent[k][:]);
		     Amax[j,k] = thisEvent[k][imax[j,k]];
		     mub[j,k] = np.mean(thisEvent[k][nz])
		     sigb[j,k] = np.std(thisEvent[k][nz])
		   j = j+1
   	   else:
   		   print 'Error! Empty event',i

   boards = set(board[np.where(board>0)])
   print 'Boards in run:',list(boards)
   j = 0
   m = np.empty([len(boards),3])
   em = np.empty([len(boards),3])
   for id in boards:
     sel = np.where(board == id)     
     for k in [0, 1, 2]:      
       pl.figure(1)
       subpl = 311+k
       pl.subplot(subpl)
       a = mub[sel,k][0]
       pl.hist(a,100)
       if k == 0:
         pl.title('Board {0}'.format(id))

       if k == 2:
       	 pl.xlabel('Mean amplitude')
       pl.grid(True)
       pl.figure(2)
       subpl = 311+k
       pl.subplot(subpl)
       b = sigb[sel,k][0]
       pl.hist(b,100)
       if k == 0:
         pl.title('Board {0}'.format(id))
       if k == 2:
       	 pl.xlabel('Std dev')
       pl.grid(True)
                     
       #Pack up results
       m[j,k] = np.mean(a)
       em[j,k] = np.mean(b)       
       print 'Channel',k,': mean=',m[j,k],'; stddev=',em[j,k]

     j = j+1

    
   return {'m':m, 'em':em}
     

def anaRuns(runstart,runstop):   # Analyse runs and write result to file
  runs=range(runstart,runstop)  
  
  att = np.zeros(np.shape(runs))
  mm = np.empty([len(runs),3])
  emm = np.empty([len(runs),3])

  for i in range(np.size(runs)):  #loop on runs
    runid = runs[i]
    # Grab attenuation values from config file
    file = open("../data/C"+str(runid)+"_b01.cfg", "r")
    #file = open("/root/GRANDproto/data/C"+str(runid)+"_b18.cfg", "r")
    for line in file:
      if re.search("Attr1", line):
    	 att1 = int(line.split()[2])
      if re.search("Attr2", line):
    	 att2 = int(line.split()[2])
    att[i] = att1+att2
    print att1,att2,att[i]
    print att
    
    res = loopEvents(str(runid),str(att[i]))      
    mm[i,:]=list(res['m'][0])
    emm[i,:]=list(res['em'][0])

  # Write to file
  conc = np.r_[att,mm[:,0],emm[:,0],mm[:,1],emm[:,1],mm[:,2],emm[:,2]]   # Concatenate results
  conc = conc.reshape(7,np.size(att)) # Reshape in line = Att, Measure_Ch[i], Error_Ch[i]
  filename = 'caliboutput_R{0}R{1}.txt'.format(runstart,runstop)
  np.savetxt(filename,conc)  # Write to file

    
def anaRes(runstart,runstop):    
    
  # Read file
  a = np.loadtxt('caliboutput_R{0}R{1}.txt'.format(runstart,runstop))
  att = a[0,:]
  mm = np.empty([len(att),3])
  emm = np.empty([len(att),3])
  for k in range(3):
    mm[:,k] = a[2*k+1,:]
    emm[:,k] = a[2*k+2,:]
  
  
  sel = np.where((att>100) & (att<200))  #Fit range
  a = 0.25
  b = -5.8-a*127*2
  #if ext == 0:
  #  att = att*2 # Same coef on both channels
  attdB = a*att+b
  p = 1e-3*pow(10,attdB/10)
  R= 50 #To be confirmed!!!
  v = np.sqrt(p*R)
 
  
  fig = pl.figure(11)
  for k in range(3):
    pl.subplot(2,1,1)
    pl.plot(att,mm[:,k],'+',label='Channel {0}'.format(k))
    #z = np.polyfit(att[sel],mm[sel,k][0],1)  # Linear fit
    #print 'Channel',k,', slope=',z[0],'LSB/dB Att coef'
    #yth = att*z[0]+z[1]
    #pl.plot(att,yth,'y--')
    pl.subplot(2,1,2)
    pl.plot(att,emm[:,k],'+',label='Channel {0}'.format(k))
  pl.subplot(2,1,1)
  pl.grid(True)
  pl.xlabel('Attenuation coef [dB]')
  pl.ylabel('Mean output level [LSB]')
  pl.legend(loc='upper left')
  pl.subplot(2,1,2)
  pl.grid(True)
  pl.xlabel('Attenuation coef [dB]')
  pl.ylabel('StdDev [LSB]')
  pl.legend(loc='lower left')
  
 
  fig = pl.figure(12)
  for k in range(3):
    z = np.polyfit(attdB[sel],mm[sel,k][0],1)  # Linear fit
    yth = attdB*z[0]+z[1]
    pl.subplot(2,1,1)
    pl.errorbar(attdB,mm[:,k],yerr=emm[:,k],label='Channel {0}'.format(k))
    pl.plot(attdB,yth,'y--')
    print 'Channel',k,', slope=',z[0],'V/dBm'
    pl.subplot(2,1,2)
    pl.errorbar(v,mm[:,k],yerr=emm[:,k],label='Channel {0}'.format(k))
  pl.subplot(2,1,1)
  pl.grid(True)
  pl.xlabel('Input power [dBm]')
  pl.ylabel('Mean output level [V]')
  pl.legend(loc='upper left')
  sbp2 = pl.subplot(2,1,2)
  sbp2.set_xscale('log')
  pl.grid(True)
  pl.xlabel('Input amplitude [V]')
  pl.ylabel('Mean output level [V]')
  pl.legend(loc='upper left')
  
  
   
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
  
  #runs=range(9198,9366) # board 2
  #runs=range(9380,9548)  # board 1
  runs=range(500,627)  # board 1
  #anaRuns(runs[0],runs[-1])
  anaRes(runs[0],runs[-1])

