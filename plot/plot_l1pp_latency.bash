#!/bin/bash
gnuplot -e "datafile='latency-points.dat';outputfile='~/Dropbox/l1pp-latency.pdf';titlename='l1pp'" ./gnuplot/l1pp-plot.gpi
