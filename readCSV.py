import numpy as np
import csv
import sys
import pylab as pl
import sys
import os
import ephem
import datetime
sys.path.append("/home/martineau/GRAND/soft/TREND_python/")
from readPSD import readPSDData
pl.style.use("/home/martineau/GRAND/soft/neutrinos/retro-ccin2p3/deps/mplstyle-l3/style/l3.mplstyle")
pl.ion()
fmax = 500
step = 20
# Balikun -- Obsolete   
#folder='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Bailikun/Apr2018/'
#files=['LOAD.CSV','TEST1.CSV','TEST2.CSV']  # Day1
#files=['LOAD.CSV','TIAN2.CSV','TIAN3.CSV','TIAN4.CSV','TIAN5.CSV']  # Day 2
#files=['LOAD.CSV','HU1.CSV','HU2.CSV','HU3.CSV','HU42.CSV','ROAD.CSV'] # Day 3
#files=['LOAD.CSV','ROAD2.CSV','ROAD3.CSV','ROAD4.CSV','ROAD5.CSV','TIAN32.CSV','TIAN12.CSV'] # Day 4
#files=['LOAD.CSV','TIAN3.CSV','TIAN32.CSV','TIAN12.CSV'] # Day 4
#files=['LOAD.CSV','TIAN12.CSV','TIAN2.CSV','TIAN32.CSV','TIAN4.CSV','TIAN5.CSV']  # TianLai
#labels=['load','R3142','R3123','R3141','R3126-7','R3128']
#files=['LOAD.CSV','HU1.CSV','HU2.CSV','HU3.CSV','HU42.CSV'] # Valley
#labels=['load','R3130','R3131','R3132','R3133']
#files=['LOAD.CSV','TEST1.CSV','TEST2.CSV','ROAD.CSV','ROAD2.CSV','ROAD3.CSV','ROAD4.CSV','ROAD5.CSV'] # Road
#labels=['load','R3110','R3111','R3134','R3140','R3143','R144-5','R3146']

# First list all measuremnts
allGansu = dict()
# Aug 31st / zone 2
folderAug31='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Gansu/August/Aug31/'
allGansu.update({'0':'GP300-200EW-a.CSV'})
allGansu.update({'1':'GP300-200NS-a.CSV'})
allGansu.update({'2':'GP300-EW-b.CSV'})
allGansu.update({'3':'GP300-NS-b.CSV'})
allGansu.update({'4':'GP300-EW-c.CSV'})
allGansu.update({'5':'GP300-NS-c.CSV'})
# Sep 1st / Zone 2
folderSep01='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Gansu/August/Sep01/'
allGansu.update({'6':'GP300-EW-c2.CSV'})
allGansu.update({'7':'GP300-NS-c2.CSV'})
allGansu.update({'8':'GP300-EW-e.CSV'})
allGansu.update({'9':'GP300-NS-e.CSV'})
allGansu.update({'10':'GP300-EW-f.CSV'})
allGansu.update({'11':'GP300-NS-f.CSV'})
allGansu.update({'12':'GP35-EW-f.CSV'})
allGansu.update({'13':'GP35-NS-f.CSV'})
allGansu.update({'14':'GP300-EW-g.CSV'})
allGansu.update({'15':'GP300-NS-g.CSV'})
# Sep 2nd / Zone 3
folderSep02='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Gansu/August/Sep02/'
allGansu.update({'16':'GP300-EW-a.CSV'})
#allGansu.update({'17':'GP300-EW-a2.CSV'})
allGansu.update({'18':'GP300-NS-a.CSV'})
allGansu.update({'19':'GP300-VERT-a.CSV'})
allGansu.update({'20':'GP300-EW-b.CSV'})
allGansu.update({'21':'GP300-NS-b.CSV'})
allGansu.update({'22':'GP300H-X-c.CSV'})
allGansu.update({'23':'GP300H-Y-c.CSV'})
allGansu.update({'24':'GP300-VERT-c.CSV'})
# Sep 3rd / Zone 1
folderSep03='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Gansu/August/Sep03/'
allGansu.update({'25':'GP300-EW-a.CSV'})
allGansu.update({'26':'GP300-NS-a.CSV'})
allGansu.update({'27':'GP300-EW-b.CSV'})
allGansu.update({'28':'GP300-NS-b.CSV'})
allGansu.update({'29':'GP300-VERT-b.CSV'})
allGansu.update({'30':'GP300-EW-c.CSV'})
allGansu.update({'31':'GP300-NS-c.CSV'})
allGansu.update({'32':'GP300-VERT-c.CSV'})
allGansu.update({'33':'GP300-EW-d.CSV'})
allGansu.update({'34':'GP300-NS-d.CSV'})
allGansu.update({'35':'GP300-VERT-d.CSV'})
allGansu.update({'36':'GP35-200EW-a.CSV'})
allGansu.update({'37':'GP35-200NS-a.CSV'})
#
# Dec 01 / Zone 2b
folderDec01='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Gansu/December/Dec01/'
allGansu.update({'38':'G2h-EW.CSV'})
allGansu.update({'39':'G2h-NS.CSV'})
allGansu.update({'40':'G2i-EW.CSV'})
allGansu.update({'41':'G2i-NS.CSV'})

