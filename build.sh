#!/bin/bash
# A script to build force-riscv
####################
# Download the force-riscv source
####################
# Fork from https://github.com/openhwgroup/force-riscv
# git clone https://github.com/yuntaolu/ForceRiscv
# cd force-riscv
# git status
# In dev branch

####################
# Build the force-riscv executable
####################
source env.sh
pushd ${FORCE_RISCV}
make clean
make -j32 2>&1 | tee ${FORCE_RISCV_ROOT}/make.log
make tests -j32 2>&1 | tee ${FORCE_RISCV_ROOT}/make_tests.log
popd

####################
# Run examples test generation
####################
# pushd ${FORCE_RISCV_ROOT}
# mkdir -p force_test_rv64
# pushd force_test_rv64
# ${FORCE_RISCV}/utils/regression/master_run.py -f ${FORCE_RISCV}/test/riscv/_def_ctrl.py -c ${FORCE_RISCV}/utils/regression/config/_riscv_rv64_fcfg.py -k all
# popd
# popd
