#!/usr/bin/env python3

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

"""
This script needs to be run before make whenever changes have been made to
pike or Handcar base code
"""

import errno
import glob
import os
import shutil

# Controls
NOISY = True

ORIGINAL_SOURCE_DIR = "standalone"
ORIGINAL_SOFTFLOAT_DIR = "standalone/softfloat"
ORIGINAL_INSNS_DIR = "standalone"
ORIGINAL_INSN_HEADERS_DIR = "standalone/riscv/insns"
REPLACEMENTS_DIR = "spike_mod"
SRC = "./src"
INC = "./inc"
INC_INSNS = INC + "/insns"

# These instruction files are generated during the configuration phase of an
# Original Spike build.
INSN_SOURCE_FILENAMES = [
    "add.cc",
    "addi.cc",
    "addiw.cc",
    "addw.cc",
    "amoadd_d.cc",
    "amoadd_w.cc",
    "amoand_d.cc",
    "amoand_w.cc",
    "amomax_d.cc",
    "amomax_w.cc",
    "amomaxu_d.cc",
    "amomaxu_w.cc",
    "amomin_d.cc",
    "amomin_w.cc",
    "amominu_d.cc",
    "amominu_w.cc",
    "amoor_d.cc",
    "amoor_w.cc",
    "amoswap_d.cc",
    "amoswap_w.cc",
    "amoxor_d.cc",
    "amoxor_w.cc",
    "and.cc",
    "andi.cc",
    "auipc.cc",
    "beq.cc",
    "bge.cc",
    "bgeu.cc",
    "blt.cc",
    "bltu.cc",
    "bne.cc",
    "c_add.cc",
    "c_addi.cc",
    "c_addi4spn.cc",
    "c_addw.cc",
    "c_and.cc",
    "c_andi.cc",
    "c_beqz.cc",
    "c_bnez.cc",
    "c_ebreak.cc",
    "c_fld.cc",
    "c_fldsp.cc",
    "c_flw.cc",
    "c_flwsp.cc",
    "c_fsd.cc",
    "c_fsdsp.cc",
    "c_fsw.cc",
    "c_fswsp.cc",
    "c_j.cc",
    "c_jal.cc",
    "c_jalr.cc",
    "c_jr.cc",
    "c_li.cc",
    "c_lui.cc",
    "c_lw.cc",
    "c_lwsp.cc",
    "c_mv.cc",
    "c_or.cc",
    "c_slli.cc",
    "c_srai.cc",
    "c_srli.cc",
    "c_sub.cc",
    "c_subw.cc",
    "c_sw.cc",
    "c_swsp.cc",
    "c_xor.cc",
    "csrrc.cc",
    "csrrci.cc",
    "csrrs.cc",
    "csrrsi.cc",
    "csrrw.cc",
    "csrrwi.cc",
    "div.cc",
    "divu.cc",
    "divuw.cc",
    "divw.cc",
    "dret.cc",
    "ebreak.cc",
    "ecall.cc",
    "fadd_d.cc",
    "fadd_h.cc",
    "fadd_q.cc",
    "fadd_s.cc",
    "fclass_d.cc",
    "fclass_h.cc",
    "fclass_q.cc",
    "fclass_s.cc",
    "fcvt_d_h.cc",
    "fcvt_d_l.cc",
    "fcvt_d_lu.cc",
    "fcvt_d_q.cc",
    "fcvt_d_s.cc",
    "fcvt_d_w.cc",
    "fcvt_d_wu.cc",
    "fcvt_h_d.cc",
    "fcvt_h_l.cc",
    "fcvt_h_lu.cc",
    "fcvt_h_q.cc",
    "fcvt_h_s.cc",
    "fcvt_h_w.cc",
    "fcvt_h_wu.cc",
    "fcvt_l_d.cc",
    "fcvt_l_h.cc",
    "fcvt_l_q.cc",
    "fcvt_l_s.cc",
    "fcvt_lu_d.cc",
    "fcvt_lu_h.cc",
    "fcvt_lu_q.cc",
    "fcvt_lu_s.cc",
    "fcvt_q_d.cc",
    "fcvt_q_h.cc",
    "fcvt_q_l.cc",
    "fcvt_q_lu.cc",
    "fcvt_q_s.cc",
    "fcvt_q_w.cc",
    "fcvt_q_wu.cc",
    "fcvt_s_d.cc",
    "fcvt_s_h.cc",
    "fcvt_s_l.cc",
    "fcvt_s_lu.cc",
    "fcvt_s_q.cc",
    "fcvt_s_w.cc",
    "fcvt_s_wu.cc",
    "fcvt_w_d.cc",
    "fcvt_w_h.cc",
    "fcvt_w_q.cc",
    "fcvt_w_s.cc",
    "fcvt_wu_d.cc",
    "fcvt_wu_h.cc",
    "fcvt_wu_q.cc",
    "fcvt_wu_s.cc",
    "fdiv_d.cc",
    "fdiv_h.cc",
    "fdiv_q.cc",
    "fdiv_s.cc",
    "fence.cc",
    "fence_i.cc",
    "feq_d.cc",
    "feq_h.cc",
    "feq_q.cc",
    "feq_s.cc",
    "fld.cc",
    "fle_d.cc",
    "fle_h.cc",
    "fle_q.cc",
    "fle_s.cc",
    "flh.cc",
    "flq.cc",
    "flt_d.cc",
    "flt_h.cc",
    "flt_q.cc",
    "flt_s.cc",
    "flw.cc",
    "fmadd_d.cc",
    "fmadd_h.cc",
    "fmadd_q.cc",
    "fmadd_s.cc",
    "fmax_d.cc",
    "fmax_h.cc",
    "fmax_q.cc",
    "fmax_s.cc",
    "fmin_d.cc",
    "fmin_h.cc",
    "fmin_q.cc",
    "fmin_s.cc",
    "fmsub_d.cc",
    "fmsub_h.cc",
    "fmsub_q.cc",
    "fmsub_s.cc",
    "fmul_d.cc",
    "fmul_h.cc",
    "fmul_q.cc",
    "fmul_s.cc",
    "fmv_d_x.cc",
    "fmv_h_x.cc",
    "fmv_w_x.cc",
    "fmv_x_d.cc",
    "fmv_x_h.cc",
    "fmv_x_w.cc",
    "fnmadd_d.cc",
    "fnmadd_h.cc",
    "fnmadd_q.cc",
    "fnmadd_s.cc",
    "fnmsub_d.cc",
    "fnmsub_h.cc",
    "fnmsub_q.cc",
    "fnmsub_s.cc",
    "fsd.cc",
    "fsgnj_d.cc",
    "fsgnj_h.cc",
    "fsgnj_q.cc",
    "fsgnj_s.cc",
    "fsgnjn_d.cc",
    "fsgnjn_h.cc",
    "fsgnjn_q.cc",
    "fsgnjn_s.cc",
    "fsgnjx_d.cc",
    "fsgnjx_h.cc",
    "fsgnjx_q.cc",
    "fsgnjx_s.cc",
    "fsh.cc",
    "fsq.cc",
    "fsqrt_d.cc",
    "fsqrt_h.cc",
    "fsqrt_q.cc",
    "fsqrt_s.cc",
    "fsub_d.cc",
    "fsub_h.cc",
    "fsub_q.cc",
    "fsub_s.cc",
    "fsw.cc",
    "jal.cc",
    "jalr.cc",
    "lb.cc",
    "lbu.cc",
    "ld.cc",
    "lh.cc",
    "lhu.cc",
    "lr_d.cc",
    "lr_w.cc",
    "lui.cc",
    "lw.cc",
    "lwu.cc",
    "mret.cc",
    "mul.cc",
    "mulh.cc",
    "mulhsu.cc",
    "mulhu.cc",
    "mulw.cc",
    "or.cc",
    "ori.cc",
    "rem.cc",
    "remu.cc",
    "remuw.cc",
    "remw.cc",
    "sb.cc",
    "sc_d.cc",
    "sc_w.cc",
    "sd.cc",
    "sfence_vma.cc",
    "sh.cc",
    "sll.cc",
    "slli.cc",
    "slliw.cc",
    "sllw.cc",
    "slt.cc",
    "slti.cc",
    "sltiu.cc",
    "sltu.cc",
    "sra.cc",
    "srai.cc",
    "sraiw.cc",
    "sraw.cc",
    "sret.cc",
    "srl.cc",
    "srli.cc",
    "srliw.cc",
    "srlw.cc",
    "sub.cc",
    "subw.cc",
    "sw.cc",
    "vaadd_vv.cc",
    "vaadd_vx.cc",
    "vaaddu_vv.cc",
    "vaaddu_vx.cc",
    "vadc_vim.cc",
    "vadc_vvm.cc",
    "vadc_vxm.cc",
    "vadd_vi.cc",
    "vadd_vv.cc",
    "vadd_vx.cc",
    "vamoadde16_v.cc",
    "vamoadde32_v.cc",
    "vamoadde64_v.cc",
    "vamoadde8_v.cc",
    "vamoande16_v.cc",
    "vamoande32_v.cc",
    "vamoande64_v.cc",
    "vamoande8_v.cc",
    "vamomaxe16_v.cc",
    "vamomaxe32_v.cc",
    "vamomaxe64_v.cc",
    "vamomaxe8_v.cc",
    "vamomaxue16_v.cc",
    "vamomaxue32_v.cc",
    "vamomaxue64_v.cc",
    "vamomaxue8_v.cc",
    "vamomine16_v.cc",
    "vamomine32_v.cc",
    "vamomine64_v.cc",
    "vamomine8_v.cc",
    "vamominue16_v.cc",
    "vamominue32_v.cc",
    "vamominue64_v.cc",
    "vamominue8_v.cc",
    "vamoore16_v.cc",
    "vamoore32_v.cc",
    "vamoore64_v.cc",
    "vamoore8_v.cc",
    "vamoswape16_v.cc",
    "vamoswape32_v.cc",
    "vamoswape64_v.cc",
    "vamoswape8_v.cc",
    "vamoxore16_v.cc",
    "vamoxore32_v.cc",
    "vamoxore64_v.cc",
    "vamoxore8_v.cc",
    "vand_vi.cc",
    "vand_vv.cc",
    "vand_vx.cc",
    "vasub_vv.cc",
    "vasub_vx.cc",
    "vasubu_vv.cc",
    "vasubu_vx.cc",
    "vcompress_vm.cc",
    "vdiv_vv.cc",
    "vdiv_vx.cc",
    "vdivu_vv.cc",
    "vdivu_vx.cc",
    "vdot_vv.cc",
    "vdotu_vv.cc",
    "vfadd_vf.cc",
    "vfadd_vv.cc",
    "vfclass_v.cc",
    "vfcvt_f_x_v.cc",
    "vfcvt_f_xu_v.cc",
    "vfcvt_rtz_x_f_v.cc",
    "vfcvt_rtz_xu_f_v.cc",
    "vfcvt_x_f_v.cc",
    "vfcvt_xu_f_v.cc",
    "vfdiv_vf.cc",
    "vfdiv_vv.cc",
    "vfdot_vv.cc",
    "vfirst_m.cc",
    "vfmacc_vf.cc",
    "vfmacc_vv.cc",
    "vfmadd_vf.cc",
    "vfmadd_vv.cc",
    "vfmax_vf.cc",
    "vfmax_vv.cc",
    "vfmerge_vfm.cc",
    "vfmin_vf.cc",
    "vfmin_vv.cc",
    "vfmsac_vf.cc",
    "vfmsac_vv.cc",
    "vfmsub_vf.cc",
    "vfmsub_vv.cc",
    "vfmul_vf.cc",
    "vfmul_vv.cc",
    "vfmv_f_s.cc",
    "vfmv_s_f.cc",
    "vfmv_v_f.cc",
    "vfncvt_f_f_w.cc",
    "vfncvt_f_x_w.cc",
    "vfncvt_f_xu_w.cc",
    "vfncvt_rod_f_f_w.cc",
    "vfncvt_rtz_x_f_w.cc",
    "vfncvt_rtz_xu_f_w.cc",
    "vfncvt_x_f_w.cc",
    "vfncvt_xu_f_w.cc",
    "vfnmacc_vf.cc",
    "vfnmacc_vv.cc",
    "vfnmadd_vf.cc",
    "vfnmadd_vv.cc",
    "vfnmsac_vf.cc",
    "vfnmsac_vv.cc",
    "vfnmsub_vf.cc",
    "vfnmsub_vv.cc",
    "vfrdiv_vf.cc",
    "vfredmax_vs.cc",
    "vfredmin_vs.cc",
    "vfredosum_vs.cc",
    "vfredsum_vs.cc",
    "vfrsub_vf.cc",
    "vfsgnj_vf.cc",
    "vfsgnj_vv.cc",
    "vfsgnjn_vf.cc",
    "vfsgnjn_vv.cc",
    "vfsgnjx_vf.cc",
    "vfsgnjx_vv.cc",
    "vfslide1down_vf.cc",
    "vfslide1up_vf.cc",
    "vfsqrt_v.cc",
    "vfsub_vf.cc",
    "vfsub_vv.cc",
    "vfwadd_vf.cc",
    "vfwadd_vv.cc",
    "vfwadd_wf.cc",
    "vfwadd_wv.cc",
    "vfwcvt_f_f_v.cc",
    "vfwcvt_f_x_v.cc",
    "vfwcvt_f_xu_v.cc",
    "vfwcvt_rtz_x_f_v.cc",
    "vfwcvt_rtz_xu_f_v.cc",
    "vfwcvt_x_f_v.cc",
    "vfwcvt_xu_f_v.cc",
    "vfwmacc_vf.cc",
    "vfwmacc_vv.cc",
    "vfwmsac_vf.cc",
    "vfwmsac_vv.cc",
    "vfwmul_vf.cc",
    "vfwmul_vv.cc",
    "vfwnmacc_vf.cc",
    "vfwnmacc_vv.cc",
    "vfwnmsac_vf.cc",
    "vfwnmsac_vv.cc",
    "vfwredosum_vs.cc",
    "vfwredsum_vs.cc",
    "vfwsub_vf.cc",
    "vfwsub_vv.cc",
    "vfwsub_wf.cc",
    "vfwsub_wv.cc",
    "vid_v.cc",
    "viota_m.cc",
    "vl1r_v.cc",
    "vle16_v.cc",
    "vle16ff_v.cc",
    "vle32_v.cc",
    "vle32ff_v.cc",
    "vle64_v.cc",
    "vle64ff_v.cc",
    "vle8_v.cc",
    "vle8ff_v.cc",
    "vlse16_v.cc",
    "vlse32_v.cc",
    "vlse64_v.cc",
    "vlse8_v.cc",
    "vlxei16_v.cc",
    "vlxei32_v.cc",
    "vlxei64_v.cc",
    "vlxei8_v.cc",
    "vmacc_vv.cc",
    "vmacc_vx.cc",
    "vmadc_vim.cc",
    "vmadc_vvm.cc",
    "vmadc_vxm.cc",
    "vmadd_vv.cc",
    "vmadd_vx.cc",
    "vmand_mm.cc",
    "vmandnot_mm.cc",
    "vmax_vv.cc",
    "vmax_vx.cc",
    "vmaxu_vv.cc",
    "vmaxu_vx.cc",
    "vmerge_vim.cc",
    "vmerge_vvm.cc",
    "vmerge_vxm.cc",
    "vmfeq_vf.cc",
    "vmfeq_vv.cc",
    "vmfge_vf.cc",
    "vmfgt_vf.cc",
    "vmfle_vf.cc",
    "vmfle_vv.cc",
    "vmflt_vf.cc",
    "vmflt_vv.cc",
    "vmfne_vf.cc",
    "vmfne_vv.cc",
    "vmin_vv.cc",
    "vmin_vx.cc",
    "vminu_vv.cc",
    "vminu_vx.cc",
    "vmnand_mm.cc",
    "vmnor_mm.cc",
    "vmor_mm.cc",
    "vmornot_mm.cc",
    "vmsbc_vvm.cc",
    "vmsbc_vxm.cc",
    "vmsbf_m.cc",
    "vmseq_vi.cc",
    "vmseq_vv.cc",
    "vmseq_vx.cc",
    "vmsgt_vi.cc",
    "vmsgt_vx.cc",
    "vmsgtu_vi.cc",
    "vmsgtu_vx.cc",
    "vmsif_m.cc",
    "vmsle_vi.cc",
    "vmsle_vv.cc",
    "vmsle_vx.cc",
    "vmsleu_vi.cc",
    "vmsleu_vv.cc",
    "vmsleu_vx.cc",
    "vmslt_vv.cc",
    "vmslt_vx.cc",
    "vmsltu_vv.cc",
    "vmsltu_vx.cc",
    "vmsne_vi.cc",
    "vmsne_vv.cc",
    "vmsne_vx.cc",
    "vmsof_m.cc",
    "vmul_vv.cc",
    "vmul_vx.cc",
    "vmulh_vv.cc",
    "vmulh_vx.cc",
    "vmulhsu_vv.cc",
    "vmulhsu_vx.cc",
    "vmulhu_vv.cc",
    "vmulhu_vx.cc",
    "vmv1r_v.cc",
    "vmv2r_v.cc",
    "vmv4r_v.cc",
    "vmv8r_v.cc",
    "vmv_s_x.cc",
    "vmv_v_i.cc",
    "vmv_v_v.cc",
    "vmv_v_x.cc",
    "vmv_x_s.cc",
    "vmxnor_mm.cc",
    "vmxor_mm.cc",
    "vnclip_wi.cc",
    "vnclip_wv.cc",
    "vnclip_wx.cc",
    "vnclipu_wi.cc",
    "vnclipu_wv.cc",
    "vnclipu_wx.cc",
    "vnmsac_vv.cc",
    "vnmsac_vx.cc",
    "vnmsub_vv.cc",
    "vnmsub_vx.cc",
    "vnsra_wi.cc",
    "vnsra_wv.cc",
    "vnsra_wx.cc",
    "vnsrl_wi.cc",
    "vnsrl_wv.cc",
    "vnsrl_wx.cc",
    "vor_vi.cc",
    "vor_vv.cc",
    "vor_vx.cc",
    "vpopc_m.cc",
    "vqmacc_vv.cc",
    "vqmacc_vx.cc",
    "vqmaccsu_vv.cc",
    "vqmaccsu_vx.cc",
    "vqmaccu_vv.cc",
    "vqmaccu_vx.cc",
    "vqmaccus_vx.cc",
    "vredand_vs.cc",
    "vredmax_vs.cc",
    "vredmaxu_vs.cc",
    "vredmin_vs.cc",
    "vredminu_vs.cc",
    "vredor_vs.cc",
    "vredsum_vs.cc",
    "vredxor_vs.cc",
    "vrem_vv.cc",
    "vrem_vx.cc",
    "vremu_vv.cc",
    "vremu_vx.cc",
    "vrgather_vi.cc",
    "vrgather_vv.cc",
    "vrgather_vx.cc",
    "vrsub_vi.cc",
    "vrsub_vx.cc",
    "vs1r_v.cc",
    "vsadd_vi.cc",
    "vsadd_vv.cc",
    "vsadd_vx.cc",
    "vsaddu_vi.cc",
    "vsaddu_vv.cc",
    "vsaddu_vx.cc",
    "vsbc_vvm.cc",
    "vsbc_vxm.cc",
    "vse16_v.cc",
    "vse32_v.cc",
    "vse64_v.cc",
    "vse8_v.cc",
    "vsetvl.cc",
    "vsetvli.cc",
    "vsext_vf2.cc",
    "vsext_vf4.cc",
    "vsext_vf8.cc",
    "vslide1down_vx.cc",
    "vslide1up_vx.cc",
    "vslidedown_vi.cc",
    "vslidedown_vx.cc",
    "vslideup_vi.cc",
    "vslideup_vx.cc",
    "vsll_vi.cc",
    "vsll_vv.cc",
    "vsll_vx.cc",
    "vsmul_vv.cc",
    "vsmul_vx.cc",
    "vsra_vi.cc",
    "vsra_vv.cc",
    "vsra_vx.cc",
    "vsrl_vi.cc",
    "vsrl_vv.cc",
    "vsrl_vx.cc",
    "vsse16_v.cc",
    "vsse32_v.cc",
    "vsse64_v.cc",
    "vsse8_v.cc",
    "vssra_vi.cc",
    "vssra_vv.cc",
    "vssra_vx.cc",
    "vssrl_vi.cc",
    "vssrl_vv.cc",
    "vssrl_vx.cc",
    "vssub_vv.cc",
    "vssub_vx.cc",
    "vssubu_vv.cc",
    "vssubu_vx.cc",
    "vsub_vv.cc",
    "vsub_vx.cc",
    "vsuxei16_v.cc",
    "vsuxei32_v.cc",
    "vsuxei64_v.cc",
    "vsuxei8_v.cc",
    "vsxei16_v.cc",
    "vsxei32_v.cc",
    "vsxei64_v.cc",
    "vsxei8_v.cc",
    "vwadd_vv.cc",
    "vwadd_vx.cc",
    "vwadd_wv.cc",
    "vwadd_wx.cc",
    "vwaddu_vv.cc",
    "vwaddu_vx.cc",
    "vwaddu_wv.cc",
    "vwaddu_wx.cc",
    "vwmacc_vv.cc",
    "vwmacc_vx.cc",
    "vwmaccsu_vv.cc",
    "vwmaccsu_vx.cc",
    "vwmaccu_vv.cc",
    "vwmaccu_vx.cc",
    "vwmaccus_vx.cc",
    "vwmul_vv.cc",
    "vwmul_vx.cc",
    "vwmulsu_vv.cc",
    "vwmulsu_vx.cc",
    "vwmulu_vv.cc",
    "vwmulu_vx.cc",
    "vwredsum_vs.cc",
    "vwredsumu_vs.cc",
    "vwsub_vv.cc",
    "vwsub_vx.cc",
    "vwsub_wv.cc",
    "vwsub_wx.cc",
    "vwsubu_vv.cc",
    "vwsubu_vx.cc",
    "vwsubu_wv.cc",
    "vwsubu_wx.cc",
    "vxor_vi.cc",
    "vxor_vv.cc",
    "vxor_vx.cc",
    "vzext_vf2.cc",
    "vzext_vf4.cc",
    "vzext_vf8.cc",
    "wfi.cc",
    "xor.cc",
    "xori.cc",
]