# Dec 02 / QinHai Zone 1
folderDec02='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Gansu/December/Dec02/'
allGansu.update({'42':'Q1-EW.CSV'})
allGansu.update({'43':'Q1-NS.CSV'})

# Dec 02&03 / QinHai Zone 2
folderDec03='/home/martineau/GRAND/GRANDproto300/SiteSurvey/Gansu/December/Dec03/'
allGansu.update({'44':'Q2a-EW.CSV'})
allGansu.update({'45':'Q2a-NS.CSV'})
allGansu.update({'46':'Q2b-EW.CSV'})
allGansu.update({'47':'Q2b-NS.CSV'})
allGansu.update({'48':'Q2c-EW.CSV'})
allGansu.update({'49':'Q2c-NS.CSV'})
allGansu.update({'50':'Q2d-EW.CSV'})  # Bad nut
allGansu.update({'51':'Q2d-NS.CSV'})  # Bad nut
allGansu.update({'52':'GP300-EW-e.CSV'})  # Bad nut 
allGansu.update({'53':'GP300-NS-e.CSV'})  # Bad nut
allGansu.update({'54':'Q2e-EW.CSV'})  # Good nut
allGansu.update({'55':'Q2e-NS.CSV'})
allGansu.update({'56':'Q2f-EW.CSV'})
allGansu.update({'57':'Q2f-NS.CSV'})


#sel = np.arange(38,47)
sel = [44,46,48,56]  #  Only EW
sel = [44,46,48,56]  # QinHai Only EW
#sel = [45,47,49,55,57]  # Only NS
#sel = [52]
#labs=["GP35 NS"]

#sel = [4,40]
#labs=["Best Zone 2, August","Best Zone 2b, December (*:-3dB)"]

#labs=["Zone 1","Zone 2","Zone 3","Zone 1"]
#sel = [33,4,16]  # Best for each zone

