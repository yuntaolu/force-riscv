#!/bin/bash
####################
# Run examples test generation
####################
 pushd ${FORCE_RISCV_ROOT}
 mkdir -p force_test_rv64
 pushd force_test_rv64
 ${FORCE_RISCV}/utils/regression/master_run.py -f ${FORCE_RISCV}/tests/riscv/_def_fctrl.py -c ${FORCE_RISCV}/utils/regression/config/_riscv_rv64_fcfg.py -k all 2>&1 | tee regression.log
 popd
 popd