INSN_HEADER_FILENAMES = [
    "add.h",
    "addi.h",
    "addiw.h",
    "addw.h",
    "amoadd_d.h",
    "amoadd_w.h",
    "amoand_d.h",
    "amoand_w.h",
    "amomax_d.h",
    "amomax_w.h",
    "amomaxu_d.h",
    "amomaxu_w.h",
    "amomin_d.h",
    "amomin_w.h",
    "amominu_d.h",
    "amominu_w.h",
    "amoor_d.h",
    "amoor_d.h",
    "amoor_w.h",
    "amoswap_d.h",
    "amoswap_w.h",
    "amoxor_d.h",
    "amoxor_w.h",
    "and.h",
    "andi.h",
    "auipc.h",
    "beq.h",
    "bge.h",
    "bgeu.h",
    "blt.h",
    "bltu.h",
    "bne.h",
    "c_add.h",
    "c_addi.h",
    "c_addi4spn.h",
    "c_addw.h",
    "c_and.h",
    "c_andi.h",
    "c_beqz.h",
    "c_bnez.h",
    "c_ebreak.h",
    "c_fld.h",
    "c_fldsp.h",
    "c_flw.h",
    "c_flwsp.h",
    "c_fsd.h",
    "c_fsdsp.h",
    "c_fsw.h",
    "c_fswsp.h",
    "c_j.h",
    "c_jal.h",
    "c_jalr.h",
    "c_jr.h",
    "c_li.h",
    "c_lui.h",
    "c_lui.h",
    "c_lw.h",
    "c_lwsp.h",
    "c_mv.h",
    "c_or.h",
    "c_slli.h",
    "c_srai.h",
    "c_srli.h",
    "c_sub.h",
    "c_subw.h",
    "c_sw.h",
    "c_swsp.h",
    "c_xor.h",
    "csrrc.h",
    "csrrci.h",
    "csrrs.h",
    "csrrsi.h",
    "csrrw.h",
    "csrrwi.h",
    "div.h",
    "divu.h",
    "divuw.h",
    "divw.h",
    "dret.h",
    "ebreak.h",
    "ecall.h",
    "fadd_d.h",
    "fadd_h.h",
    "fadd_q.h",
    "fadd_s.h",
    "fclass_d.h",
    "fclass_h.h",
    "fclass_q.h",
    "fclass_s.h",
    "fcvt_d_h.h",
    "fcvt_d_l.h",
    "fcvt_d_lu.h",
    "fcvt_d_q.h",
    "fcvt_d_s.h",
    "fcvt_d_w.h",
    "fcvt_d_wu.h",
    "fcvt_h_d.h",
    "fcvt_h_l.h",
    "fcvt_h_lu.h",
    "fcvt_h_q.h",
    "fcvt_h_s.h",
    "fcvt_h_w.h",
    "fcvt_h_wu.h",
    "fcvt_l_d.h",
    "fcvt_l_h.h",
    "fcvt_l_q.h",
    "fcvt_l_s.h",
    "fcvt_lu_d.h",
    "fcvt_lu_h.h",
    "fcvt_lu_q.h",
    "fcvt_lu_s.h",
    "fcvt_q_d.h",
    "fcvt_q_h.h",
    "fcvt_q_l.h",
    "fcvt_q_lu.h",
    "fcvt_q_s.h",
    "fcvt_q_w.h",
    "fcvt_q_wu.h",
    "fcvt_s_d.h",
    "fcvt_s_h.h",
    "fcvt_s_l.h",
    "fcvt_s_lu.h",
    "fcvt_s_q.h",
    "fcvt_s_w.h",
    "fcvt_s_wu.h",
    "fcvt_w_d.h",
    "fcvt_w_h.h",
    "fcvt_w_q.h",
    "fcvt_w_s.h",
    "fcvt_wu_d.h",
    "fcvt_wu_h.h",
    "fcvt_wu_q.h",
    "fcvt_wu_s.h",
    "fdiv_d.h",
    "fdiv_h.h",
    "fdiv_q.h",
    "fdiv_s.h",
    "fence.h",
    "fence_i.h",
    "feq_d.h",
    "feq_h.h",
    "feq_q.h",
    "feq_s.h",
    "fld.h",
    "fle_d.h",
    "fle_h.h",
    "fle_q.h",
    "fle_s.h",
    "flh.h",
    "flq.h",
    "flt_d.h",
    "flt_h.h",
    "flt_q.h",
    "flt_s.h",
    "flw.h",
    "fmadd_d.h",
    "fmadd_h.h",
    "fmadd_q.h",
    "fmadd_s.h",
    "fmax_d.h",
    "fmax_h.h",
    "fmax_q.h",
    "fmax_s.h",
    "fmin_d.h",
    "fmin_h.h",
    "fmin_q.h",
    "fmin_s.h",
    "fmsub_d.h",
    "fmsub_h.h",
    "fmsub_q.h",
    "fmsub_s.h",
    "fmul_d.h",
    "fmul_h.h",
    "fmul_q.h",
    "fmul_s.h",
    "fmv_d_x.h",
    "fmv_h_x.h",
    "fmv_w_x.h",
    "fmv_x_d.h",
    "fmv_x_h.h",
    "fmv_x_w.h",
    "fnmadd_d.h",
    "fnmadd_h.h",
    "fnmadd_q.h",
    "fnmadd_s.h",
    "fnmsub_d.h",
    "fnmsub_h.h",
    "fnmsub_q.h",
    "fnmsub_s.h",
    "fsd.h",
    "fsgnj_d.h",
    "fsgnj_h.h",
    "fsgnj_q.h",
    "fsgnj_s.h",
    "fsgnjn_d.h",
    "fsgnjn_h.h",
    "fsgnjn_q.h",
    "fsgnjn_s.h",
    "fsgnjx_d.h",
    "fsgnjx_h.h",
    "fsgnjx_q.h",
    "fsgnjx_s.h",
    "fsh.h",
    "fsq.h",
    "fsqrt_d.h",
    "fsqrt_h.h",
    "fsqrt_q.h",
    "fsqrt_s.h",
    "fsub_d.h",
    "fsub_h.h",
    "fsub_q.h",
    "fsub_s.h",
    "fsw.h",
    "jal.h",
    "jalr.h",
    "lb.h",
    "lbu.h",
    "ld.h",
    "lh.h",
    "lhu.h",
    "lr_d.h",
    "lr_w.h",
    "lui.h",
    "lw.h",
    "lwu.h",
    "mret.h",
    "mul.h",
    "mulh.h",
    "mulhsu.h",
    "mulhu.h",
    "mulw.h",
    "or.h",
    "ori.h",
    "rem.h",
    "remu.h",
    "remuw.h",
    "remw.h",
    "sb.h",
    "sc_d.h",
    "sc_w.h",
    "sd.h",
    "sfence_vma.h",
    "sh.h",
    "sll.h",
    "slli.h",
    "slliw.h",
    "sllw.h",
    "slt.h",
    "slti.h",
    "sltiu.h",
    "sltu.h",
    "sra.h",
    "srai.h",
    "sraiw.h",
    "sraw.h",
    "sret.h",
    "srl.h",
    "srli.h",
    "srliw.h",
    "srlw.h",
    "sub.h",
    "subw.h",
    "sw.h",
    "vaadd_vv.h",
    "vaadd_vx.h",
    "vaaddu_vv.h",
    "vaaddu_vx.h",
    "vadc_vim.h",
    "vadc_vvm.h",
    "vadc_vxm.h",
    "vadd_vi.h",
    "vadd_vv.h",
    "vadd_vx.h",
    "vamoadde16_v.h",
    "vamoadde32_v.h",
    "vamoadde64_v.h",
    "vamoadde8_v.h",
    "vamoande16_v.h",
    "vamoande32_v.h",
    "vamoande64_v.h",
    "vamoande8_v.h",
    "vamomaxe16_v.h",
    "vamomaxe32_v.h",
    "vamomaxe64_v.h",
    "vamomaxe8_v.h",
    "vamomaxue16_v.h",
    "vamomaxue32_v.h",
    "vamomaxue64_v.h",
    "vamomaxue8_v.h",
    "vamomine16_v.h",
    "vamomine32_v.h",
    "vamomine64_v.h",
    "vamomine8_v.h",
    "vamominue16_v.h",
    "vamominue32_v.h",
    "vamominue64_v.h",
    "vamominue8_v.h",
    "vamoore16_v.h",
    "vamoore32_v.h",
    "vamoore64_v.h",
    "vamoore8_v.h",
    "vamoswape16_v.h",
    "vamoswape32_v.h",
    "vamoswape64_v.h",
    "vamoswape8_v.h",
    "vamoxore16_v.h",
    "vamoxore32_v.h",
    "vamoxore64_v.h",
    "vamoxore8_v.h",
    "vand_vi.h",
    "vand_vv.h",
    "vand_vx.h",
    "vasub_vv.h",
    "vasub_vx.h",
    "vasubu_vv.h",
    "vasubu_vx.h",
    "vcompress_vm.h",
    "vdiv_vv.h",
    "vdiv_vx.h",
    "vdivu_vv.h",
    "vdivu_vx.h",
    "vdot_vv.h",
    "vdotu_vv.h",
    "vfadd_vf.h",
    "vfadd_vv.h",
    "vfclass_v.h",
    "vfcvt_f_x_v.h",
    "vfcvt_f_xu_v.h",
    "vfcvt_rtz_x_f_v.h",
    "vfcvt_rtz_xu_f_v.h",
    "vfcvt_x_f_v.h",
    "vfcvt_xu_f_v.h",
    "vfdiv_vf.h",
    "vfdiv_vv.h",
    "vfdot_vv.h",
    "vfirst_m.h",
    "vfmacc_vf.h",
    "vfmacc_vv.h",
    "vfmadd_vf.h",
    "vfmadd_vv.h",
    "vfmax_vf.h",
    "vfmax_vv.h",
    "vfmerge_vfm.h",
    "vfmin_vf.h",
    "vfmin_vv.h",
    "vfmsac_vf.h",
    "vfmsac_vv.h",
    "vfmsub_vf.h",
    "vfmsub_vv.h",
    "vfmul_vf.h",
    "vfmul_vv.h",
    "vfmv_f_s.h",
    "vfmv_s_f.h",
    "vfmv_v_f.h",
    "vfncvt_f_f_w.h",
    "vfncvt_f_x_w.h",
    "vfncvt_f_xu_w.h",
    "vfncvt_rod_f_f_w.h",
    "vfncvt_rtz_x_f_w.h",
    "vfncvt_rtz_xu_f_w.h",
    "vfncvt_x_f_w.h",
    "vfncvt_xu_f_w.h",
    "vfnmacc_vf.h",
    "vfnmacc_vv.h",
    "vfnmadd_vf.h",
    "vfnmadd_vv.h",
    "vfnmsac_vf.h",
    "vfnmsac_vv.h",
    "vfnmsub_vf.h",
    "vfnmsub_vv.h",
    "vfrdiv_vf.h",
    "vfredmax_vs.h",
    "vfredmin_vs.h",
    "vfredosum_vs.h",
    "vfredsum_vs.h",
    "vfrsub_vf.h",
    "vfsgnj_vf.h",
    "vfsgnj_vv.h",
    "vfsgnjn_vf.h",
    "vfsgnjn_vv.h",
    "vfsgnjx_vf.h",
    "vfsgnjx_vv.h",
    "vfslide1down_vf.h",
    "vfslide1up_vf.h",
    "vfsqrt_v.h",
    "vfsub_vf.h",
    "vfsub_vv.h",
    "vfwadd_vf.h",
    "vfwadd_vv.h",
    "vfwadd_wf.h",
    "vfwadd_wv.h",
    "vfwcvt_f_f_v.h",
    "vfwcvt_f_x_v.h",
    "vfwcvt_f_xu_v.h",
    "vfwcvt_rtz_x_f_v.h",
    "vfwcvt_rtz_xu_f_v.h",
    "vfwcvt_x_f_v.h",
    "vfwcvt_xu_f_v.h",
    "vfwmacc_vf.h",
    "vfwmacc_vv.h",
    "vfwmsac_vf.h",
    "vfwmsac_vv.h",
    "vfwmul_vf.h",
    "vfwmul_vv.h",
    "vfwnmacc_vf.h",
    "vfwnmacc_vv.h",
    "vfwnmsac_vf.h",
    "vfwnmsac_vv.h",
    "vfwredosum_vs.h",
    "vfwredsum_vs.h",
    "vfwsub_vf.h",
    "vfwsub_vv.h",
    "vfwsub_wf.h",
    "vfwsub_wv.h",
    "vid_v.h",
    "viota_m.h",
    "vl1r_v.h",
    "vle16_v.h",
    "vle16ff_v.h",
    "vle32_v.h",
    "vle32ff_v.h",
    "vle64_v.h",
    "vle64ff_v.h",
    "vle8_v.h",
    "vle8ff_v.h",
    "vlse16_v.h",
    "vlse32_v.h",
    "vlse64_v.h",
    "vlse8_v.h",
    "vlxei16_v.h",
    "vlxei32_v.h",
    "vlxei64_v.h",
    "vlxei8_v.h",
    "vmacc_vv.h",
    "vmacc_vx.h",
    "vmadc_vim.h",
    "vmadc_vvm.h",
    "vmadc_vxm.h",
    "vmadd_vv.h",
    "vmadd_vx.h",
    "vmand_mm.h",
    "vmandnot_mm.h",
    "vmax_vv.h",
    "vmax_vx.h",
    "vmaxu_vv.h",
    "vmaxu_vx.h",
    "vmerge_vim.h",
    "vmerge_vvm.h",
    "vmerge_vxm.h",
    "vmfeq_vf.h",
    "vmfeq_vv.h",
    "vmfge_vf.h",
    "vmfgt_vf.h",
    "vmfle_vf.h",
    "vmfle_vv.h",
    "vmflt_vf.h",
    "vmflt_vv.h",
    "vmfne_vf.h",
    "vmfne_vv.h",
    "vmin_vv.h",
    "vmin_vx.h",
    "vminu_vv.h",
    "vminu_vx.h",
    "vmnand_mm.h",
    "vmnor_mm.h",
    "vmor_mm.h",
    "vmornot_mm.h",
    "vmsbc_vvm.h",
    "vmsbc_vxm.h",
    "vmsbf_m.h",
    "vmseq_vi.h",
    "vmseq_vv.h",
    "vmseq_vx.h",
    "vmsgt_vi.h",
    "vmsgt_vx.h",
    "vmsgtu_vi.h",
    "vmsgtu_vx.h",
    "vmsif_m.h",
    "vmsle_vi.h",
    "vmsle_vv.h",
    "vmsle_vx.h",
    "vmsleu_vi.h",
    "vmsleu_vv.h",
    "vmsleu_vx.h",
    "vmslt_vv.h",
    "vmslt_vx.h",
    "vmsltu_vv.h",
    "vmsltu_vx.h",
    "vmsne_vi.h",
    "vmsne_vv.h",
    "vmsne_vx.h",
    "vmsof_m.h",
    "vmul_vv.h",
    "vmul_vx.h",
    "vmulh_vv.h",
    "vmulh_vx.h",
    "vmulhsu_vv.h",
    "vmulhsu_vx.h",
    "vmulhu_vv.h",
    "vmulhu_vx.h",
    "vmv1r_v.h",
    "vmv2r_v.h",
    "vmv4r_v.h",
    "vmv8r_v.h",
    "vmv_s_x.h",
    "vmv_v_i.h",
    "vmv_v_v.h",
    "vmv_v_x.h",
    "vmv_x_s.h",
    "vmvnfr_v.h",
    "vmxnor_mm.h",
    "vmxor_mm.h",
    "vnclip_wi.h",
    "vnclip_wv.h",
    "vnclip_wx.h",
    "vnclipu_wi.h",
    "vnclipu_wv.h",
    "vnclipu_wx.h",
    "vnmsac_vv.h",
    "vnmsac_vx.h",
    "vnmsub_vv.h",
    "vnmsub_vx.h",
    "vnsra_wi.h",
    "vnsra_wv.h",
    "vnsra_wx.h",
    "vnsrl_wi.h",
    "vnsrl_wv.h",
    "vnsrl_wx.h",
    "vor_vi.h",
    "vor_vv.h",
    "vor_vx.h",
    "vpopc_m.h",
    "vqmacc_vv.h",
    "vqmacc_vx.h",
    "vqmaccsu_vv.h",
    "vqmaccsu_vx.h",
    "vqmaccu_vv.h",
    "vqmaccu_vx.h",
    "vqmaccus_vx.h",
    "vredand_vs.h",
    "vredmax_vs.h",
    "vredmaxu_vs.h",
    "vredmin_vs.h",
    "vredminu_vs.h",
    "vredor_vs.h",
    "vredsum_vs.h",
    "vredxor_vs.h",
    "vrem_vv.h",
    "vrem_vx.h",
    "vremu_vv.h",
    "vremu_vx.h",
    "vrgather_vi.h",
    "vrgather_vv.h",
    "vrgather_vx.h",
    "vrsub_vi.h",
    "vrsub_vx.h",
    "vs1r_v.h",
    "vsadd_vi.h",
    "vsadd_vv.h",
    "vsadd_vx.h",
    "vsaddu_vi.h",
    "vsaddu_vv.h",
    "vsaddu_vx.h",
    "vsbc_vvm.h",
    "vsbc_vxm.h",
    "vse16_v.h",
    "vse32_v.h",
    "vse64_v.h",
    "vse8_v.h",
    "vsetvl.h",
    "vsetvli.h",
    "vsext_vf2.h",
    "vsext_vf4.h",
    "vsext_vf8.h",
    "vslide1down_vx.h",
    "vslide1up_vx.h",
    "vslidedown_vi.h",
    "vslidedown_vx.h",
    "vslideup_vi.h",
    "vslideup_vx.h",
    "vsll_vi.h",
    "vsll_vv.h",
    "vsll_vx.h",
    "vsmul_vv.h",
    "vsmul_vx.h",
    "vsra_vi.h",
    "vsra_vv.h",
    "vsra_vx.h",
    "vsrl_vi.h",
    "vsrl_vv.h",
    "vsrl_vx.h",
    "vsse16_v.h",
    "vsse32_v.h",
    "vsse64_v.h",
    "vsse8_v.h",
    "vssra_vi.h",
    "vssra_vv.h",
    "vssra_vx.h",
    "vssrl_vi.h",
    "vssrl_vv.h",
    "vssrl_vx.h",
    "vssub_vv.h",
    "vssub_vx.h",
    "vssubu_vv.h",
    "vssubu_vx.h",
    "vsub_vv.h",
    "vsub_vx.h",
    "vsuxei16_v.h",
    "vsuxei32_v.h",
    "vsuxei64_v.h",
    "vsuxei8_v.h",
    "vsxei16_v.h",
    "vsxei32_v.h",
    "vsxei64_v.h",
    "vsxei8_v.h",
    "vwadd_vv.h",
    "vwadd_vx.h",
    "vwadd_wv.h",
    "vwadd_wx.h",
    "vwaddu_vv.h",
    "vwaddu_vx.h",
    "vwaddu_wv.h",
    "vwaddu_wx.h",
    "vwmacc_vv.h",
    "vwmacc_vx.h",
    "vwmaccsu_vv.h",
    "vwmaccsu_vx.h",
    "vwmaccu_vv.h",
    "vwmaccu_vx.h",
    "vwmaccus_vx.h",
    "vwmul_vv.h",
    "vwmul_vx.h",
    "vwmulsu_vv.h",
    "vwmulsu_vx.h",
    "vwmulu_vv.h",
    "vwmulu_vx.h",
    "vwredsum_vs.h",
    "vwredsumu_vs.h",
    "vwsub_vv.h",
    "vwsub_vx.h",
    "vwsub_wv.h",
    "vwsub_wx.h",
    "vwsubu_vv.h",
    "vwsubu_vx.h",
    "vwsubu_wv.h",
    "vwsubu_wx.h",
    "vxor_vi.h",
    "vxor_vv.h",
    "vxor_vx.h",
    "vzext_vf2.h",
    "vzext_vf4.h",
    "vzext_vf8.h",
    "wfi.h",
    "xor.h",
    "xori.h",
]

