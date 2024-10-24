#!/bin/bash
# A script to execute an example - loop_unconditional_branches_force
# Generation command:
/home/ytlu/projects/force-riscv/bin/friscv -t /home/ytlu/projects/force-riscv/tests/riscv/loop/loop_unconditional_branches_force.py --max-instr 12000 --num-chips 1 --num-cores 1 --num-threads 1 -s 0x3fbf0812edeb0d84 --cfg config/riscv_rv64.config  --noiss

# ISS command:
/home/ytlu/projects/force-riscv/fpix/bin/fpix_riscv --railhouse fpix_riscv.railhouse --cluster_num 1 --core_num 1 --threads_per_cpu 1 -i 12000 --cfg /home/ytlu/projects/force-riscv/fpix/config/riscv_rv64.config loop_unconditional_branches_force.Default.ELF

