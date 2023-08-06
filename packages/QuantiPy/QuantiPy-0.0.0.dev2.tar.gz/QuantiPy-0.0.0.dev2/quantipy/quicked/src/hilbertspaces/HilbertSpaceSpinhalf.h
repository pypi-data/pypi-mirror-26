/** @file HilbertSpace_SpinHalf_incl.h
 *  @brief Template Specialization for Spinhalf Hilbertspaces upto 63 sites 
 *  @author Alexander Wietek  
 */

#ifndef __QUICKED_HILBERTSPACES_HILBERTSPACESPINHALF_H__
#define __QUICKED_HILBERTSPACES_HILBERTSPACESPINHALF_H__

#include "HilbertSpace.h"
#include "BasisState.h"
#include "BasisStateSpinhalfDetail.h"
#include "combinatorics.h"

namespace quicked
{

  ///////////////////////////////////////////////////////////////
  // SpinHalf HilbertSpace Template Specialization
  ///////////////////////////////////////////////////////////////

  template <> inline uint32 local_dimension<HILBERTSPACE_SPINHALF_TYPE>()
  {return 2;}


  template <>
  class HilbertSpace<HILBERTSPACE_SPINHALF_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_SPINHALF_TYPE>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_SPINHALF_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_SPINHALF_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_SPINHALF_TYPE>& b);

  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_SPINHALF_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_SPINHALF_TYPE>(const uint32& _n_sites,
					     const qn_t& _quantumnumber)
    : HilbertSpaceBase<HILBERTSPACE_SPINHALF_TYPE>(_n_sites,
						   combinatorics::binomial(_n_sites,
									   _quantumnumber.val)),
      quantumnumber_(_quantumnumber),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { 
      // Check if Number of upspins is valid
      assert(0 <= quantumnumber_.val);
      assert(quantumnumber_.val <= n_sites_);
    }

    inline qn_t quantumnumber() const {return quantumnumber_;} 

  
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     
    inline state_t operator[](const uint64& idx) const
    { return BasisStateSpinhalfDetail::get_nth_pattern<state_t>
	(idx, quantumnumber_.val, n_sites_);};
    inline uint64 index(const state_t& state) const
    { return BasisStateSpinhalfDetail::get_n_for_pattern<state_t>
	(state, quantumnumber_.val, n_sites_);};
  
  private:
    inline state_t get_first_state() const
    {return ((state_t)1 << quantumnumber_.val) - 1;}
    inline state_t get_next_state(const state_t& state) const 
    {return combinatorics::get_next_pattern(state);}
    inline state_t get_last_state() const
    {return (state_t)get_first_state() << (n_sites_ - quantumnumber_.val);}
    inline state_t get_stopper() const
    { // std::cout << "last:  " << BasisStateSUNDetail::base_print(get_last_state(), 2, n_sites()*2) << std::endl;
      // std::cout << "ntol:  " << BasisStateSUNDetail::base_print(combinatorics::get_next_pattern(get_last_state()), 2, n_sites()*2) << std::endl;
      return combinatorics::get_next_pattern(get_last_state());
    }

    const qn_t quantumnumber_;
    const iterator begin_;
    const iterator end_;

  };

 
}

#endif

