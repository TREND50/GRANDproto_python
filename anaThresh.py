import os
import time
import sys
import math

import numpy as np
import pylab as pl

print sys.argv
boardid = sys.argv[1]
TYPE = sys.argv[2]
folder = sys.argv[3]
dur = 10  #Duration of runs to be checked in testthreshn.py)

fname = 'thresh' + TYPE + '_b' + boardid + '.txt' 
fname = folder+'/'+fname
a = np.loadtxt(fname)
pat = a[:,0]
th = a[:,1]
nb = a[:,2]
if TYPE=='n':
  y = np.asarray(nb)/dur
if TYPE=='s':
  y = np.asarray(nb)/(dur*10*2)  #10Hz square 
pati = [1000,1,10000,10,100000,100]
ch=['X+','X-','Y+','Y-','Z+','Z-']
c = ['b','b','g','g','r','r']
lstyle=['-','--','-','--','-','--']

fig, ax = pl.subplots()
for i in range(np.size(pati)):
  sel = np.where(pat==pati[i])
  ax.plot(th[sel],y[sel],lstyle[i],color=c[i],marker='*',label=ch[i],linewidth=2)
  
if TYPE=='n':
  ax.set_title('Noise trigger - board {0}'.format(boardid))
  ax.set_ylabel('Trig rate (Hz)')
  #ax.set_yscale('log')
  rate = rate+0.
  ax.set_ylim([-0.1,np.max(y)*1.1])
if TYPE=='s':
  ax.set_title('Signal trigger - board {0}'.format(boardid))
  ax.set_ylabel('$N_{Trig}/N_{Signal}$')

ax.set_xlabel('Threshold (mV)')
pl.grid(True)
pl.legend(loc='best')
#pl.show()

if TYPE=='n':
  fig.savefig(folder+'/thresh_noise.png')
if TYPE=='s':
  fig.savefig(folder+'/thresh_signal.png')
