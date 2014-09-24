from env import *
import numpy as np
import matplotlib.pyplot as plt
import patricia
import subprocess
yearmonth = ['2004.10','2006.10','2008.10','2010.07','2012.07','2014.07']
collector = ['','route-views6']
#class Get_prefix_Num()
plt.figure(1, figsize=(16, 12))

#    def __int__(self,loc)
#        self.loc =loc
#ann_num = [0,0,0,0,0,0,0]
#i = 0
def get_announce_num(loc):
    filelist = open(loc,'r')
    tmp_date = ''
    ann_num = [0,0,0,0,0,0,0]
    i = 0

    for flist in filelist:
        flist = flist.replace('\n','')
        tmp = flist.split('.')
        subprocess.call('gunzip -c '+flist+' > ' + flist.replace('txt.gz', 'txt'), shell=True)
        if tmp[4] == tmp_date:
            f = open(flist.replace('txt.gz','txt'),'r')
            for line in f:
                try:
                    line = line.split('|')
                    if line[2]=='A':
                        ann_num[i] += 1
                except:
                    continue
                
        else:
            if tmp_date !='':
                i += 1
            tmp_date = tmp[4]
            f = open(flist.replace('txt.gz','txt'),'r')
            for line in f:
                try:
                    line = line.split('|')
                    if line[2]=='A':
                        ann_num[i] += 1
                except:
                    continue
    plot_cdf(ann_num,tmp_date[0:7])

def plot_cdf(lis,lab):
    plt.plot(lis,label = lab) 
    #plt.show()                
if __name__ == '__main__':
    for ym in yearmonth:
        
        loc = '/media/sxr/TOURO/metadata/' + ym + '/updt_filelist_route-views6'
        get_announce_num(loc)
    plt.legend(loc = 1)
    plt.show()   
