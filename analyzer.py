from netaddr import *
from env import *
import os
import subprocess
from datetime import datetime
import time 
from update_class import *
from window_class import *
import cmlib
from env import *
import matplotlib.pyplot as plt 
import numpy as np
from IPy import IP

class Analyzer():

    def __init__(self, filelist,as_ym, clctr, win_maxsize):
        self.filelist = filelist# filelist file name 
        self.collector = clctr
        #self.as_ym = as_ym
        self.as_list = []# Interesting BGP peer AS
        self.win4 = Window(as_ym,win_maxsize)# Initialize a window object
        self.win6 = Window(as_ym,win_maxsize)# Initialize a window object

    def parse_update(self,yearmonth):
        
        IP_num = 0
        IPv6_num = 0
        IPv4_num = 0
        A_num = 0
        W_num = 0
        A_IPv6_num = 0
        W_IPv6_num = 0
        A_IPv4_num = 0
        W_IPv4_num = 0

        for clctr in self.collector:
            self.win4.intial4_as_path(clctr)
            self.win6.intial6_as_path(clctr)
            self.win4.start = 0
            self.win6.start = 0
            self.win4.trie = patricia.trie(None)
            self.win6.trie = patricia.trie(None)
            filelist = open(self.filelist + clctr , 'r')
            for flist in filelist.readlines():
                flist = flist.replace('\n', '')
                print flist
                self.win4.cut_trie()
                self.win6.cut_trie()
                f = open(flist.replace('txt.gz', 'txt'), 'r')
                #for line in f.readlines():
                while 1:
                    line = f.readline()
                    if line:
                        try:
                            line = line.replace('\n','')
                            tmp = line.split('|')
                            #statistics announcement and withdrawal
                            IP_num = IP_num + 1
                            #print IP_num
                            if IP(tmp[3]).version() == 6:
                                IPv6_num = IPv6_num + 1
                                if tmp[2] =='A':
                                    A_num = A_num + 1
                                    A_IPv6_num = A_IPv6_num + 1
                                elif tmp[2] == 'W':
                                    W_num = W_num + 1
                                    W_IPv6_num = W_IPv6_num + 1                       
                            elif IP(tmp[3]).version() == 4:
                                IPv4_num = IPv4_num + 1
                                if tmp[2] =='A':
                                    A_num = A_num + 1
                                    A_IPv4_num = A_IPv4_num + 1
                                elif tmp[2] == 'W':
                                    W_num = W_num + 1
                                    W_IPv4_num = W_IPv4_num + 1

                            #process update,analyzer every attribute 
                            updt = Update(line.replace('\n',''))
                            #print 'from_control1'
                            from_control = updt.get_protocol()
                            #print from_control
                            if from_control == 4:
                                self.win4.add(updt)
                            elif from_control == 6:
                                self.win6.add(updt)
                        except:
                            print line
                            continue
                f.close()
                #os.remove(flist.replace('txt.gz', 'txt'))

            filelist.close()
            del self.win4.as_path_trie
            del self.win6.as_path_trie
        file_ip_num = open(hdname + 'IP_num','a')
        file_ip_num.write(yearmonth + '\n')
        file_ip_num.write('IP_num    IPv6_num   IPv4_num   A_num   W_num    '+\
        'A_IPv6_num   W_IPv6_num   A_IPv4_num   W_IPv4_num' + '\n' )
        file_ip_num.write(str(IP_num) + '  '+ str(IPv6_num) + '  ' + str(IPv4_num) +\
         '  ' + str(A_num) + '  ' + str(W_num) + '  ' + str(A_IPv6_num) + '  ' +\
         str(W_IPv6_num) + '  ' + str(A_IPv4_num) + '  ' + str(W_IPv4_num) + '\n')
        
        return 0

    
    def get_aadi_num(self):
        dt = self.win6.aadi_inter_time.keys()
        dt.sort()
        aadi_inter_num = [0,0,0,0,0,0]
        for key in dt:
            if key<1:
                aadi_inter_num[0] += self.win6.aadi_inter_time[key]
            elif key<30 and key>=1:
                aadi_inter_num[1] += self.win6.aadi_inter_time[key]
            elif key<60 and key>=30:
                aadi_inter_num[2] += self.win6.aadi_inter_time[key]
            elif key<120 and key>=60:
                aadi_inter_num[3] += self.win6.aadi_inter_time[key]
            elif key<240 and key>=120:
                aadi_inter_num[4] += self.win6.aadi_inter_time[key]
            elif key>=240:
                aadi_inter_num[5] += self.win6.aadi_inter_time[key]                     
    def plot_update_count(self):
        import matplotlib.pyplot as plt 
        import matplotlib.dates as mpldates
        from matplotlib.dates import HourLocator
        import numpy as np

        dt = self.update_count.keys()
        dt.sort()
        update4_count = []
        update6_count = []

        for key in dt:
            update4_count.append(self.update_count[key][0])
            update6_count.append(self.update_count[key][1])

        left = 0.05
        width = 0.92
        bottom = 0.15
        height = 0.8
        rect_scatter = [left, bottom, width, height]

        plt.figure(1, figsize=(16, 12))

        axScatter = plt.axes(rect_scatter)
        axScatter.plot(dt, update4_count, 'r-')
        axScatter.plot(dt, update6_count, 'b-')

        axScatter.set_xlabel('Datetime')
        myFmt = mpldates.DateFormatter('%m-%d %H%M')
        axScatter.xaxis.set_major_formatter(myFmt)

        axScatter.set_ylabel('Number of updates')
        axScatter.set_yscale('log')

        plt.show()
        return 0

    def plot_bgp_dynamic(self,yearmonth):
        all4 = self.win4.wadi + self.win4.aadi + self.win4.wwdu + self.win4.aadut1 + \
        self.win4.aadut2 + self.win4.wadu + self.win4.aw  + self.win4.wa
        try:
            file4 =open(hdname + '/update4_num','a')
            file4.write(yearmonth + '\n' )
            print self.win4.wadi, ':', float(self.win4.wadi)/float(all4) * 100, '%'
            print self.win4.aadi, ':', float(self.win4.aadi)/float(all4) * 100, '%'
            print self.win4.wwdu, ':', float(self.win4.wwdu)/float(all4) * 100, '%'
            print self.win4.aadut1, ':', float(self.win4.aadut1)/float(all4) * 100, '%'
            print self.win4.aadut2, ':', float(self.win4.aadut2)/float(all4) * 100, '%'
            print self.win4.wadu, ':', float(self.win4.wadu)/float(all4) * 100, '%'
            print self.win4.aw, ':', float(self.win4.aw)/float(all4) * 100, '%'
            print self.win4.wa, ':', float(self.win4.wa)/float(all4) * 100, '%'
            file4.write('wadi:' + str(self.win4.wadi) + '  ' + str(float(self.win4.wadi)/float(all4) * 100) + '%' + '\n')
            file4.write('aadi:' + str(self.win4.aadi) + '  ' + str(float(self.win4.aadi)/float(all4) * 100) + '%' + '\n')
            file4.write('wwdu:' + str(self.win4.wwdu) + '  ' + str(float(self.win4.wwdu)/float(all4) * 100) + '%' + '\n')
            file4.write('aadut1:' + str(self.win4.aadut1) + '  ' + str(float(self.win4.aadut1)/float(all4) * 100) + '%' + '\n')
            file4.write('aadut2:' + str(self.win4.aadut2) + '  ' + str(float(self.win4.aadut2)/float(all4) * 100) + '%' + '\n')
            file4.write('wadu:' + str(self.win4.wadu) + '  ' + str(float(self.win4.wadu)/float(all4) * 100) + '%' + '\n')
            file4.write('aw:' + str(self.win4.aw) + '  ' + str(float(self.win4.aw)/float(all4) * 100) + '%' + '\n')
            file4.write('wa:' + str(self.win4.wa) + '  ' + str(float(self.win4.wa)/float(all4) * 100) + '%' + '\n')
            file4.close()
        except:
            print 'No IPv4 address'
        all6 = self.win6.wadi + self.win6.aadi + self.win6.wwdu +\
        self.win6.aadut1 + self.win6.aadut2 + self.win6.wadu + self.win6.aw + self.win6.wa
        try:
            file6 = open(hdname + '/update6_num','a')
            file6.write(yearmonth + '\n' )
            print self.win6.wadi, ':', float(self.win6.wadi)/float(all6) * 100, '%'
            print self.win6.aadi, ':', float(self.win6.aadi)/float(all6) * 100, '%'
            print self.win6.wwdu, ':', float(self.win6.wwdu)/float(all6) * 100, '%'
            print self.win6.aadut1, ':', float(self.win6.aadut1)/float(all6) * 100, '%'
            print self.win6.aadut2, ':', float(self.win6.aadut2)/float(all6) * 100, '%'
            print self.win6.wadu, ':', float(self.win6.wadu)/float(all6) * 100, '%'
            print self.win6.aw, ':', float(self.win6.aw)/float(all6) * 100, '%'
            print self.win6.wa, ':', float(self.win6.wa)/float(all6) * 100, '%'
            file6.write('wadi:' + str(self.win6.wadi) + '  ' + str(float(self.win6.wadi)/float(all6) * 100) + '%' + '\n')
            file6.write('aadi:' + str(self.win6.aadi) + '  ' + str(float(self.win6.aadi)/float(all6) * 100) + '%' + '\n')
            file6.write('wwdu:' + str(self.win6.wwdu) + '  ' + str(float(self.win6.wwdu)/float(all6) * 100) + '%' + '\n')
            file6.write('aadut1:' + str(self.win6.aadut1) + '  ' + str(float(self.win6.aadut1)/float(all6) * 100) + '%' + '\n')
            file6.write('aadut2:' + str(self.win6.aadut2) + '  ' + str(float(self.win6.aadut2)/float(all6) * 100) + '%' + '\n')
            file6.write('wadu:' + str(self.win6.wadu) + '  ' + str(float(self.win6.wadu)/float(all6) * 100) + '%' + '\n')
            file6.write('aw:' + str(self.win6.aw) + '  ' + str(float(self.win6.aw)/float(all6) * 100) + '%' + '\n')
            file6.write('wa:' + str(self.win6.wa) + '  ' + str(float(self.win6.wa)/float(all6) * 100) + '%' + '\n')
            file6.close()
        except:
            print 'No IPv6 address'
