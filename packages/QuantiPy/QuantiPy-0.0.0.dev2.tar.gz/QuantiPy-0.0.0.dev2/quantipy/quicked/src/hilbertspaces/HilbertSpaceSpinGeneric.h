/** @file HilbertSpaceSpinGeneric.h
 *  @brief Template Specialization for Generic Spin Hilbertspaces
 *  @author Alexander Wietek  
 */

#ifndef __QUICKED_HILBERTSPACES_HILBERTSPACESPINGENERIC_H__
#define __QUICKED_HILBERTSPACES_HILBERTSPACESPINGENERIC_H__

#include "HilbertSpace.h"
#include "HilbertSpaceSpinGenericDetail.h"
#include "BasisState.h"

namespace quicked
{

  template <hilbert_t THilbertSpace, uint32 SPIN> // SPIN = 2S +1
  class HilbertSpaceSpinGenericBase : public HilbertSpaceBase<THilbertSpace>
  {
  public:
    typedef HilbertSpaceSpinGenericDetail::iterator<THilbertSpace, SPIN> iterator;
    using typename HilbertSpaceBase<THilbertSpace>::qn_t;
    using typename HilbertSpaceBase<THilbertSpace>::state_t;

    HilbertSpaceSpinGenericBase(const uint32& _n_sites,
				const qn_t& _quantumnumber)
      : HilbertSpaceBase<THilbertSpace>(_n_sites, 0),
      quantumnumber_(_quantumnumber),
      begin_(iterator(_quantumnumber.val, _n_sites, 0)),
      end_(iterator(_quantumnumber.val, _n_sites, -1))
    {
      assert(valid_quantumnumber<THilbertSpace>(quantumnumber_, _n_sites));
    }
    inline qn_t quantumnumber() const {return quantumnumber_;} 
    inline const iterator& begin() const { return begin_; }
    inline const iterator& end() const { return end_;}
    
  private:
    const qn_t quantumnumber_;
    const iterator begin_;
    const iterator end_;
    
  };

  template <>
  class HilbertSpace<HILBERTSPACE_SPIN_HALF_GEN_TYPE> :
    public HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_HALF_GEN_TYPE, 2>
  {
  public:
    HilbertSpace<HILBERTSPACE_SPIN_HALF_GEN_TYPE>(const uint32& _n_sites,
						  const qn_t& _quantumnumber)
    : HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_HALF_GEN_TYPE, 2>
    (_n_sites, _quantumnumber){};
  };

  template <>
  class HilbertSpace<HILBERTSPACE_SPIN_ONE_GEN_TYPE> :
    public HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_ONE_GEN_TYPE, 3>
  {
  public:
    HilbertSpace<HILBERTSPACE_SPIN_ONE_GEN_TYPE>(const uint32& _n_sites,
						 const qn_t& _quantumnumber)
    : HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_ONE_GEN_TYPE, 3>
    (_n_sites, _quantumnumber){};
  };

  template <>
  class HilbertSpace<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> :
    public HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE, 4>
  {
  public:
    HilbertSpace<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>(const uint32& _n_sites,
						 const qn_t& _quantumnumber)
    : HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE, 4>
    (_n_sites, _quantumnumber){};
  };

  template <>
  class HilbertSpace<HILBERTSPACE_SPIN_TWO_GEN_TYPE> :
    public HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_TWO_GEN_TYPE, 5>
  {
  public:
    HilbertSpace<HILBERTSPACE_SPIN_TWO_GEN_TYPE>(const uint32& _n_sites,
						 const qn_t& _quantumnumber)
    : HilbertSpaceSpinGenericBase<HILBERTSPACE_SPIN_TWO_GEN_TYPE, 5>
    (_n_sites, _quantumnumber){};
  };


  
  template <> inline uint32 local_dimension<HILBERTSPACE_SPIN_HALF_GEN_TYPE>()
  {return 2;}
  template <> inline uint32 local_dimension<HILBERTSPACE_SPIN_ONE_GEN_TYPE>()
  {return 3;}
  template <> inline uint32 local_dimension<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>()
  {return 4;}
  template <> inline uint32 local_dimension<HILBERTSPACE_SPIN_TWO_GEN_TYPE>()
  {return 5;}
}
    

#endif
