#!/bin/bash

cat ./latency.dat | awk '{ for(i=1;i<=64;i++){print i, " ", $i}}'
