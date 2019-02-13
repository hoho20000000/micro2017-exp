#!/usr/bin/python

#
# A Python script to run all CC-NUMA multi-core experiments for PARSEC 2.1 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os
import multiprocessing as mp


ckp_tick_512 = '4881191223250'
ckp_tick_2048 = '5046198013500'
ckp_tick_4096 = '5160523235750'
mem_size='2GB'
def run(bench, input_set):
    dir =  '../gem5-out-disk/mtrace-micro2017/'+ bench + '/' + input_set\
           + "-l2-evict"
    os.system('mkdir -p ' + dir)

    #use larger DRAM to simulate multi-program 
    cmd_run = '../gem5-micro2017/build/X86_MESI_Two_Level/gem5.opt -d ' + dir \
              + ' ../gem5-micro2017/configs/example/fs.py --cpu-type=timing'\
              + ' --kernel=x86_64-vmlinux-2.6.28.4-smp -n 4   --l1d_size=32kB'\
              + ' --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --l2_size=512kB'\
              + ' --l2_assoc=8 --num-l2caches=4 --ruby --garnet=flexible'\
              + ' --checkpoint-dir=$GEM5_CKPT_DIR/4core_2GB/ -r 1'\
              + ' --mem-size=' + mem_size\
              + '  --restore-with-cpu=timing --script=../spec-rcs/'\
              + bench + '_' + input_set + '.rcS' + ' --maxinsts=1000000000'
    print cmd_run
    os.system(cmd_run)


def run_as_task(task):
    bench, input_set = task
    run(bench, input_set)

tasks = []


def run_experiments():
    num_processes = 4
    #num_processes = mp.cpu_count()
    pool = mp.Pool(num_processes)
    pool.map(run_as_task, tasks)

    pool.close()
    pool.join()


def add_task(bench, input_set):
    task = (bench, input_set)
    tasks.append(task)

# input_sets = ['simsmall', 'simmedium', 'simlarge']
# input_sets = ['simsmall']
# input_sets = ['simmedium']
input_sets = ['ref']


def add_tasks(bench, input_set):
    add_task(bench, input_set)
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

for input_set in input_sets:
    ##SPEC BENCHMARK
    #add_tasks('bzip2', input_set)
    #add_tasks('sjeng', input_set)
    #add_tasks('gobmk', input_set) ok
    #add_tasks('h264ref', input_set) ok
    #add_tasks('hmmer', input_set) ok
    #add_tasks('libquantum', input_set)
    #add_tasks('mcf', input_set) 
    #add_tasks('omnetpp', input_set)
    #add_tasks('specrand', input_set)
    #add_tasks('xalancbmk', input_set)#no output, checked, worked
    #add_tasks('dealII', input_set) #no output, checked, worked
    #add_tasks('GemsFDTD', input_set)
    #add_tasks('lbm', input_set)
    #add_tasks('milc', input_set)
    #add_tasks('namd', input_set)#no output
    #add_tasks('povray', input_set)#no output
    add_tasks('soplex', input_set)# did not run due to script error
    #add_tasks('sphinx3', input_set)#no output

    #add_tasks('combine_bzip2_sjeng', input_set)
    #add_tasks('combine_gobmk_h264ref', input_set)
    #add_tasks('combine_sjeng_h264ref', input_set)
    #add_tasks('combine_bzip2_h264ref', input_set)
    #add_tasks('combine_gobmk_h264ref_sjeng_bzip2', input_set)

run_experiments()
