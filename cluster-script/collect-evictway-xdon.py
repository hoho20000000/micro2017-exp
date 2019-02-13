#!/usr/bin/python

#
# A Python script to run all CC-NUMA multi-core experiments for PARSEC 2.1 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os
import multiprocessing as mp
import sys,getopt


ckp_tick_512 = '4881191223250'
ckp_tick_2048 = '5046198013500'
ckp_tick_3072 = '5160523235750'
mem_size='3GB'
wd0=''
wd1=''
wd2=''
def run(bench, input_set):
    dir =  '/home/fan/gem5-out-disk/mtrace-micro2017/'+ bench + '/' + input_set\
           + "/l2-evict-new"
    os.system('mkdir -p ' + dir)
    os.system('cp -r ~/os_ckpt/4core_3GB/* ' + dir)

    #use larger DRAM to simulate multi-program 
    cmd_run = '~/gem5-micro2017/build/X86_MESI_Two_Level/gem5.opt -d ' + dir \
              + ' --debug-flag=WayEvictMICRO17 --debug-file=evict-way.out.gz'\
              + ' --debug-start=' + ckp_tick_3072 \
              + ' ~/gem5-micro2017/configs/example/fs.py --cpu-type=timing'\
              + ' --kernel=x86_64-vmlinux-2.6.28.4-smp -n 4   --l1d_size=32kB'\
              + ' --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --l2_size=512kB'\
              + ' --l2_assoc=8 --num-l2caches=4 --ruby --garnet=flexible'\
              + ' --checkpoint-dir=/home/fan/os_ckpt/4core_3GB -r 1'\
              + ' --mem-size=' + mem_size\
              + '  --restore-with-cpu=timing --script=/home/fan/Dropbox/spec-rcs/'\
              + bench + '_' + input_set + '.rcS' 
    print cmd_run
    os.system(cmd_run)


def run_as_task(task):
    bench, input_set = task
    run(bench, input_set)

tasks = []


def run_experiments(argv):
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
    num_processes = 4
    print wd0, wd1,wd2 
    for input_set in input_sets:
        add_tasks(wd0.strip('\n')+'_mode0', input_set)
        add_tasks(wd1.strip('\n')+'_mode1', input_set)
        add_tasks(wd2.strip('\n')+'_mode2', input_set)

    pool = mp.Pool(num_processes)
    pool.map(run_as_task, tasks)

    pool.close()
    pool.join()


def add_task(bench, input_set):
    task = (bench, input_set)
    tasks.append(task)

input_sets = ['ref']


def add_tasks(bench, input_set):
    add_task(bench, input_set)


run_experiments(sys.argv[1:])
