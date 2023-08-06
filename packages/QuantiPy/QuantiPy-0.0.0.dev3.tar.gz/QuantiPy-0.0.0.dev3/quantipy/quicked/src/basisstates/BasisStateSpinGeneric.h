/** @file BasisStatesSUN.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Type definitions/basic functionality for Basis states in SU(N) 
 *         Hilbertspaces
 *  
 */
#ifndef __QUICKED_BASISSTATES_BASISSTATESPINGENERIC_H__
#define __QUICKED_BASISSTATES_BASISSTATESPINGENERIC_H__

#include <algorithm>
#include <iterator>

#include "BasisStateSUNDetail.h"
#include "BasisStateSpinGenericDetail.h"

namespace quicked
{
  // Type definition
  template <> struct state_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  { typedef uint64 type; };
  
  // n_bits
  template<> struct n_bits<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  { static const uint32 value = 1;};
  template<> struct n_bits<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  { static const uint32 value = 2;};
  template<> struct n_bits<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  { static const uint32 value = 2;};
  template<> struct n_bits<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  { static const uint32 value = 3;};

  // local_dim
  template<> struct local_dim<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  { static const uint32 value = 2;};
  template<> struct local_dim<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  { static const uint32 value = 3;};
  template<> struct local_dim<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  { static const uint32 value = 4;};
  template<> struct local_dim<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  { static const uint32 value = 5;};

  // quantumnumber_t
  template <> struct quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  { uint32 val; };  
  template <> struct quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  { uint32 val; };
  template <> struct quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  { uint32 val; };
  template <> struct quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  { uint32 val; };


  template <> inline std::string qn2string<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& qn)
  { std::ostringstream ss; ss << "{" << qn.val << "}"; return ss.str(); }

  template <> inline std::string qn2string<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& qn)
  { std::ostringstream ss; ss << "{" << qn.val << "}"; return ss.str(); }

  template <> inline std::string qn2string<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& qn)
  { std::ostringstream ss; ss << "{" << qn.val << "}"; return ss.str(); }

  template <> inline std::string qn2string<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& qn)
  { std::ostringstream ss; ss << "{" << qn.val << "}"; return ss.str(); }  
  
  // get_site_value (using SU(N) detail functions)
  template <> inline uint32 get_site_value<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>::type& state,
   const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<2, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>::type& state,
   const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<3, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>::type& state,
   const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<4, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>::type& state,
   const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<5, uint64>(state,site);}
    
  // set_site_value
  template <> inline void set_site_value<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  (typename state_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>::type* state,
   const uint32& site, const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<2, uint64>(state, site, value);}
  template <> inline void set_site_value<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  (typename state_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>::type* state,
   const uint32& site, const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<3, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  (typename state_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>::type* state,
   const uint32& site, const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<4, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  (typename state_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>::type* state,
   const uint32& site, const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<5, uint64>(state, site, value);}   

  // get_site_mask
  template <> inline typename state_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>::type
  get_site_mask<HILBERTSPACE_SPIN_HALF_GEN_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<2, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>::type
  get_site_mask<HILBERTSPACE_SPIN_ONE_GEN_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<3, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>::type
  get_site_mask<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<4, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>::type
  get_site_mask<HILBERTSPACE_SPIN_TWO_GEN_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<5, uint64>(site); }

  // valid_quantumnumber
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& qn,
   const uint32& n_sites)
  {return (qn.val <= n_sites);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& qn,
   const uint32& n_sites)
  {return (qn.val <= n_sites*2);}
  template <>
  inline bool valid_quantumnumber<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& qn,
   const uint32& n_sites)
  {return (qn.val <= n_sites*3);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& qn,
   const uint32& n_sites)
  {return (qn.val <= n_sites*4);}

  // get_quantumnumber
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  get_quantumnumber<HILBERTSPACE_SPIN_HALF_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE> qn;
    BasisStateSpinGenericDetail::_get_sz<1>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  get_quantumnumber<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE> qn;
    BasisStateSpinGenericDetail::_get_sz<2>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  get_quantumnumber<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> qn;
    BasisStateSpinGenericDetail::_get_sz<2>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  get_quantumnumber<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
  (const typename state_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE> qn;
    BasisStateSpinGenericDetail::_get_sz<3>(state, n_sites, &qn.val);
    return qn; }
  

  // == operator for quantumnumbers
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& b)
  { return a.val == b.val; }
  template <> inline bool operator ==
  (const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& b)
  { return a.val == b.val; }
  template <> inline bool operator ==
  (const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& b)
  { return a.val == b.val; }
  template <> inline bool operator ==
  (const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& b)
  { return a.val == b.val; }
  
  // <= operator for quantumnumbers
  template <> inline bool operator <=
  (const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& b)
  { return a.val <= b.val; }
  template <> inline bool operator <=
  (const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& b)
  { return a.val <= b.val; }
  template <> inline bool operator <=
  (const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& b)
  { return a.val <= b.val; }
  template <> inline bool operator <=
  (const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& b)
  { return a.val <= b.val; }
  
  // addition operator for quantum numbers
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE> operator+
  (const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE> qn = {a.val + b.val};
    return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE> operator+
  (const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE> qn = {a.val + b.val};
    return qn;}
  template <>
  inline quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> operator+
  (const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> qn =
      {a.val + b.val};
    return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE> operator+
  (const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE> qn = {a.val + b.val};
    return qn;}

  // subtraction operator for quantum numbers
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE> qn = {a.val - b.val};
    return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE> qn = {a.val - b.val};
    return qn;}
  template <>
  inline quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> qn =
      {a.val - b.val};
    return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE>& b)
  { const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE> qn = {a.val - b.val};
    return qn;}


  // half filling
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE> half_filling
  (const uint32& n_sites)
  { const quantumnumber_t<HILBERTSPACE_SPIN_HALF_GEN_TYPE> qn = {n_sites/2};  
    return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE> half_filling
  (const uint32& n_sites)
  { const quantumnumber_t<HILBERTSPACE_SPIN_ONE_GEN_TYPE> qn = {n_sites};  
    return qn;}  
  template <>
  inline quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> half_filling
  (const uint32& n_sites)
  { const quantumnumber_t<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE> qn ={3*n_sites/2};
    return qn;}  
  template <> inline quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE> half_filling
  (const uint32& n_sites)
  { const quantumnumber_t<HILBERTSPACE_SPIN_TWO_GEN_TYPE> qn = {2*n_sites};  
    return qn;}  
  
}
#endif
