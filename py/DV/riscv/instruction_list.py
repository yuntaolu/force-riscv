#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES
# OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import warnings

warnings.warn(
    "DV.instruction_list is deprecated; please use " "DV.riscv.trees.instruction_tree",
    DeprecationWarning,
)

branch_instructions = [
    "BEQ##RISCV",
    "BGE##RISCV",
    "BGEU##RISCV",
    "BLT##RISCV",
    "BLTU##RISCV",
    "BNE##RISCV",
    "JAL##RISCV",
    "JALR##RISCV",
]

instructions = [
    "ADD##RISCV",
    "ADDI##RISCV",
    "ADDIW##RISCV",
    "ADDW##RISCV",
    "AMOADD.D##RISCV",
    "AMOADD.W##RISCV",
    "AMOAND.D##RISCV",
    "AMOAND.W##RISCV",
    "AMOMAX.D##RISCV",
    "AMOMAX.W##RISCV",
    "AMOMAXU.D##RISCV",
    "AMOMAXU.W##RISCV",
    "AMOMIN.D##RISCV",
    "AMOMIN.W##RISCV",
    "AMOMINU.D##RISCV",
    "AMOMINU.W##RISCV",
    "AMOOR.D##RISCV",
    "AMOOR.W##RISCV",
    "AMOSWAP.D##RISCV",
    "AMOSWAP.W##RISCV",
    "AMOXOR.D##RISCV",
    "AMOXOR.W##RISCV",
    "AND##RISCV",
    "ANDI##RISCV",
    "AUIPC##RISCV",
    "BEQ##RISCV",
    "BGE##RISCV",
    "BGEU##RISCV",
    "BLT##RISCV",
    "BLTU##RISCV",
    "BNE##RISCV",
    "CSRRC#register#RISCV",
    "CSRRCI#immediate#RISCV",
    "CSRRS#register#RISCV",
    "CSRRSI#immediate#RISCV",
    "CSRRW#register#RISCV",
    "CSRRWI#immediate#RISCV",
    "DIV##RISCV",
    "DIVU##RISCV",
    "DIVUW##RISCV",
    "DIVW##RISCV",
    "EBREAK##RISCV",
    "ECALL##RISCV",
    "FADD.D#Double-precision#RISCV",
    "FADD.Q#Quad-precision#RISCV",
    "FADD.S#Single-precision#RISCV",
    "FCLASS.D##RISCV",
    "FCLASS.Q##RISCV",
    "FCLASS.S##RISCV",
    "FCVT.D.L##RISCV",
    "FCVT.D.LU##RISCV",
    "FCVT.D.Q##RISCV",
    "FCVT.D.S##RISCV",
    "FCVT.D.W##RISCV",
    "FCVT.D.WU##RISCV",
    "FCVT.L.D##RISCV",
    "FCVT.L.Q##RISCV",
    "FCVT.L.S##RISCV",
    "FCVT.LU.D##RISCV",
    "FCVT.LU.Q##RISCV",
    "FCVT.LU.S##RISCV",
    "FCVT.Q.D##RISCV",
    "FCVT.Q.L##RISCV",
    "FCVT.Q.LU##RISCV",
    "FCVT.Q.S##RISCV",
    "FCVT.Q.W##RISCV",
    "FCVT.Q.WU##RISCV",
    "FCVT.S.D##RISCV",
    "FCVT.S.L##RISCV",
    "FCVT.S.LU##RISCV",
    "FCVT.S.Q##RISCV",
    "FCVT.S.W##RISCV",
    "FCVT.S.WU##RISCV",
    "FCVT.W.D##RISCV",
    "FCVT.W.Q##RISCV",
    "FCVT.W.S##RISCV",
    "FCVT.WU.D##RISCV",
    "FCVT.WU.Q##RISCV",
    "FCVT.WU.S##RISCV",
    "FDIV.D#Double-precision#RISCV",
    "FDIV.Q#Quad-precision#RISCV",
    "FDIV.S#Single-precision#RISCV",
    "FENCE##RISCV",
    "FENCE.I##RISCV",
    "FEQ.D##RISCV",
    "FEQ.Q##RISCV",
    "FEQ.S##RISCV",
    "FLD##RISCV",
    "FLE.D##RISCV",
    "FLE.Q##RISCV",
    "FLE.S##RISCV",
    "FLQ##RISCV",
    "FLT.D##RISCV",
    "FLT.Q##RISCV",
    "FLT.S##RISCV",
    "FLW##RISCV",
    "FMADD.D#Double-precision#RISCV",
    "FMADD.Q#Quad-precision#RISCV",
    "FMADD.S#Single-precision#RISCV",
    "FMAX.D##RISCV",
    "FMAX.Q##RISCV",
    "FMAX.S##RISCV",
    "FMIN.D##RISCV",
    "FMIN.Q##RISCV",
    "FMIN.S##RISCV",
    "FMSUB.D#Double-precision#RISCV",
    "FMSUB.Q#Quad-precision#RISCV",
    "FMSUB.S#Single-precision#RISCV",
    "FMUL.D#Double-precision#RISCV",
    "FMUL.Q#Quad-precision#RISCV",
    "FMUL.S#Single-precision#RISCV",
    "FMV.D.X##RISCV",
    "FMV.W.X##RISCV",
    "FMV.X.D##RISCV",
    "FMV.X.W##RISCV",
    "FNMADD.D#Double-precision#RISCV",
    "FNMADD.Q#Quad-precision#RISCV",
    "FNMADD.S#Single-precision#RISCV",
    "FNMSUB.D#Double-precision#RISCV",
    "FNMSUB.Q#Quad-precision#RISCV",
    "FNMSUB.S#Single-precision#RISCV",
    "FSD##RISCV",
    "FSGNJ.D##RISCV",
    "FSGNJ.Q##RISCV",
    "FSGNJ.S##RISCV",
    "FSGNJN.D##RISCV",
    "FSGNJN.Q##RISCV",
    "FSGNJN.S##RISCV",
    "FSGNJX.D##RISCV",
    "FSGNJX.Q##RISCV",
    "FSGNJX.S##RISCV",
    "FSQ##RISCV",
    "FSQRT.D##RISCV",
    "FSQRT.Q##RISCV",
    "FSQRT.S##RISCV",
    "FSUB.D#Double-precision#RISCV",
    "FSUB.Q#Quad-precision#RISCV",
    "FSUB.S#Single-precision#RISCV",
    "FSW##RISCV",
    "JAL##RISCV",
    "JALR##RISCV",
    "LB##RISCV",
    "LBU##RISCV",
    "LD##RISCV",
    "LH##RISCV",
    "LHU##RISCV",
    "LR.D##RISCV",
    "LR.W##RISCV",
    "LUI##RISCV",
    "LW##RISCV",
    "LWU##RISCV",
    "MUL##RISCV",
    "MULH##RISCV",
    "MULHSU##RISCV",
    "MULHU##RISCV",
    "MULW##RISCV",
    "OR##RISCV",
    "ORI##RISCV",
    "REM##RISCV",
    "REMU##RISCV",
    "REMUW##RISCV",
    "REMW##RISCV",
    "SB##RISCV",
    "SC.D##RISCV",
    "SC.W##RISCV",
    "SD##RISCV",
    "SH##RISCV",
    "SLL##RISCV",
    "SLLI#RV32I#RISCV",
    "SLLI#RV64I#RISCV",
    "SLLIW##RISCV",
    "SLLW##RISCV",
    "SLT##RISCV",
    "SLTI##RISCV",
    "SLTIU##RISCV",
    "SLTU##RISCV",
    "SRA##RISCV",
    "SRAI#RV32I#RISCV",
    "SRAI#RV64I#RISCV",
    "SRAIW##RISCV",
    "SRAW##RISCV",
    "SRL##RISCV",
    "SRLI#RV32I#RISCV",
    "SRLI#RV64I#RISCV",
    "SRLIW##RISCV",
    "SRLW##RISCV",
    "SUB##RISCV",
    "SUBW##RISCV",
    "SW##RISCV",
    "XOR##RISCV",
    "XORI##RISCV",
]