# These are all to be renamed as cc files during copying
SOFTFLOAT_SOURCE_FILENAMES = [
    "f128_add.c",
    "f128_classify.c",
    "f128_div.c",
    "f128_eq.c",
    "f128_eq_signaling.c",
    "f128_isSignalingNaN.c",
    "f128_le.c",
    "f128_le_quiet.c",
    "f128_lt.c",
    "f128_lt_quiet.c",
    "f128_mul.c",
    "f128_mulAdd.c",
    "f128_rem.c",
    "f128_roundToInt.c",
    "f128_sqrt.c",
    "f128_sub.c",
    "f128_to_f16.c",
    "f128_to_f32.c",
    "f128_to_f64.c",
    "f128_to_i32.c",
    "f128_to_i32_r_minMag.c",
    "f128_to_i64.c",
    "f128_to_i64_r_minMag.c",
    "f128_to_ui32.c",
    "f128_to_ui32_r_minMag.c",
    "f128_to_ui64.c",
    "f128_to_ui64_r_minMag.c",
    "f16_add.c",
    "f16_classify.c",
    "f16_div.c",
    "f16_eq.c",
    "f16_eq_signaling.c",
    "f16_isSignalingNaN.c",
    "f16_le.c",
    "f16_le_quiet.c",
    "f16_lt.c",
    "f16_lt_quiet.c",
    "f16_mul.c",
    "f16_mulAdd.c",
    "f16_rem.c",
    "f16_roundToInt.c",
    "f16_sqrt.c",
    "f16_sub.c",
    "f16_to_f128.c",
    "f16_to_f32.c",
    "f16_to_f64.c",
    "f16_to_i16.c",
    "f16_to_i32.c",
    "f16_to_i32_r_minMag.c",
    "f16_to_i64.c",
    "f16_to_i64_r_minMag.c",
    "f16_to_i8.c",
    "f16_to_ui16.c",
    "f16_to_ui32.c",
    "f16_to_ui32_r_minMag.c",
    "f16_to_ui64.c",
    "f16_to_ui64_r_minMag.c",
    "f16_to_ui8.c",
    "f32_add.c",
    "f32_classify.c",
    "f32_div.c",
    "f32_eq.c",
    "f32_eq_signaling.c",
    "f32_isSignalingNaN.c",
    "f32_le.c",
    "f32_le_quiet.c",
    "f32_lt.c",
    "f32_lt_quiet.c",
    "f32_mul.c",
    "f32_mulAdd.c",
    "f32_rem.c",
    "f32_roundToInt.c",
    "f32_sqrt.c",
    "f32_sub.c",
    "f32_to_f128.c",
    "f32_to_f16.c",
    "f32_to_f64.c",
    "f32_to_i16.c",
    "f32_to_i32.c",
    "f32_to_i32_r_minMag.c",
    "f32_to_i64.c",
    "f32_to_i64_r_minMag.c",
    "f32_to_ui16.c",
    "f32_to_ui32.c",
    "f32_to_ui32_r_minMag.c",
    "f32_to_ui64.c",
    "f32_to_ui64_r_minMag.c",
    "f64_add.c",
    "f64_classify.c",
    "f64_div.c",
    "f64_eq.c",
    "f64_eq_signaling.c",
    "f64_isSignalingNaN.c",
    "f64_le.c",
    "f64_le_quiet.c",
    "f64_lt.c",
    "f64_lt_quiet.c",
    "f64_mul.c",
    "f64_mulAdd.c",
    "f64_rem.c",
    "f64_roundToInt.c",
    "f64_sqrt.c",
    "f64_sub.c",
    "f64_to_f128.c",
    "f64_to_f16.c",
    "f64_to_f32.c",
    "f64_to_i32.c",
    "f64_to_i32_r_minMag.c",
    "f64_to_i64.c",
    "f64_to_i64_r_minMag.c",
    "f64_to_ui32.c",
    "f64_to_ui32_r_minMag.c",
    "f64_to_ui64.c",
    "f64_to_ui64_r_minMag.c",
    "fall_maxmin.c",
    "i32_to_f128.c",
    "i32_to_f16.c",
    "i32_to_f32.c",
    "i32_to_f64.c",
    "i64_to_f128.c",
    "i64_to_f16.c",
    "i64_to_f32.c",
    "i64_to_f64.c",
    "s_add128.c",
    "s_add256M.c",
    "s_addCarryM.c",
    "s_addComplCarryM.c",
    "s_addM.c",
    "s_addMagsF128.c",
    "s_addMagsF16.c",
    "s_addMagsF32.c",
    "s_addMagsF64.c",
    "s_approxRecip32_1.c",
    "s_approxRecip_1Ks.c",
    "s_approxRecipSqrt32_1.c",
    "s_approxRecipSqrt_1Ks.c",
    "s_commonNaNToF128UI.c",
    "s_commonNaNToF16UI.c",
    "s_commonNaNToF32UI.c",
    "s_commonNaNToF64UI.c",
    "s_compare128M.c",
    "s_compare96M.c",
    "s_countLeadingZeros16.c",
    "s_countLeadingZeros32.c",
    "s_countLeadingZeros64.c",
    "s_countLeadingZeros8.c",
    "s_eq128.c",
    "s_f128UIToCommonNaN.c",
    "s_f16UIToCommonNaN.c",
    "s_f32UIToCommonNaN.c",
    "s_f64UIToCommonNaN.c",
    "s_le128.c",
    "s_lt128.c",
    "s_mul128By32.c",
    "s_mul128MTo256M.c",
    "s_mul128To256M.c",
    "s_mul64ByShifted32To128.c",
    "s_mul64To128.c",
    "s_mul64To128M.c",
    "s_mulAddF128.c",
    "s_mulAddF16.c",
    "s_mulAddF32.c",
    "s_mulAddF64.c",
    "s_negXM.c",
    "s_normRoundPackToF128.c",
    "s_normRoundPackToF16.c",
    "s_normRoundPackToF32.c",
    "s_normRoundPackToF64.c",
    "s_normSubnormalF128Sig.c",
    "s_normSubnormalF16Sig.c",
    "s_normSubnormalF32Sig.c",
    "s_normSubnormalF64Sig.c",
    "s_propagateNaNF128UI.c",
    "s_propagateNaNF16UI.c",
    "s_propagateNaNF32UI.c",
    "s_propagateNaNF64UI.c",
    "s_remStepMBy32.c",
    "s_roundMToI64.c",
    "s_roundMToUI64.c",
    "s_roundPackMToI64.c",
    "s_roundPackMToUI64.c",
    "s_roundPackToF128.c",
    "s_roundPackToF16.c",
    "s_roundPackToF32.c",
    "s_roundPackToF64.c",
    "s_roundPackToI32.c",
    "s_roundPackToI64.c",
    "s_roundPackToUI32.c",
    "s_roundPackToUI64.c",
    "s_roundToI32.c",
    "s_roundToI64.c",
    "s_roundToUI32.c",
    "s_roundToUI64.c",
    "s_shiftRightJam128.c",
    "s_shiftRightJam128Extra.c",
    "s_shiftRightJam256M.c",
    "s_shiftRightJam32.c",
    "s_shiftRightJam64.c",
    "s_shiftRightJam64Extra.c",
    "s_shortShiftLeft128.c",
    "s_shortShiftLeft64To96M.c",
    "s_shortShiftRight128.c",
    "s_shortShiftRightExtendM.c",
    "s_shortShiftRightJam128.c",
    "s_shortShiftRightJam128Extra.c",
    "s_shortShiftRightJam64.c",
    "s_shortShiftRightJam64Extra.c",
    "s_shortShiftRightM.c",
    "s_sub128.c",
    "s_sub1XM.c",
    "s_sub256M.c",
    "s_subM.c",
    "s_subMagsF128.c",
    "s_subMagsF16.c",
    "s_subMagsF32.c",
    "s_subMagsF64.c",
    "softfloat_raiseFlags.c",
    "softfloat_state.c",
    "ui32_to_f128.c",
    "ui32_to_f16.c",
    "ui32_to_f32.c",
    "ui32_to_f64.c",
    "ui64_to_f128.c",
    "ui64_to_f16.c",
    "ui64_to_f32.c",
    "ui64_to_f64.c",
]

