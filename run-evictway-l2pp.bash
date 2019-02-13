#!/bin/bash

../gem5-fy/build/X86_MESI_Two_Level/gem5.opt -d ../gem5-out-disk/mtrace-micro2017/l2-prime-probe/ref-evict --debug-flag=WayEvictMICRO17 --debug-file=evict-way.out ../gem5-fy/configs/example/fs.py  --cpu-type=timing --kernel=x86_64-vmlinux-2.6.28.4-smp -n 4   --l1d_size=32kB --l1i_size=32kB --l1d_assoc=2 --l1i_assoc=2 --l2_size=512kB --l2_assoc=8 --num-l2caches=4 --ruby --garnet=flexible --checkpoint-dir=./checkpoints/hack_ckpt_2GB/ -r 1 --mem-size=2GB  --restore-with-cpu=timing --script=./rcS_files/l2-prime-probe.rcS

