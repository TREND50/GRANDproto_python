from anaSLC import displaySLC
from anaSLC import loopSLCRuns
import pylab as pl

ants = ["05","06","09","10","11","18","27","31"]
pl.ion()

for ant in ants:
  #loopSLCRuns(ant,6350,6352)
  displaySLC(ant)
  raw_input()
  pl.close('all')