SOFTFLOAT_HEADER_FILENAMES = [
    "internals.h",
    "platform.h",
    "primitiveTypes.h",
    "softfloat_types.h",
]

SPIKE_SOURCE_FILENAMES = [
    "fesvr/option_parser.cc",
    "riscv/cachesim.cc",
    "riscv/execute.cc",
    "riscv/extension.cc",
    "riscv/extensions.cc",
    "riscv/trap.cc",
]

SPIKE_HEADER_FILENAMES = [
    "fesvr/elf.h",
    "fesvr/option_parser.h",
    "icache.h",
    "insn_list.h",
    "riscv/arith.h",
    "riscv/byteorder.h",
    "riscv/cachesim.h",
    "riscv/common.h",
    "riscv/encoding.h",
    "riscv/extension.h",
    "riscv/insn_template.h",
    "riscv/memtracer.h",
    "riscv/mmu.h",
    "riscv/opcodes.h",
    "riscv/simif.h",
    "riscv/tracer.h",
    "riscv/trap.h",
]

# All these ones need to be turned into patch operations rather than file
# replacements to the extent possible
REPLACEMENT_SOURCE_FILENAMES = [
    "disasm.cc",
    "execute.cc",
    "mmu.cc",
    "processor.cc",
    "regnames.cc",
    "simlib.cc",
]
REPLACEMENT_HEADER_FILENAMES = [
    "config.h",
    "decode.h",
    "devices.h",
    "disasm.h",
    "mmu.h",
    "primitives.h",
    "processor.h",
    "simif.h",
    "simlib.h",
    "specialize.h",
]
REPLACEMENT_INSN_HEADER_FILENAMES = ["mret.h", "sret.h"]
GLOB_REPLACEMENT_INSN_HEADER_FILENAMES = ["insns/*.h"]


