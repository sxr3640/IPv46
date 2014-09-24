#!/usr/bin/env python
"""
Show how to use an rrule instance to make a custom date ticker - here
we put a tick mark on every 5th easter

See https://moin.conectiva.com.br/DateUtil for help with rrules
"""
import matplotlib.pyplot as plt
from matplotlib.dates import YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange
import numpy as np
import datetime

# tick every 5th easter
rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
loc = RRuleLocator(rule)
formatter = DateFormatter('%m/%y')
date1 = datetime.date( 2004, 10, 1)
date2 = datetime.date( 2006, 10, 1)
date3 = datetime.date( 2008, 10, 1)
date4 = datetime.date( 2010, 07, 1)
date5 = datetime.date( 2012, 07, 1)
date6 = datetime.date( 2014, 07, 1)
#delta = datetime.timedelta(days=365)
#dates = [date1, date2,date3,date4]#,date5,date6]
#y1 = [2.9,2.7,4.8,4.1]
dates = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []
file = open('/media/sxr/TOURO/update6_num','r')
for line in file:
    print line
    if line[0] =='2':
        print line,
        print line[5:7]
        print int(line[5:7])
        date = datetime.date(int(line[0:4]),int(line[5:7]),1)
        dates.append(date)
    if line[0:4] == 'wadi':
        tmp = line.split()[1][0:4]
        y1.append(tmp)
    if line[0:4] == 'aadi':
        tmp = line.split()[1][0:4]
        y2.append(tmp)
    if line[0:4] == 'wwdu':
        tmp = line.split()[1][0:4]
        y3.append(tmp)
    if line[0:6] == 'aadut1':
        tmp = line.split()[1][0:4]
        y4.append(tmp)
    if line[0:6] == 'aadut2':
        tmp = line.split()[1][0:4]
        y5.append(tmp)
    if line[0:4] == 'wadu':
        tmp = line.split()[1][0:4]
        y6.append(tmp)
    if line[0:2] == 'aw':
        tmp = line.split()[1][0:4]
        y7.append(tmp)
print dates
print y1
print y2
print y3
print y4
print y5
print y6
print y7

forward = []
policy = y5
dup = [] 
forandply = []
#s = np.random.rand(len(dates)) # make up some random y values
for x,y in zip(y1,y2):
    tmp = float(x) + float(y)
    forward.append(str(tmp))
print forward    

for x,y,z in zip(y1,y2,y5):
    tmp = float(x) + float(y) +float(z)
    forandply.append(str(tmp))
print forandply    

for x,y,z in zip(y3,y4,y7):
    tmp = float(x) + float(y) + float(z)
    dup.append(str(tmp))
print dup
fig, ax = plt.subplots()
#plt.plot_date(dates, y1,'r-',label="wadi")
#plt.plot_date(dates, y2,'b-',label="aadi")
plt.plot_date(dates, y3,'g-',label="wwdu")
plt.plot_date(dates, y4,'y-',label="aadut1")
#plt.plot_date(dates, y5,'o-',label="aadut2")
#plt.plot_date(dates, y6,'r-.',label='wadu')
plt.plot_date(dates, y7,'b-.',label='aw')

#plt.plot_date(dates, forandply,'o-',label="forandply")
#plt.plot_date(dates, forward,'o-',label="forward")
#plt.plot_date(dates, policy,'o-',label="policy")
plt.plot_date(dates, dup,'o-',label="dup")

ytext = plt.ylabel(u'(%)')
xtext = plt.xlabel(u'time(year)')
#ax.xaxis.set_major_locator(loc)
ax.xaxis.set_major_formatter(formatter)
plt.legend(framealpha=0.5)
#labels = ax.get_xticklabels()
#plt.setp(labels, rotation=30, fontsize=10)

plt.show()
