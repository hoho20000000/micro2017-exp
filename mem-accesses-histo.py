#!/bin/env python
import matplotlib as mpl
import math
import os
import scipy.stats as stats
import sys, getopt
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from numpy.random import normal, uniform
import numpy as np
import matplotlib.mlab as mlab
from scipy.interpolate import interp1d
from scipy.interpolate import spline
import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter
def to_percent(y, position):
        s = str(100 * y)
        s = s[:-2]
        if mpl.rcParams['text.usetex'] is True:
         return s + r'$\%$'
        else:
         return s + '%'
#from scipy.signal import savgol_filter
#from scipy.signal import savgol_filter

def main(argv):
  inputfile=''
  outputfile = ''
  try:
  	opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="]);
  except getopt.GetoptError:
  	print '-i <inputfile> -o <outputfile>'
  	sys.exit(2)
  for opt, arg in opts:
  	if opt == '-h':
  		print '-i file -o file'
  		sys.exit()
  	elif opt in ("-i", "--ifile"):
  		inputfile = arg
  	elif opt in ("-o", "--ofile"):
  		outputfile = arg
  
  addresses = []
  print inputfile
  #read the latencies from file
  for line in open(inputfile):
    #print line
    addresses.append(int(line.split(" ")[1], 16))
  
  # the histogram of the data
  weights = np.ones_like(addresses)/float(len(addresses))
  minaddr = min(addresses)
  maxaddr = max(addresses)
  print 'max address %s, min addre is%s'% (maxaddr, minaddr)
  n, bins, patches = plt.hist(addresses, bins=200, normed=0, weights=weights, facecolor='red', alpha=0.75);
  #n, bins, patches = plt.hist(interarrivals, 100, facecolor='green', alpha=0.75)
  
  #mu = np.mean(interarrivals);
  #sigma = np.std(interarrivals);
  
  #y = mlab.normpdf( bins, mu, sigma);
  #l = plt.plot(bins, y, 'r--', linewidth=1);

  ##calculate Measurement of Sparse
  plt.xlabel('Memory Addresses', fontsize=18);
  plt.ylabel('Counts', fontsize=18);
  #plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
  #plt.axis([40, 160, 0, 0.03])
  plt.grid(True);
  #solve y lavel cut off issuse
  plt.gcf().subplots_adjust(left=0.2, bottom=0.2, right=None, top=None, wspace=None, hspace=None)
  plt.gcf().set_size_inches(15,5);
  	
  axes = plt.gca();
  #axes.get_xaxis().set_tick_params( direction='out');
  plt.legend()
  ##plt.minorticks_on();
  ##plt.yticks(np.arange(0,0.7,0.1));
  #plt.yticks(fontsize = 18);
  #fig = plt.figure()
  #fig.savefig('test.pdf')
  plt.plot()
  #fmt = '%.0f%%'
  formatter = FuncFormatter(to_percent)
  #ytickformat=mtick.FormatStrFormatter(formatter)
  axes.yaxis.set_major_formatter(formatter)
  ##axes.set_xlim([0,5000])
  #axes.set_ylim([0,0.6])
  #plt.legend(loc='best')
  pdf = PdfPages(outputfile+".pdf");
  pdf.savefig()
  #plt.savefig('latency_distributions.png')
  plt.close()
  pdf.close()

if __name__ == "__main__":
	main(sys.argv[1:]);