def printout(string):
    if NOISY:
        print(string)


def makedir(path):
    try:
        os.mkdir(path)
    except OSError as exc:
        if not exc.errno == errno.EEXIST or not os.path.isdir(path):
            raise


def is_first_file_newer(file1, file2):
    """If file2 is older than file1, or does not exist, return True"""
    try:
        file1_ts = os.stat(file1).st_mtime
    except FileNotFoundError as exc:
        print("source file1, %s, not found" % file1)
        raise exc
    try:
        file2_ts = os.stat(file2).st_mtime
    except FileNotFoundError:
        # printout('target file2, %s, not found' % file2)
        return True
    if file1_ts > file2_ts:
        return True
    else:
        printout("skip copy of %s to %s due to timestamp" % (file1, file2))
    return False


def copy(src, dest):
    if is_first_file_newer(src, dest):
        printout("Copying %s to %s" % (src, dest))
        shutil.copy2(src, dest)
    else:
        printout("Skipping copying %s to %s" % (src, dest))


def copy_files(prefix_path_string, filenames_list, destination_dir):
    printout("\nCopying specific files from: %s to %s" % (prefix_path_string, destination_dir))

    for filename in filenames_list:
        # Take all the c code and label it as c++ code
        src = prefix_path_string + "/" + filename
        dest = destination_dir + "/" + os.path.basename(filename)

        if dest.endswith(".c"):
            dest += "c"

        copy(src, dest)


