/** @file BasisStatesSUN.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Type definitions/basic functionality for Basis states in SU(N) 
 *         Hilbertspaces
 *  
 */
#ifndef __QUICKED_BASISSTATES_BASISSTATEUNCONSTRAINED_H__
#define __QUICKED_BASISSTATES_BASISSTATEUNCONSTRAINED_H__

#include <sstream>
#include "BasisStateSUNDetail.h"

#include "common.h"

namespace quicked
{
  // Type definition
  template <> struct state_t<HILBERTSPACE_2_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_3_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_4_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_5_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_6_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_7_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_8_TYPE> { typedef uint64 type; };

  // n_bits
  template<> struct n_bits<HILBERTSPACE_2_TYPE>
  { static const uint32 value = 1;};
  template<> struct n_bits<HILBERTSPACE_3_TYPE>
  { static const uint32 value = 2;};
  template<> struct n_bits<HILBERTSPACE_4_TYPE>
  { static const uint32 value = 2;};
  template<> struct n_bits<HILBERTSPACE_5_TYPE>
  { static const uint32 value = 3;};
  template<> struct n_bits<HILBERTSPACE_6_TYPE>
  { static const uint32 value = 3;};
  template<> struct n_bits<HILBERTSPACE_7_TYPE>
  { static const uint32 value = 3;};
  template<> struct n_bits<HILBERTSPACE_8_TYPE>
  { static const uint32 value = 3;};

  // local_dim
  template<> struct local_dim<HILBERTSPACE_2_TYPE>
  { static const uint32 value = 2;};
  template<> struct local_dim<HILBERTSPACE_3_TYPE>
  { static const uint32 value = 3;};
  template<> struct local_dim<HILBERTSPACE_4_TYPE>
  { static const uint32 value = 4;};
  template<> struct local_dim<HILBERTSPACE_5_TYPE>
  { static const uint32 value = 5;};
  template<> struct local_dim<HILBERTSPACE_6_TYPE>
  { static const uint32 value = 6;};
  template<> struct local_dim<HILBERTSPACE_7_TYPE>
  { static const uint32 value = 7;};
  template<> struct local_dim<HILBERTSPACE_8_TYPE>
  { static const uint32 value = 8;};

  // quantumnumber_t
  template <> struct quantumnumber_t<HILBERTSPACE_2_TYPE> { uint32 val; };  
  template <> struct quantumnumber_t<HILBERTSPACE_3_TYPE> { uint32 val; };
  template <> struct quantumnumber_t<HILBERTSPACE_4_TYPE> { uint32 val; };
  template <> struct quantumnumber_t<HILBERTSPACE_5_TYPE> { uint32 val; };
  template <> struct quantumnumber_t<HILBERTSPACE_6_TYPE> { uint32 val; };
  template <> struct quantumnumber_t<HILBERTSPACE_7_TYPE> { uint32 val; };
  template <> struct quantumnumber_t<HILBERTSPACE_8_TYPE> { uint32 val; };

