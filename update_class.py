from datetime import datetime
from netaddr import *
import time

# We ignore: 1) an update announces and withdraws the same prefix
# 2) an update announces the same prefix twice

class Update():

    def __init__(self, string):
		self.time = 0
		self.next_hop = None
		self.announce = []
		self.withdrawn = []
		self.as_path = None
		self.communities = None
		self.origin = None
		self.protocol = None
		self.from_ip = None
		string = string.split('|')
		#print string[5]
		self.time = int(string[1])
		addr = IPAddress(string[3]).bits()
		if len(addr) >40:
			self.from_ip = addr.replace(':','')
			self.protocol = 6
		else:
			self.from_ip = addr.replace('.', '')
			self.protocol = 4
		if string[2] == 'A':
			self.announce.append(self.pfx_to_binary(string[5]))
			self.as_path = string[6]
			self.origin = string[7]
			self.next_hop = self.pfx_to_binary(string[8])
			self.communities = string[11]	
		elif string[2]=='W':
			self.withdrawn.append(self.pfx_to_binary(string[5]))
			



    def pfx_to_binary(self, content):
        length = None
        pfx = content.split('/')[0]
        try:
            length = int(content.split('/')[1])
        except:
            pass
        if self.protocol == 4:
            addr = IPAddress(pfx).bits()
            addr = addr.replace('.', '')
            if length:
                addr = addr[:length]
            return addr
        elif self.protocol == 6:
            addr = IPAddress(pfx).bits()
            addr = addr.replace(':', '')
            if length:
                addr = addr[:length]
            return addr
        else:
            print 'protocol false!'
            return 0

    def equal_to(self, u):# According to Jun Li, do not consider prefix
        # May be incomplete.
		if self.next_hop == u.next_hop and self.as_path == u.as_path and\
        	self.communities ==u.communities and self.origin == u.origin:
			return True
		else:
			return False

    def has_same_path(self, u):
		if self.as_path == u.as_path and self.next_hop == u.next_hop:
			return True
		else:
			return False

    def get_time(self):
        return self.time

    def get_from_ip(self):
        return self.from_ip

    def get_announce(self):
        return self.announce

    def get_withdrawn(self):
        return self.withdrawn

    def get_protocol(self):
        return self.protocol

    def is_abnormal(self):
        aset = set(self.announce)
        if len(aset) < len(self.announce):
            return True
        wset = set(self.withdrawn)
        if len(wset) < len(self.withdrawn):
            return True
        bset = aset.intersection(wset)
        if bset:
            return True

        return False

    def print_attr(self):
        print self.time
        print self.next_hop
        print self.announce
        print self.withdrawn
        print self.as_path
        print self.communities
        print self.origin
        print self.protocol
