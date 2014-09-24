from env import *
import numpy as np
import matplotlib.pyplot as plt
import patricia
import subprocess
yearmonth = ['2006.10']#,'2006.10','2008.10','2010.07','2012.07','2014.07']
collector = ['route-views6']
#class Get_prefix_Num()
plt.figure(1, figsize=(16, 12))
#    def __int__(self,loc)
#        self.loc =loc
def get_prefix_num(loc):
    filelist = open(loc,'r')
    tmp_date = ''
    for flist in filelist:
        flist = flist.replace('\n','')
        print flist
        tmp = flist.split('.')
        subprocess.call('gunzip -c '+flist+' > ' + flist.replace('txt.gz', 'txt'), shell=True)
        if tmp[4] == tmp_date:
            f = open(flist.replace('txt.gz','txt'),'r')
            for line in f:
                try:
                    line = line.split('|')
                    #if line[2]=='A':
                    string = line[4] + '|' + line[5]  # prefix + AS
                    if AS_prefix.has_key(string):
                        AS_prefix[string] += 1
                    else:
                        AS_prefix[string] = 1
                except:
                    continue
                
        else:
            if tmp_date !='':
                plot_cdf(AS_prefix,tmp_date)
            tmp_date = tmp[4]       
            AS_prefix = {}
            f = open(flist.replace('txt.gz','txt'),'r')
            for line in f:
                try:
                    line = line.split('|')
                    #if line[2]=='A':
                    string = line[4] + '|' + line[5]
                    if AS_prefix.has_key(string):
                        AS_prefix[string] += 1
                    else:
                        AS_prefix[string] = 1
                except:
                    continue
    plot_cdf(AS_prefix,tmp_date)

def plot_cdf(dic,lab):
    dt = dic.keys()
    b =[]
    b_normal = []
    normal = []
    prefix_AS = {}
    all_num = 0
    for key in dt:
        b.append(dic[key])
    b.sort()
    for i in range(len(b)-1):
        if prefix_AS.has_key(b[i]):
            prefix_AS[b[i]] += 1
        else:
            prefix_AS[b[i]] =1

    for key in prefix_AS.keys():
        b_normal.append(prefix_AS[key])

    for i in xrange(1,len(b_normal)):
        b_normal[i] += b_normal[i-1]

    all_num =  b_normal[len(b_normal)-1]
    for i in range(len(b_normal)-1):
        normal.append(float(b_normal[i])/float(all_num))
    print len(normal)
    xlim = np.arange(1,len(normal)+1)
    plt.plot(xlim,normal,label=lab)
    plt.xlim(1,50) 
    #plt.show()                
if __name__ == '__main__':
    for ym in yearmonth:
        loc = '/media/sxr/TOURO/metadata/' + ym + '/updt_filelist_'
        get_prefix_num(loc)
        plt.legend(loc = 4)
        plt.show()   
