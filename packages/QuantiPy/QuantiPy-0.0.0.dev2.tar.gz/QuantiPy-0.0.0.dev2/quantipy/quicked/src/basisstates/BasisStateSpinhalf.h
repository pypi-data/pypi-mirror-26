/** @file BasisStatesSpinhalf.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Type definitions/basic functionality for Basis states in 
 *         Spinhalf Hilbertspaces
 *  
 */
#ifndef __QUICKED_BASISSTATES_BASISSTATESPINHALF_H__
#define __QUICKED_BASISSTATES_BASISSTATESPINHALF_H__

#include "BasisState.h"

namespace quicked
{
  template <> struct state_t<HILBERTSPACE_SPINHALF_TYPE> { typedef uint64 type; };

  template <> struct n_bits<HILBERTSPACE_SPINHALF_TYPE>
  { static const uint32 value = 1;};

  template <> struct local_dim<HILBERTSPACE_SPINHALF_TYPE>
  { static const uint32 value = 2;};
  
  template <> struct quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>
  { uint32 val; };// Sz Quantum Number

  template <> inline std::string qn2string<HILBERTSPACE_SPINHALF_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& qn)
  { std::ostringstream ss; ss << "{" << qn.val << "}"; return ss.str(); }

  template <> inline uint32 get_site_value<HILBERTSPACE_SPINHALF_TYPE>
  (const typename state_t<HILBERTSPACE_SPINHALF_TYPE>::type& state,
   const uint32& site)
  {return gbit(state, site);}

  template <> inline void set_site_value<HILBERTSPACE_SPINHALF_TYPE>
  (typename state_t<HILBERTSPACE_SPINHALF_TYPE>::type* state, const uint32& site,
   const uint32& value)
  {*state = (*state & ~((uint64)1 << site)) | ((uint64)value << site);}

  template <> inline typename state_t<HILBERTSPACE_SPINHALF_TYPE>::type
  get_site_mask<HILBERTSPACE_SPINHALF_TYPE>(const uint32& site)
  {return typename state_t<HILBERTSPACE_SPINHALF_TYPE>::type(1) << site;}

  template <> inline bool valid_quantumnumber<HILBERTSPACE_SPINHALF_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& qn, const uint32& n_sites)
  {return (qn.val<=n_sites);}
  
  template <> inline quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>
  get_quantumnumber<HILBERTSPACE_SPINHALF_TYPE>
  (const typename state_t<HILBERTSPACE_SPINHALF_TYPE>::type& state,
   const uint32& n_sites)
  {quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE> qn; qn.val=popcnt(state);
    return qn;}

  template <> inline bool operator ==
  (const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& b)
  {return a.val==b.val;}

  template <> inline bool operator <=
  (const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& b)
  {return a.val<=b.val;}

  template <> inline quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE> operator+
  (const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE> qn = {a.val + b.val};
    return qn;}

  template <> inline quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE> qn = {a.val - b.val};
    return qn;}

  template <> inline quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE> half_filling
  (const uint32& n_sites)
  { const quantumnumber_t<HILBERTSPACE_SPINHALF_TYPE> qn = {n_sites/2};  
    return qn;}
}
#endif
