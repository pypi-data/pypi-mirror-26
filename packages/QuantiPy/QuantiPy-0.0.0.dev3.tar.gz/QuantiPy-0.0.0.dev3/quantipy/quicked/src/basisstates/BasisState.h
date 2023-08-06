/** @file BasisStates.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Type definitions/basic functionality for Basis states and their corresponding quantum numbers
 *  
 */
#ifndef __QUICKED_BASISSTATES_BASISSTATE_H__
#define __QUICKED_BASISSTATES_BASISSTATE_H__

#include <string>
#include <numeric>

#include "HilbertSpaceTypes.h"

#include "bitops.h"
#include "common.h"


namespace quicked 
{

  // Define State types for the different hilbertspaces
  template <hilbert_t THilbertSpace> struct state_t;

  // Trait defining how many bits are used for one site
  template<hilbert_t THilbertSpace> struct n_bits{ static const uint32 value = 1;};

  // Trait defining local dimension of hilbertspace
  template<hilbert_t THilbertSpace> struct local_dim{ static const uint32 value;};

  // Define QuantumNumber types of the computational basis for the
  // different hilbertspaces
  template <hilbert_t THilbertSpace> struct quantumnumber_t;

  // function for printing the quantum number
  template <hilbert_t THilbertSpace> inline std::string qn2string
  (const quantumnumber_t<THilbertSpace>& qn);

  // Functions for getting/setting the site value of a state
  template <hilbert_t THilbertSpace>
  inline uint32 get_site_value(const typename state_t<THilbertSpace>::type& state,
			       const uint32& site);
  template <hilbert_t THilbertSpace>
  inline void set_site_value(typename state_t<THilbertSpace>::type* state,
			     const uint32& site, const uint32& value);

  // Site masks 
  template <hilbert_t THilbertSpace>
  inline typename state_t<THilbertSpace>::type get_site_mask(const uint32& site);

  template <hilbert_t THilbertSpace>
  inline typename state_t<THilbertSpace>::type get_multisite_mask
  (const uint32& n_mask_sites, const uint32& n_sites, const uint32* sites)
  {
    typename state_t<THilbertSpace>::type mask(0);
    for (uint32 i=0; i < n_mask_sites; ++i)
      mask |= get_site_mask<THilbertSpace>(sites[i]);
    return mask;
  }

  // Function to check whether a state is well formed
  template <hilbert_t THilbertSpace> inline bool
  valid_state(const typename state_t<THilbertSpace>::type& state,
	      const uint32& n_sites)
  {
    for (uint32 i=0; i < n_sites; ++i)
      if (get_site_value<THilbertSpace>(state, i) >=
	  local_dim<THilbertSpace>::value) return false;
    return true;
  }

  // Function to check whether a state is well formed
  template <hilbert_t THilbertSpace> inline bool
  valid_quantumnumber(const quantumnumber_t<THilbertSpace>& qn,
		      const uint32& n_sites);
  
  // Function to retrieve quantum numbers from state
  template <hilbert_t THilbertSpace> inline quantumnumber_t<THilbertSpace>
  get_quantumnumber(const typename state_t<THilbertSpace>::type& state,
		    const uint32& n_sites);

  // Generic comparision for quantum numbers
  template <hilbert_t THilbertSpace> inline bool operator ==
  (const quantumnumber_t<THilbertSpace>& a,
   const quantumnumber_t<THilbertSpace>& b);
  template <hilbert_t THilbertSpace> inline bool operator !=
  (const quantumnumber_t<THilbertSpace>& a,
   const quantumnumber_t<THilbertSpace>& b)
  {return !(a==b);}

  // Generic order for quantum numbers
  template <hilbert_t THilbertSpace> inline bool operator <=
  (const quantumnumber_t<THilbertSpace>& a,
   const quantumnumber_t<THilbertSpace>& b);

  // Addition/Subtraction operator for quantum numbers
  template <hilbert_t THilbertSpace>
  inline quantumnumber_t<THilbertSpace> operator+
  (const quantumnumber_t<THilbertSpace>& a,
   const quantumnumber_t<THilbertSpace>& b);

  template <hilbert_t THilbertSpace>
  inline quantumnumber_t<THilbertSpace> operator-
  (const quantumnumber_t<THilbertSpace>& a, 
   const quantumnumber_t<THilbertSpace>& b);

  // Return quantum numbers for half_filling (whenever this makes sense)
  template <hilbert_t THilbertSpace>
  inline quantumnumber_t<THilbertSpace> half_filling(const uint32& n_sites);
 
  // Function to swap several site values between two states
  template <hilbert_t THilbertSpace>
  inline void swap_sites_with_mask
  (const typename state_t<THilbertSpace>::type& mask,
   typename state_t<THilbertSpace>::type *a,
   typename state_t<THilbertSpace>::type *b)
  {
    // get bits in mask
    typename state_t<THilbertSpace>::type ainmask = (*a) & mask;
    typename state_t<THilbertSpace>::type binmask = (*b) & mask;
    // set bits to zero
    *a &= (~mask);
    *b &= (~mask);
    // swap bits
    *a |= binmask;
    *b |= ainmask;
  }
  
 template <hilbert_t THilbertSpace>
 inline void swap_sites(const uint32& n_sites, const uint32& n_mask_sites,
			const uint32* sites,
			typename state_t<THilbertSpace>::type *a,
			typename state_t<THilbertSpace>::type *b)
  {
    typename state_t<THilbertSpace>::type mask =
      get_multisite_mask<THilbertSpace>(n_mask_sites, n_sites, sites);
    swap_sites_with_mask<THilbertSpace>(mask, a, b);
  }

  
  // Functions for converting states to strings
  template <hilbert_t THilbertSpace> std::string state_string
  (const typename state_t<THilbertSpace>::type& state, const uint32& n_sites)
  {
    std::ostringstream ss;
    for (uint32 i = 0; i < n_sites-1; ++i)
      ss << get_site_value<THilbertSpace>(state, i);
    ss << get_site_value<THilbertSpace>(state, n_sites-1);
    return ss.str();
  }


}

#include "BasisStateSUN.h"
#include "BasisStateSpinhalf.h"
#include "BasisStateSpinGeneric.h"
#include "BasisStateUnconstrained.h"

#endif
