from analyzer import *
import os
import subprocess

yearmonth = ['2014.07']#,'2008.10']#,'2008.10','2010.07','2012.07','2014.07']
yearmonth1 = ['2014.06']#,'2008.09']
#yearmonth = ['2012.07','2014.07']
clctr= ['','route-views6','route-views.eqix']

for ym,as_ym in zip(yearmonth,yearmonth1):
    filelist = '/media/sxr/TOURO/metadata/' + ym + '/updt_filelist_'
    for collector in clctr:
        file_upt = open(filelist + collector,'r')
        for line in file_upt:
            if os.path.isfile(line.replace('.txt.gz\n','.txt')):
                continue
            else:
                print line
                #subprocess.call('gunzip -c '+line+' > \
                #'+line.replace('txt.gz', 'txt'), shell=True)
    #ana = Analyzer(filelist,as_ym,clctr, 45)
    #ana.parse_update(ym)
    #ana.plot_bgp_dynamic(ym)
