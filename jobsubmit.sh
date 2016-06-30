#!/bin/sh
# @ job_name           = 1024x50Padded
# @ job_type           = bluegene
# @ comment            = "n=1024, m=50, zero-padded"
# @ error              = $(job_name).$(Host).$(jobid).err
# @ output             = $(job_name).$(Host).$(jobid).out
# @ bg_size            = 128
# @ wall_clock_limit   = 30:00
# @ bg_connectivity    = Torus
# @ queue 

source /scratch/s/scinet/nolta/venv-numpy/setup

NP=2048
OMP=4 ## Each core has 4 threads. Since RPN = 16, OMP = 4?
RPN=16

module purge

module load python/2.7.3
module load xlf/14.1 essl/5.1

cd /home/p/pen/seaifan/Scintillometry/src

mkdir results

echo "----------------------"
echo "STARTING in directory $PWD"
date
echo "np ${NP}, rpn ${RPN}, omp ${OMP}"

OMP_NUM_THREADS=${OMP}
time runjob --np ${NP} --ranks-per-node=${RPN} --env-all : `which python` run_real.py yty2 0 148 1024 50 100 1

echo "ENDED"
date