  template <> inline std::string qn2string<HILBERTSPACE_2_TYPE>
  (const quantumnumber_t<HILBERTSPACE_2_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_3_TYPE>
  (const quantumnumber_t<HILBERTSPACE_3_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_4_TYPE>
  (const quantumnumber_t<HILBERTSPACE_4_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_5_TYPE>
  (const quantumnumber_t<HILBERTSPACE_5_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_6_TYPE>
  (const quantumnumber_t<HILBERTSPACE_6_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_7_TYPE>
  (const quantumnumber_t<HILBERTSPACE_7_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_8_TYPE>
  (const quantumnumber_t<HILBERTSPACE_8_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{}";
    return ss.str();
  }

    
  // get_site_value
  template <> inline uint32 get_site_value<HILBERTSPACE_2_TYPE>
  (const typename state_t<HILBERTSPACE_2_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<2, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_3_TYPE>
  (const typename state_t<HILBERTSPACE_3_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<3, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_4_TYPE>
  (const typename state_t<HILBERTSPACE_4_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<4, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_5_TYPE>
  (const typename state_t<HILBERTSPACE_5_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<5, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_6_TYPE>
  (const typename state_t<HILBERTSPACE_6_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<6, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_7_TYPE>
  (const typename state_t<HILBERTSPACE_7_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<7, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_8_TYPE>
  (const typename state_t<HILBERTSPACE_8_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<8, uint64>(state,site);}
    
  // set_site_value
  template <> inline void set_site_value<HILBERTSPACE_2_TYPE>
  (typename state_t<HILBERTSPACE_2_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<2, uint64>(state, site, value);}
  template <> inline void set_site_value<HILBERTSPACE_3_TYPE>
  (typename state_t<HILBERTSPACE_3_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<3, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_4_TYPE>
  (typename state_t<HILBERTSPACE_4_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<4, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_5_TYPE>
  (typename state_t<HILBERTSPACE_5_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<5, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_6_TYPE>
  (typename state_t<HILBERTSPACE_6_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<6, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_7_TYPE>
  (typename state_t<HILBERTSPACE_7_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<7, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_8_TYPE>
  (typename state_t<HILBERTSPACE_8_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<8, uint64>(state, site, value);}   

  // get_site_mask
  template <> inline typename state_t<HILBERTSPACE_2_TYPE>::type
  get_site_mask<HILBERTSPACE_2_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<2, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_3_TYPE>::type
  get_site_mask<HILBERTSPACE_3_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<3, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_4_TYPE>::type
  get_site_mask<HILBERTSPACE_4_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<4, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_5_TYPE>::type
  get_site_mask<HILBERTSPACE_5_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<5, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_6_TYPE>::type
  get_site_mask<HILBERTSPACE_6_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<6, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_7_TYPE>::type
  get_site_mask<HILBERTSPACE_7_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<7, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_8_TYPE>::type
  get_site_mask<HILBERTSPACE_8_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<8, uint64>(site); }

  // valid_quantumnumber
  template <> inline bool valid_quantumnumber<HILBERTSPACE_2_TYPE>
  (const quantumnumber_t<HILBERTSPACE_2_TYPE>& qn, const uint32& n_sites)
  {return true;}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_3_TYPE>
  (const quantumnumber_t<HILBERTSPACE_3_TYPE>& qn, const uint32& n_sites)
  {return true;}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_4_TYPE>
  (const quantumnumber_t<HILBERTSPACE_4_TYPE>& qn, const uint32& n_sites)
  {return true;}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_5_TYPE>
  (const quantumnumber_t<HILBERTSPACE_5_TYPE>& qn, const uint32& n_sites)
  {return true;}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_6_TYPE>
  (const quantumnumber_t<HILBERTSPACE_6_TYPE>& qn, const uint32& n_sites)
  {return true;}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_7_TYPE>
  (const quantumnumber_t<HILBERTSPACE_7_TYPE>& qn, const uint32& n_sites)
  {return true;}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_8_TYPE>
  (const quantumnumber_t<HILBERTSPACE_8_TYPE>& qn, const uint32& n_sites)
  {return true;}

  // get_quantumnumber
  template <> inline quantumnumber_t<HILBERTSPACE_2_TYPE>
  get_quantumnumber<HILBERTSPACE_2_TYPE>
  (const typename state_t<HILBERTSPACE_2_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_2_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_3_TYPE>
  get_quantumnumber<HILBERTSPACE_3_TYPE>
  (const typename state_t<HILBERTSPACE_3_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_3_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_4_TYPE>
  get_quantumnumber<HILBERTSPACE_4_TYPE>
  (const typename state_t<HILBERTSPACE_4_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_4_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_5_TYPE>
  get_quantumnumber<HILBERTSPACE_5_TYPE>
  (const typename state_t<HILBERTSPACE_5_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_5_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_6_TYPE>
  get_quantumnumber<HILBERTSPACE_6_TYPE>
  (const typename state_t<HILBERTSPACE_6_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_6_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_7_TYPE>
  get_quantumnumber<HILBERTSPACE_7_TYPE>
  (const typename state_t<HILBERTSPACE_7_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_7_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_8_TYPE>
  get_quantumnumber<HILBERTSPACE_8_TYPE>
  (const typename state_t<HILBERTSPACE_8_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_8_TYPE> qn = {0}; return qn; }

  // == operator for quantumnumbers
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_2_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_2_TYPE>& b)
  { return true; }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_3_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_3_TYPE>& b)
  { return true; }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_4_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_4_TYPE>& b)
  { return true; }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_5_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_5_TYPE>& b)
  { return true; }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_6_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_6_TYPE>& b)
  { return true; }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_7_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_7_TYPE>& b)
  { return true; }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_8_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_8_TYPE>& b)
  { return true; }

  // <= operator for quantumnumbers
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_2_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_2_TYPE>& b)
  { return true; }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_3_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_3_TYPE>& b)
  { return true; }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_4_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_4_TYPE>& b)
  { return true; }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_5_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_5_TYPE>& b)
  { return true; }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_6_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_6_TYPE>& b)
  { return true; }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_7_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_7_TYPE>& b)
  { return true; }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_8_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_8_TYPE>& b)
  { return true; }

  

  // addition operator for quantum numbers
  template <> inline quantumnumber_t<HILBERTSPACE_2_TYPE> operator+
  (const quantumnumber_t<HILBERTSPACE_2_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_2_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_2_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_3_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_3_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_3_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_3_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_4_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_4_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_4_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_4_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_5_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_5_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_5_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_5_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_6_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_6_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_6_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_6_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_7_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_7_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_7_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_7_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_8_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_8_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_8_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_8_TYPE> qn = {0}; return qn; }

  // subtraction operator for quantum numbers
  template <> inline quantumnumber_t<HILBERTSPACE_2_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_2_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_2_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_2_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_3_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_3_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_3_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_3_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_4_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_4_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_4_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_4_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_5_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_5_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_5_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_5_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_6_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_6_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_6_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_6_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_7_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_7_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_7_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_7_TYPE> qn = {0}; return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_8_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_8_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_8_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_8_TYPE> qn = {0}; return qn; }


  // half filling
  template <> quantumnumber_t<HILBERTSPACE_2_TYPE> half_filling
    (const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_2_TYPE> qn = {0}; return qn; }
  template <> quantumnumber_t<HILBERTSPACE_3_TYPE> half_filling
    (const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_3_TYPE> qn = {0}; return qn; }
  template <> quantumnumber_t<HILBERTSPACE_4_TYPE> half_filling
    (const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_4_TYPE> qn = {0}; return qn; }
  template <> quantumnumber_t<HILBERTSPACE_5_TYPE> half_filling
    (const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_5_TYPE> qn = {0}; return qn; }
  template <> quantumnumber_t<HILBERTSPACE_6_TYPE> half_filling
    (const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_6_TYPE> qn = {0}; return qn; }
  template <> quantumnumber_t<HILBERTSPACE_7_TYPE> half_filling
    (const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_7_TYPE> qn = {0}; return qn; }
  template <> quantumnumber_t<HILBERTSPACE_8_TYPE> half_filling
    (const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_8_TYPE> qn = {0}; return qn; }
  
}
#endif
