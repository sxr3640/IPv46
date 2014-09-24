from update_class import *
from netaddr import *
from env import *
import patricia
import os
from netaddr import *

class Window():

    def __init__(self,as_ym, maxsize):
        # Window parameters
        self.maxsize = maxsize
        self.as_ym = as_ym
        self.size = 0
        self.start = 0  # Window start
        self.end = 0  # Window end
        self.trie = patricia.trie(None)  # Store still active updates.

        self.as_path_trie = patricia.trie(None)

        # BGP dynamics count variables
        self.wadi = 0
        self.aadi = 0
        self.wwdu = 0
        self.aadut1 = 0
        self.aadut2 = 0
        self.wadu = 0
        self.aw = 0
        self.wa = 0
        self.aadi_inter_time = {}

    def pfx_to_binary(self, content):
        length = None
        pfx = content.split('/')[0]
        try:
            length = int(content.split('/')[1])
        except:
            pass
        addr = IPAddress(pfx).bits()
        if len(addr) < 40:
            addr = addr.replace('.', '')
            if length:
                addr = addr[:length]
            return addr
        else:
            addr = addr.replace(':', '')
            if length:
                addr = addr[:length]
            return addr

    def intial4_as_path(self,clctr):
        self.as_path_trie = patricia.trie(None)
        rib_location = hdname + 'archive.routeviews.org/' + clctr + '/bgpdata/' + self.as_ym + '/RIBS'
        print rib_location
        list = os.listdir(rib_location)
        for line in list:
            ribpath = os.path.join(rib_location,line)
        print ribpath
        ribfile = open(ribpath,'r')
        while 1:
            line = ribfile.readline()
            tmpline = line.split('|')
            if line:
                try:
                    addr = IPAddress(tmpline[3]).bits()
                    #print addr
                    if len(addr) <= 40:
                        from_ip = addr.replace(':','')
                        prefix = self.pfx_to_binary(tmpline[5])
                        key = prefix
                        try:
                            self.as_path_trie[key][from_ip] = tmpline[6]
                        except:
                            self.as_path_trie[key] = {}
                            self.as_path_trie[key][from_ip] = tmpline[6]

                except:
                    continue

            else:
                break
                #continue
        ribfile.close()

    def intial6_as_path(self,clctr):
        self.as_path_trie = patricia.trie(None)
        rib_location = hdname + 'archive.routeviews.org/' + clctr + '/bgpdata/' + self.as_ym + '/RIBS'
        print rib_location
        list = os.listdir(rib_location)
        for line in list:
            ribpath = os.path.join(rib_location,line)
        print ribpath
        ribfile = open(ribpath,'r')
        while 1:
            line = ribfile.readline()
            tmpline = line.split('|')
            #print tmpline
            if line:
                try:
                    addr = IPAddress(tmpline[3]).bits()
                    #print addr
                    if len(addr) >40:
                        from_ip = addr.replace(':','')
                        prefix = self.pfx_to_binary(tmpline[5])
                        key = prefix
                        try:
                            self.as_path_trie[key][from_ip] = tmpline[6]
                        except:
                            self.as_path_trie[key] = {}
                            self.as_path_trie[key][from_ip] = tmpline[6]
                except:
                    continue
            else:
                break
                #continue
        ribfile.close()        
        
    def add(self, update):
        if update.is_abnormal():
            print '!!!!!!!!!!!!'
            return 0
        utime = update.get_time()
        if self.start == 0:  # first run
            self.start = utime
            self.end = utime
            self.size = 1
        else:
            if self.end < utime:
                if self.size < self.maxsize:  # increase window
                    self.size += utime - self.end
                    self.end = utime
                    if self.size > self.maxsize:  # When utime - end > 1
                        self.start += self.size - self.maxsize
                        self.size = self.maxsize
                else:  # size alraedy maximum
                    self.start += utime - self.end
                    self.end = utime
            elif self.end > utime:
                print 'Wrong update time!'
            else:
                pass
        #print 'analyze update.......'
        self.analyze_update(update)

        return 0

    def analyze_update(self, update):		
        a_list = update.get_announce() 
        w_list = update.get_withdrawn()
        for upfx in a_list:
            try:
                update_list = self.trie[upfx]
            except:
                self.trie[upfx] = []
                self.trie[upfx].append(update)
                update_list = self.trie[upfx]
                continue

            change = False
            for ud in reversed(update_list): # Latest first
                if ud.get_time() < self.start:
                    update_list.remove(ud)
                    continue
                if upfx in ud.get_announce():
                    if ud.equal_to(update):
                        self.aadut1 += 1
                    else:
                        if ud.as_path == update.as_path and\
                            ud.next_hop == update.next_hop:
                            self.aadut2 += 1
                        else:
                            self.aadi += 1
                            try:
                                self.as_path_trie[upfx][update.from_ip] = update.as_path
                            except:
                                self.as_path_trie[upfx] ={}
                                self.as_path_trie[upfx][update.from_ip] = update.as_path
                            #inter_time = update.get_time() - ud.get_time()
                            #if self.aadi_inter_time.has_key(inter_time):
                            #    self.aadi_inter_time[inter_time] =self.aadi_inter_time[inter_time] + 1
                            #else:
                            #     self.aadi_inter_time[inter_time] = 1        
                    change = True
                    break
                elif upfx in ud.get_withdrawn():
                    try:
                        if self.as_path_trie[upfx][update.from_ip] == update.as_path:
                            self.wadu += 1
                        else:
                            self.wadi += 1
                            self.as_path_trie[upfx][update.from_ip] = update.as_path
                        change = True
                        break
                    except:
                        self.wa += 1
                        change = True
                        break
                        
                else:  # Normally, this will not happen.
                    #update_list.remove(ud)
                    continue


            if update not in update_list:  # Normally, this will be True.
                update_list.append(update)

            self.trie[upfx] = update_list

        for upfx in w_list:
            try:
                update_list = self.trie[upfx]
            except:
                self.trie[upfx] = []
                self.trie[upfx].append(update)
                update_list = self.trie[upfx]
                continue

            change = False
            for ud in reversed(update_list):
                if ud.get_time() < self.start:
                    update_list.remove(ud)
                    continue

                if upfx in ud.get_withdrawn():
                    self.wwdu += 1
                    change = True
                    break
                elif upfx in ud.get_announce():
                    self.aw += 1
                    change = True
                    break
                else:
                    #update_list.remove(ud)
                    continue

            if change:
                update_list.remove(ud)
            if update not in update_list:  # Normally, this will be True.
                update_list.append(update)

            self.trie[upfx] = update_list

        return 0

    def cut_trie(self):  # Delete updates that are out of current window.
        print 'trie size before cut = ', len(self.trie)
        for addr in sorted(self.trie):
            ulist = self.trie[addr]
            try:
                for update in ulist:
                    if update.get_time() < self.start:
                        ulist.remove(update)
                if ulist == []:
                    del self.trie[addr]
            except:  # root node has value None
                pass
        print 'trie size after cut = ', len(self.trie)
        return 0