j = 0
for i in sel:
  try:
    filename = allGansu[str(i)]
  except:
    print 'No entry for key {0}'.format(i)
    continue
  if i<6:
    folder=folderAug31
  if i>5 and i<16:  
    folder=folderSep01
  if i>15 and i<25:  
    folder=folderSep02
  if i>24 and i<38:
    folder=folderSep03  
  if i>37 and i<42:
    folder=folderDec01
  if i>41 and i<44:
    folder=folderDec02
  if i>43 and i<59:
    folder=folderDec03

  lab=filename[:-4]
  filename=folder+filename
  #print f[]
  
  def getData(filename):
    print 'Reading',filename
    fi = open(filename, 'rb')
    data = fi.read()
    fi.close()
    fo = open('temp.csv', 'wb')
    fo.write(data.replace('\x00', ''))  # Get rid of <nul> characters
    fo.close()
    fo = open('temp.csv', 'rb')  #re-open in read mode
    reader = csv.reader(fo)
  
    # Now loop on file
    ind = 0
    f = []
    power = []
    try:
      for row in reader:
        row = np.asarray(row)
        ind += 1
        if len(row)>4 and row[3]=='RBW':  # Grabing RBW value from CSV header
          rbw = float(row[4])
        if ind>16:  
  	  #print 'Row read successfully!', row[0], row[1]
  	  f.append(float(row[0]))
  	  power.append(float(row[1]))
 
    except csv.Error, e:
      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    f = np.asarray(f)
    power = np.asarray(power)
    psd = power-10*np.log10(rbw)  # As PSD = Power/DeltaF
    return f,psd

  # Combine EW+NS
  if 0:
    f,psdew=getData(filename)
    filename = allGansu[str(i+1)]
    filename=folder+filename
    _,psdns=getData(filename)
    if i==56:
      psdns=psdns[2:-1]
    psd = (psdew+psdns)/2
    lab = lab[:-3]
  else:
    f,psd=getData(filename)
  
  f = f/1e6
  if i == 0:
    sel = np.where((f>55) & (f<95))
    meanLoadGP = np.mean(psd[sel])
  if i>39:
    psd = psd-3
  pl.figure(1)
  #pl.subplot(221+i)
  pl.plot(f,psd,'-',lw=2,label=lab)
  #pl.plot(f,psd,'-',lw=2,label=labs[j])
  pl.xticks(np.arange(0, fmax+step,step))
  pl.grid(True)
  pl.xlabel('Frequency (MHz)')
  pl.ylabel('PSD (dBm/Hz)')
  #pl.ylabel('Power(dBm)')
  pl.legend(loc='best')  
  pl.xlim(0,fmax)
  pl.xlim(0,250)
  j = j+1
pl.show()
#raw_input()

if 0:
 ## Now plot TREND results
 ulastai = ephem.Observer();
 ulastai.long = ephem.degrees("86.71")
 ulastai.lat = ephem.degrees("42.95")
 ulastai.elevation = 2650;
 for i in range(38):
  antid = 101+i
  resLoad = readPSDData(2667,antid,0)
  f=resLoad['f']
  sel = np.where((f>0) & (f<100e6))
  fl = f[sel]/1e6
  psdl = resLoad['PSD']
  psdldb = psdl[sel,1][0]; # Use 1st PSD measurement # Warning psd[sel,1] is [[]]...
  sel = np.where((fl>60) & (fl<90))
  offset =  meanLoadGP - np.mean(psdldb[sel])
  psdldb = psdldb+offset
  resAnt = readPSDData(2676,antid,0)
  ut0 = resAnt['ut0'];
  date=datetime.datetime.utcfromtimestamp(int(ut0)).strftime('%Y/%m/%d %H:%M:%S')
  ulastai.date = ephem.Date(date)
  lst_run = ulastai.sidereal_time()
  print 'Antenna ',antid, ', LST at run start: ',lst_run
  fant=resAnt['f']
  sel = np.where((fant>0) & (fant<100e6))
  fant = fant[sel]/1e6
  psdant = resAnt['PSD']
  psdantdb = psdant[sel,1][0]; # Use 1st PSD measurement # Warning psd[sel,1] is [[]]...
  psdantdb= psdantdb+offset
  sel = np.where((fant>51) & (fant<90))
  if (np.max(psdantdb[sel])-meanLoadGP>10) or (np.min(psdantdb[sel])-meanLoadGP<0):
    continue  
  #pl.plot(fl,psdldb,'--',label='Load TREND')
  #pl.plot(fant[sel],psdantdb[sel],'--',label='Ant TREND')

#pl.ylim([-120,-30])
#pl.plot([50,100],[-74.5,-74.5],'--',lw=6,color='gray',label='Ulastai min')


pl.legend(loc='best')  
pl.show()
raw_input()
   
