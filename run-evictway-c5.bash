#!/bin/bash
mkdir -p ../gem5-out-disk/mtrace-micro2017/c5/base
mkdir -p ../gem5-out-disk/mtrace-micro2017/c5/l2-evict

../gem5-fy/build/X86_MESI_Two_Level/gem5.opt -d ../gem5-out-disk/mtrace-micro2017/c5/ref-evict --debug-flag=RubyPrefetcher --debug-file=evict-way.out --debug-start=5046198013500 ../gem5-fy/configs/example/fs.py --cpu-type=timing --kernel=x86_64-vmlinux-2.6.28.4-smp -n 4   --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --l2_size=512kB --l2_assoc=8 --num-l2caches=4 --ruby --garnet=flexible --checkpoint-dir=../system-files/hack_ckpt_2GB/ -r 1 --mem-size=2GB  --restore-with-cpu=timing --script=./rcS_files/c5.rcS