def main():
    printout(
        "###\n### Copying original Spike files and then modifying them. "
        "Output will be in src and inc directories.\n###"
    )

    copy_files(ORIGINAL_SOURCE_DIR, SPIKE_SOURCE_FILENAMES, SRC)
    copy_files(ORIGINAL_SOURCE_DIR, SPIKE_HEADER_FILENAMES, INC)
    copy_files(ORIGINAL_INSNS_DIR, INSN_SOURCE_FILENAMES, SRC)
    copy_files(ORIGINAL_SOFTFLOAT_DIR, SOFTFLOAT_SOURCE_FILENAMES, SRC)
    copy_files(ORIGINAL_SOFTFLOAT_DIR, SOFTFLOAT_HEADER_FILENAMES, INC)
    copy_files(REPLACEMENTS_DIR, REPLACEMENT_SOURCE_FILENAMES, SRC)
    copy_files(REPLACEMENTS_DIR, REPLACEMENT_HEADER_FILENAMES, INC)

    makedir(INC_INSNS)
    copy_files(ORIGINAL_INSN_HEADERS_DIR, INSN_HEADER_FILENAMES, INC_INSNS)
    copy_files(REPLACEMENTS_DIR, REPLACEMENT_INSN_HEADER_FILENAMES, INC_INSNS)
    for src in glob.glob(str(REPLACEMENTS_DIR + "/insns/*.h")):
        dest = "./inc/insns/" + os.path.basename(src)
        copy(src, dest)

    makedir("./inc/fesvr")
    copy("inc/option_parser.h", "inc/fesvr/option_parser.h")


if __name__ == "__main__":
    main()
