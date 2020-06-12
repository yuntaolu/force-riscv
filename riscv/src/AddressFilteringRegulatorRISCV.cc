//
// Copyright (C) [2020] Futurewei Technologies, Inc.
//
// FORCE-RISCV is licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR
// FIT FOR A PARTICULAR PURPOSE.
// See the License for the specific language governing permissions and
// limitations under the License.
//
#include <AddressFilteringRegulatorRISCV.h>
#include <VmConstraint.h>
#include <Constraint.h>
#include <GenRequest.h>
#include <VmMapper.h>
#include <Log.h>

/*!
  \file AddressFilteringRegulatorRISCV.cc
  \brief AddressFilteringRegulator RISCV layer code.
*/

using namespace std;

namespace Force {

  AddressFilteringRegulatorRISCV::AddressFilteringRegulatorRISCV()
    : AddressFilteringRegulator()
  {

  }

  AddressFilteringRegulatorRISCV::AddressFilteringRegulatorRISCV(const AddressFilteringRegulatorRISCV& rOther)
    : AddressFilteringRegulator(rOther)
  {

  }

  AddressFilteringRegulatorRISCV::~AddressFilteringRegulatorRISCV()
  {

  }

  Object* AddressFilteringRegulatorRISCV::Clone() const
  {
    return new AddressFilteringRegulatorRISCV(*this);
  }

  void AddressFilteringRegulatorRISCV::Setup(const Generator* pGen)
  {
    AddressFilteringRegulator::Setup(pGen);
  }

  void AddressFilteringRegulatorRISCV::GetInstrVmConstraints(const GenPageRequest& rPageReq, const VmMapper& rVmMapper, vector<VmConstraint* >& rVmConstraints) const
  {
    const map<EPagingExceptionType, EExceptionConstraintType>& excep_constraints = rPageReq.GetExceptionConstraints();

    for (auto vm_constr_item : excep_constraints)
    {
      switch (vm_constr_item.first)
      {
        case EPagingExceptionType::InstructionAccessFault:
          GetInstrAccessVmConstraints(rPageReq, rVmMapper, rVmConstraints, vm_constr_item.second);
          break;
        case EPagingExceptionType::InstructionPageFault:
          GetInstrPageFaultVmConstraints(rPageReq, rVmMapper, rVmConstraints, vm_constr_item.second);
          break;
        default:
          break;
      }
    }
  }

  void AddressFilteringRegulatorRISCV::GetDataVmConstraints(const GenPageRequest& rPageReq, const VmMapper& rVmMapper, vector<VmConstraint* >& rVmConstraints) const
  {
    const map<EPagingExceptionType, EExceptionConstraintType>& excep_constraints = rPageReq.GetExceptionConstraints();

    for (auto vm_constr_item : excep_constraints)
    {
      switch (vm_constr_item.first)
      {
        case EPagingExceptionType::LoadAccessFault:
        case EPagingExceptionType::StoreAmoAccessFault:
          GetDataAccessVmConstraints(rPageReq, rVmMapper, rVmConstraints, vm_constr_item.second);
          break;
        case EPagingExceptionType::LoadPageFault:
        case EPagingExceptionType::StoreAmoPageFault:
          GetDataPageFaultVmConstraints(rPageReq, rVmMapper, rVmConstraints, vm_constr_item.second);
          break;
        default:
          break;
      }
    }
  }

  void AddressFilteringRegulatorRISCV::GetInstrAccessVmConstraints(const GenPageRequest& rPageReq, const VmMapper& rVmMapper, vector<VmConstraint* >& rVmConstraints, EExceptionConstraintType permConstrType) const
  {
    switch (permConstrType)
    {
      case EExceptionConstraintType::PreventHard:
        {
          bool privileged = false;
          rPageReq.GetGenBoolAttribute(EPageGenBoolAttrType::Privileged, privileged);
          if (privileged)
          {
            const ConstraintSet* vm_constr = rVmMapper.GetVmConstraint(EVmConstraintType::PrivilegedNoExecute);
            if (vm_constr != nullptr)
            {
              rVmConstraints.push_back(new VmNotInConstraint(EVmConstraintType::PrivilegedNoExecute, vm_constr));
            }
          }
        }
        break;
      default:
        // TODO implement other exception constraint types
        break;
    }
  }

