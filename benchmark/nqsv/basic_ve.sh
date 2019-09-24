#!/bin/sh

#PBS -T necmpi
#PBS --venode=1
#PBS -q hackathonque


source /opt/nec/nosupport/frovedis/ve/bin/veenv.sh

script_dir=$HOME/frovedis  # SET YOUR OWN PATH

python $script_dir/basic.py
