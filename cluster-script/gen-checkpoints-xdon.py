#!/usr/bin/python

#
# A Python script to run all CC-NUMA multi-core experiments for PARSEC 2.1 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os
import multiprocessing as mp
import sys,getopt
import time


ckp_tick_512 = '4881191223250'
ckp_tick_2048 = '5046198013500'
ckp_tick_3072 =5160523235750
mem_size='3GB'
wd0=''
wd1=''
wd2=''
tasks = []
def run(bench, input_set, loop_index):
    dir =  '/home/fan/gem5-out-disk/mtrace-micro2017/'+ bench + '/' + input_set\
           + "/ckpts"
    #take checkpoint every half second
    ckpt_ticks=ckp_tick_3072+500000000000*loop_index
    ckpt_ticks_next=ckpt_ticks + 500000000000
    if loop_index == 1:
       os.system('mkdir -p ' + dir)
       os.system('cp -r ~/os_ckpt/4core_3GB/* ' + dir)

    #use larger DRAM to simulate multi-program 
    cmd_run = '~/gem5-micro2017/build/X86_MOESI_hammer/gem5.opt -d ' + dir \
              + ' ~/gem5-micro2017/configs/example/fs.py --cpu-type=timing'\
              + ' --kernel=x86_64-vmlinux-2.6.28.4-smp -n 4   --l1d_size=32kB'\
              + ' --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --l2_size=512kB'\
              + ' --l2_assoc=8 --num-l2caches=4 --ruby'\
              + ' --checkpoint-dir=' + dir + ' -r ' + str(loop_index)\
              + ' --mem-size=' + mem_size\
              + ' --take-checkpoints=' + str(ckpt_ticks)+","+str(ckpt_ticks_next)\
              + ' --restore-with-cpu=timing --script=/home/fan/Dropbox/spec-rcs/'\
              + bench + '_' + input_set + '.rcS' 
    print cmd_run
    os.system(cmd_run)


def run_as_task(task):
    bench, input_set, loop_index = task
    run(bench, input_set, loop_index)



def run_experiments(argv, loop_index):
    try:
      opts, args = getopt.getopt(argv,"i:",["ibench=="])
    except getopt.GetoptError:
      print '-i <benchindex>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print '-i <benchindex> '
         sys.exit()
      elif opt in ("-i", "--ibench"):
         bench_index = int(arg)
    tmp_index=0;
    with open("/home/fan/Dropbox/spec-rcs/mode0_workload_names.dat") as f:
	for name in f:
	    tmp_index+=1
            if tmp_index == bench_index:
	    	wd0 = name;
		tmp_index = 0
                break
    with open("/home/fan/Dropbox/spec-rcs/mode1_workload_names.dat") as f:
	for name in f:
	    tmp_index+=1
            if tmp_index == bench_index:
		tmp_index = 0
	    	wd1 = name;
                break
    with open("/home/fan/Dropbox/spec-rcs/mode2_workload_names.dat") as f:
	for name in f:
	    tmp_index+=1
            if tmp_index == bench_index:
	    	wd2 = name;
                break
    num_processes = 3
    print wd0, wd1,wd2 
    for input_set in input_sets:
        add_tasks(wd0.strip('\n')+'_mode0', input_set, loop_index)
        add_tasks(wd1.strip('\n')+'_mode1', input_set, loop_index)
        add_tasks(wd2.strip('\n')+'_mode2', input_set, loop_index)

    pool = mp.Pool(num_processes)
    pool.map(run_as_task, tasks)

    pool.close()
    pool.join()
    del tasks[:]


def add_task(bench, input_set, loop_index):
    task = (bench, input_set, loop_index)
    tasks.append(task)

# input_sets = ['simsmall', 'simmedium', 'simlarge']
# input_sets = ['simsmall']
# input_sets = ['simmedium']
input_sets = ['ref']


def add_tasks(bench, input_set, loop_index):
    add_task(bench, input_set, loop_index)
    #add_task(bench, input_set, '512kB', 8, 'LRU', 2, 2, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '1MB', 8, 'LRU', 2, 2, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '2MB', 8, 'LRU', 2, 2, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '4MB', 8, 'LRU', 2, 2, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '8MB', 8, 'LRU', 2, 2, '1kB', 8, 'LRU')

    #add_task(bench, input_set, '256kB', 8, 'LRU', 2, 1, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '256kB', 8, 'LRU', 2, 4, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '256kB', 8, 'LRU', 2, 8, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '256kB', 8, 'LRU', 4, 1, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '256kB', 8, 'LRU', 4, 2, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '256kB', 8, 'LRU', 4, 4, '1kB', 8, 'LRU')

    #add_task(bench, input_set, '256kB', 8, 'IbRDP', 2, 2, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '256kB', 8, 'RRIP', 2, 2, '1kB', 8, 'LRU')
    #add_task(bench, input_set, '256kB', 8, 'DBRSP', 2, 2, '1kB', 8, 'LRU')
def run_experiments_loop(argv):
    #try to create checkpoints for ever
    ckpt_index=0;
    while True:
	ckpt_index=ckpt_index+1
    	run_experiments(argv,ckpt_index)
	print "finished loop ", ckpt_index


run_experiments_loop(sys.argv[1:])
