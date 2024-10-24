import time
import os
import subprocess




# /home/ytlu/projects/force-riscv/bin/friscv -t /home/ytlu/projects/force-riscv/tests/riscv/loop/loop_unconditional_branches_force.py --max-instr 12000 --num-chips 1 --num-cores 1 --num-threads 1 -s 0x3fbf0812edeb0d84 --cfg config/riscv_rv64.config  --noiss
# Execute a shell command
# Execute a shell command
friscv = '/home/ytlu/projects/force-riscv/bin/friscv'
force = '/home/ytlu/projects/force-riscv/tests/riscv/loop/loop_unconditional_branches_force.py'
config = '/home/ytlu/projects/force-riscv/config/riscv_rv64.config'
log = '/home/ytlu/projects/force-riscv/branch_tests/loop_branch.log'



for loop in range(10):
    # Use current time in milliseconds as a seed
    random_seed = int(time.time() * 1000)
    print(f'Random seed: {random_seed}')
    clean = subprocess.run(['rm', '*.ELF', '*.S'])
    result = subprocess.run([friscv, '-t', force, '--max-instr', '256', '--num-chips', '1', '--num-cores', '1', '--num-threads', '1', '-s', f'0x{random_seed:016x}', '--cfg', config, '--noiss'])

    elf_file = 'loop_unconditional_branches_force.Default.ELF'
    elf_file_new = 'branch_test_' + str(loop) + '.ELF'
    assembly_file = 'loop_unconditional_branches_force.Default.S'
    assembly_file_new = 'branch_test_' + str(loop) + '.S'
    rename_elf = subprocess.run(['mv', elf_file, elf_file_new])
    rename_s = subprocess.run(['mv', assembly_file, assembly_file_new])
