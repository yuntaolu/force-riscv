#!/bin/bash
# A script to source environment parameters

# gcc version 9.4.0 (Debian 12.2.0-14)
# python conda env force python 3.6.15
export FORCE_RISCV=/usr/local/bin/g++
export FORCE_PYTHON_VER=3.6
export FORCE_PYTHON_LIB=$HOME/miniforge3/envs/force/lib 
export FORCE_PYTHON_INC=$HOME/miniforge3/envs/force/include/python3.6m

export FORCE_RISCV_ROOT=$HOME/projects
export FORCE_RISCV=${FORCE_RISCV_ROOT}/force-riscv
export LD_LIBRARY_PATH=$FORCE_PYTHON_LIB:$LD_LIBRARY_PATH

pushd ${FORCE_RISCV}
source setenv.bash
popd
