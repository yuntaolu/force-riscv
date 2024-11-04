# Installation Guiude
Build and test guide for FORCE-RISCV, referring to [README.md](./README.md)

## Setup
* Request access to private repository.
* Clone the FORCE-RISCV repository:
  * ` git clone git@github.com:yuntaolu/force-riscv.git`
  * ` cd [base_directory]/force-riscv/`

* Set the build  environment 
  * ` source env.sh`
  * Note: python: 3.6, gcc version: 9.4.0
  * In `env.sh`, for example in conda python 3.6 environment named `force` with gnu 9.4.0 on Debian Linux systems
  * `export FORCE_RISCV=/usr/local/bin/g++`
  * `export FORCE_PYTHON_VER=3.6`
  * `export FORCE_PYTHON_LIB=$HOME/miniforge3/envs/force/lib`
  * `export FORCE_PYTHON_INC=$HOME/miniforge3/envs/force/include/python3.6m`
  * `export FORCE_RISCV_ROOT=$HOME/projects`
  * `export FORCE_RISCV=${FORCE_RISCV_ROOT}/force-riscv`
  * `export LD_LIBRARY_PATH=$FORCE_PYTHON_LIB:$LD_LIBRARY_PATH`
  * `source setenv.bash`

* Build FORCE-RISCV
  * `./build.sh`
  * In `build.sh`, it will make the project and generate executions in `./bin`

* Regression Test FORCE-RISCV
  * `./test.sh`
  * In `test.sh`, it will execute regression tests of all templates in FORCE-RISCV
  * `mkdir -p force_test_rv64`
  * `cd force_test_rv64`
  * `${FORCE_RISCV}/utils/regression/master_run.py -f ${FORCE_RISCV}/tests/riscv/_def_fctrl.py -c ${FORCE_RISCV}/utils/regression/config/_riscv_rv64_fcfg.py -k all 2>&1 | tee regression.log`

* An Example of Unconditional Branches Test FORCE-RISCV
 * Generate 10 test cases. [branch_tests](./branch_tests)
 * `python generate_branch_test.py`
