#!/usr/bin/python

#
# A Python script to run all CC-NUMA multi-core experiments for PARSEC 2.1 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os
import multiprocessing as mp


def run(bench, run_num):
    dir =  'exp_compressed/'+ bench + '/run-' + run_num
          # + numa_cache_size + '/' + str(numa_cache_assoc) + 'way/' + numa_cache_tags + '/'
    #os.system('rm -fr ' + dir)
    os.system('mkdir -p ' + dir)

    cmd_run = '../gem5-caco/build/X86_MESI_Two_Level/gem5.opt -d ' + dir  \
			  + ' ../gem5-caco/configs/example/fs.py --cpu-type=timing ' \
	          + '--kernel=x86_64-vmlinux-2.6.28.4-smp -n 8   --l1d_size=8kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --l2_size=8MB ' \
			  + '--l2_assoc=8 --num-l2caches=1 --ruby --garnet=flexible --checkpoint-dir=./os_ckpt/ -r 1 --restore-with-cpu=timing' \
              + ' --script=./rcsfiles/l1pp.rcS' + ' --maxinsts=200000000'
    print cmd_run
    os.system(cmd_run)


def run_as_task(task):
    bench, run_num = task
    run(bench, run_num)

tasks = []


def run_experiments():
    num_processes = 5
    #num_processes = mp.cpu_count()
    pool = mp.Pool(num_processes)
    pool.map(run_as_task, tasks)

    pool.close()
    pool.join()


def add_task(bench, run_num):
    task = (bench, run_num)
    tasks.append(task)


def add_tasks(bench, run_num):
    add_task(bench, run_num)

for run_num in range(1):
    add_tasks('l1pp', str(run_num))

run_experiments()