  void AddressFilteringRegulatorRISCV::GetInstrPageFaultVmConstraints(const GenPageRequest& rPageReq, const VmMapper& rVmMapper, vector<VmConstraint* >& rVmConstraints, EExceptionConstraintType constrType) const
  {
    switch (constrType)
    {
      case EExceptionConstraintType::PreventHard:
        {
          const ConstraintSet* vm_constr = rVmMapper.GetVmConstraint(EVmConstraintType::PageFault);
          if (vm_constr != nullptr)
          {
            rVmConstraints.push_back(new VmNotInConstraint(EVmConstraintType::PageFault, vm_constr));
          }
        }
        break;
      default:
        // TODO implement other exception constraint types
        break;
    }
  }




  void AddressFilteringRegulatorRISCV::GetDataAccessVmConstraints(const GenPageRequest& rPageReq, const VmMapper& rVmMapper, vector<VmConstraint* >& rVmConstraints, EExceptionConstraintType permConstrType) const
  {
    switch (permConstrType)
    {
      case EExceptionConstraintType::PreventHard:
        {
          if (rPageReq.PrivilegeLevelSpecified() && (rPageReq.PrivilegeLevel() == EPrivilegeLevelType::U))
          {
            const ConstraintSet* vm_constr = rVmMapper.GetVmConstraint(EVmConstraintType::NoUserAccess);
            if (vm_constr != nullptr)
            {
              rVmConstraints.push_back(new VmNotInConstraint(EVmConstraintType::NoUserAccess, vm_constr));
            }
          }
          else
          {
            const ConstraintSet* vm_constr = rVmMapper.GetVmConstraint(EVmConstraintType::UserAccess);
            if (vm_constr != nullptr)
            {
              rVmConstraints.push_back(new VmNotInConstraint(EVmConstraintType::UserAccess, vm_constr));
            }
          }

          auto mem_access = rPageReq.MemoryAccessType();
          if (EMemAccessTypeBaseType(mem_access) & EMemAccessTypeBaseType(EMemAccessType::Write))
          {
            const ConstraintSet* vm_constr = rVmMapper.GetVmConstraint(EVmConstraintType::ReadOnly);
            if (vm_constr != nullptr)
            {
              rVmConstraints.push_back(new VmNotInConstraint(EVmConstraintType::ReadOnly, vm_constr));
            }
          }
        }
        break;
      default:
        // TODO implement other exception constraint types
        break;
    }
  }

  //TODO determine if non-atomic constr is populated/needed for RISCV
      /*{
        bool atomic = false;
        rPageReq.GetGenBoolAttribute(EPageGenBoolAttrType::Atomic, atomic);
        if (atomic) {
          const ConstraintSet* vm_constr = rVmMapper.GetVmConstraint(EVmConstraintType::NonAtomic);
          if (vm_constr != nullptr) {
            rVmConstraints.push_back(new VmNotInConstraint(EVmConstraintType::NonAtomic, vm_constr));
          }
        }
      }*/

  void AddressFilteringRegulatorRISCV::GetDataPageFaultVmConstraints(const GenPageRequest& rPageReq, const VmMapper& rVmMapper, vector<VmConstraint* >& rVmConstraints, EExceptionConstraintType constrType) const
  {
    switch (constrType)
    {
      case EExceptionConstraintType::PreventHard:
        {
          const ConstraintSet* vm_constr = rVmMapper.GetVmConstraint(EVmConstraintType::PageFault);
          if (vm_constr != nullptr)
          {
            rVmConstraints.push_back(new VmNotInConstraint(EVmConstraintType::PageFault, vm_constr));
          }
        }
        break;
      default:
        // TODO implement other exception constraint types
        break;
    }
  }

}
