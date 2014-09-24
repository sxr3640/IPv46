import matplotlib.pyplot as plt 
import numpy as np
from analyzer import *
def plot_aadi():
	aadi_inter_num = [36468, 125618, 15515, 5407, 25085, 2635]
	x = []
	x = [0,1,2,3,4,5]                    
	plt.plot(x,aadi_inter_num,'r-')
	plt.show()
if __name__ == '__main__':
    plot_aadi()
