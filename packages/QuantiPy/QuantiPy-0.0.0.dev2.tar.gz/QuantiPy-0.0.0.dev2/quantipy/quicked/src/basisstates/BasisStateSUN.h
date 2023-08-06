/** @file BasisStatesSUN.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Type definitions/basic functionality for Basis states in SU(N) 
 *         Hilbertspaces
 *  
 */
#ifndef __QUICKED_BASISSTATES_BASISSTATESUN_H__
#define __QUICKED_BASISSTATES_BASISSTATESUN_H__

#include <algorithm>
#include <iterator>

#include "BasisStateSUNDetail.h"

namespace quicked
{
  // Type definition
  template <> struct state_t<HILBERTSPACE_SU2_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SU3_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SU4_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SU5_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SU6_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SU7_TYPE> { typedef uint64 type; };
  template <> struct state_t<HILBERTSPACE_SU8_TYPE> { typedef uint64 type; };

  // n_bits
  template<> struct n_bits<HILBERTSPACE_SU2_TYPE>
  { static const uint32 value = 1;};
  template<> struct n_bits<HILBERTSPACE_SU3_TYPE>
  { static const uint32 value = 2;};
  template<> struct n_bits<HILBERTSPACE_SU4_TYPE>
  { static const uint32 value = 2;};
  template<> struct n_bits<HILBERTSPACE_SU5_TYPE>
  { static const uint32 value = 3;};
  template<> struct n_bits<HILBERTSPACE_SU6_TYPE>
  { static const uint32 value = 3;};
  template<> struct n_bits<HILBERTSPACE_SU7_TYPE>
  { static const uint32 value = 3;};
  template<> struct n_bits<HILBERTSPACE_SU8_TYPE>
  { static const uint32 value = 3;};

  // local_dim
  template<> struct local_dim<HILBERTSPACE_SU2_TYPE>
  { static const uint32 value = 2;};
  template<> struct local_dim<HILBERTSPACE_SU3_TYPE>
  { static const uint32 value = 3;};
  template<> struct local_dim<HILBERTSPACE_SU4_TYPE>
  { static const uint32 value = 4;};
  template<> struct local_dim<HILBERTSPACE_SU5_TYPE>
  { static const uint32 value = 5;};
  template<> struct local_dim<HILBERTSPACE_SU6_TYPE>
  { static const uint32 value = 6;};
  template<> struct local_dim<HILBERTSPACE_SU7_TYPE>
  { static const uint32 value = 7;};
  template<> struct local_dim<HILBERTSPACE_SU8_TYPE>
  { static const uint32 value = 8;};

  // quantumnumber_t
  template <> struct quantumnumber_t<HILBERTSPACE_SU2_TYPE> { uint32 val[2]; };  
  template <> struct quantumnumber_t<HILBERTSPACE_SU3_TYPE> { uint32 val[3]; };
  template <> struct quantumnumber_t<HILBERTSPACE_SU4_TYPE> { uint32 val[4]; };
  template <> struct quantumnumber_t<HILBERTSPACE_SU5_TYPE> { uint32 val[5]; };
  template <> struct quantumnumber_t<HILBERTSPACE_SU6_TYPE> { uint32 val[6]; };
  template <> struct quantumnumber_t<HILBERTSPACE_SU7_TYPE> { uint32 val[7]; };
  template <> struct quantumnumber_t<HILBERTSPACE_SU8_TYPE> { uint32 val[8]; };

  template <> inline std::string qn2string<HILBERTSPACE_SU2_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{" << qn.val[0] << ",";
    for (uint32 i = 1; i < 1; ++i) ss << qn.val[i] << ",";
    ss << qn.val[1] << "}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_SU3_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{" << qn.val[0] << ",";
    for (uint32 i = 1; i < 2; ++i) ss << qn.val[i] << ",";
    ss << qn.val[2] << "}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_SU4_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{" << qn.val[0] << ",";
    for (uint32 i = 1; i < 3; ++i) ss << qn.val[i] << ",";
    ss << qn.val[3] << "}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_SU5_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{" << qn.val[0] << ",";
    for (uint32 i = 1; i < 4; ++i) ss << qn.val[i] << ",";
    ss << qn.val[4] << "}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_SU6_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{" << qn.val[0] << ",";
    for (uint32 i = 1; i < 5; ++i) ss << qn.val[i] << ",";
    ss << qn.val[5] << "}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_SU7_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{" << qn.val[0] << ",";
    for (uint32 i = 1; i < 6; ++i) ss << qn.val[i] << ",";
    ss << qn.val[6] << "}";
    return ss.str();
  }
  template <> inline std::string qn2string<HILBERTSPACE_SU8_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& qn)
  {
    std::ostringstream ss;
    ss << "{" << qn.val[0] << ",";
    for (uint32 i = 1; i < 7; ++i) ss << qn.val[i] << ",";
    ss << qn.val[7] << "}";
    return ss.str();
  }

    
  // get_site_value
  template <> inline uint32 get_site_value<HILBERTSPACE_SU2_TYPE>
  (const typename state_t<HILBERTSPACE_SU2_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<2, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SU3_TYPE>
  (const typename state_t<HILBERTSPACE_SU3_TYPE>::type& state, const uint32& site)  {return BasisStateSUNDetail::_get_site_value_sun<3, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SU4_TYPE>
  (const typename state_t<HILBERTSPACE_SU4_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<4, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SU5_TYPE>
  (const typename state_t<HILBERTSPACE_SU5_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<5, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SU6_TYPE>
  (const typename state_t<HILBERTSPACE_SU6_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<6, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SU7_TYPE>
  (const typename state_t<HILBERTSPACE_SU7_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<7, uint64>(state,site);}
  template <> inline uint32 get_site_value<HILBERTSPACE_SU8_TYPE>
  (const typename state_t<HILBERTSPACE_SU8_TYPE>::type& state, const uint32& site)
  {return BasisStateSUNDetail::_get_site_value_sun<8, uint64>(state,site);}
    
  // set_site_value
  template <> inline void set_site_value<HILBERTSPACE_SU2_TYPE>
  (typename state_t<HILBERTSPACE_SU2_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<2, uint64>(state, site, value);}
  template <> inline void set_site_value<HILBERTSPACE_SU3_TYPE>
  (typename state_t<HILBERTSPACE_SU3_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<3, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_SU4_TYPE>
  (typename state_t<HILBERTSPACE_SU4_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<4, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_SU5_TYPE>
  (typename state_t<HILBERTSPACE_SU5_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<5, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_SU6_TYPE>
  (typename state_t<HILBERTSPACE_SU6_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<6, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_SU7_TYPE>
  (typename state_t<HILBERTSPACE_SU7_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<7, uint64>(state, site, value);}   
  template <> inline void set_site_value<HILBERTSPACE_SU8_TYPE>
  (typename state_t<HILBERTSPACE_SU8_TYPE>::type* state, const uint32& site,
   const uint32& value) 
  {BasisStateSUNDetail::_set_site_value_sun<8, uint64>(state, site, value);}   

  // get_site_mask
  template <> inline typename state_t<HILBERTSPACE_SU2_TYPE>::type
  get_site_mask<HILBERTSPACE_SU2_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<2, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SU3_TYPE>::type
  get_site_mask<HILBERTSPACE_SU3_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<3, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SU4_TYPE>::type
  get_site_mask<HILBERTSPACE_SU4_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<4, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SU5_TYPE>::type
  get_site_mask<HILBERTSPACE_SU5_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<5, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SU6_TYPE>::type
  get_site_mask<HILBERTSPACE_SU6_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<6, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SU7_TYPE>::type
  get_site_mask<HILBERTSPACE_SU7_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<7, uint64>(site); }
  template <> inline typename state_t<HILBERTSPACE_SU8_TYPE>::type
  get_site_mask<HILBERTSPACE_SU8_TYPE>(const uint32& site)
  {return BasisStateSUNDetail::_get_site_mask<8, uint64>(site); }

  // valid_quantumnumber
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SU2_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& qn, const uint32& n_sites)
  {return BasisStateSUNDetail::_valid_quantumnumber_sun<2>(n_sites, qn.val);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SU3_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& qn, const uint32& n_sites)
  {return BasisStateSUNDetail::_valid_quantumnumber_sun<3>(n_sites, qn.val);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SU4_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& qn, const uint32& n_sites)
  {return BasisStateSUNDetail::_valid_quantumnumber_sun<4>(n_sites, qn.val);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SU5_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& qn, const uint32& n_sites)
  {return BasisStateSUNDetail::_valid_quantumnumber_sun<5>(n_sites, qn.val);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SU6_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& qn, const uint32& n_sites)
  {return BasisStateSUNDetail::_valid_quantumnumber_sun<6>(n_sites, qn.val);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SU7_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& qn, const uint32& n_sites)
  {return BasisStateSUNDetail::_valid_quantumnumber_sun<7>(n_sites, qn.val);}
  template <> inline bool valid_quantumnumber<HILBERTSPACE_SU8_TYPE>
  (const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& qn, const uint32& n_sites)
  {return BasisStateSUNDetail::_valid_quantumnumber_sun<8>(n_sites, qn.val);}

  // get_quantumnumber
  template <> inline quantumnumber_t<HILBERTSPACE_SU2_TYPE>
  get_quantumnumber<HILBERTSPACE_SU2_TYPE>
  (const typename state_t<HILBERTSPACE_SU2_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SU2_TYPE> qn;
    BasisStateSUNDetail::_get_color_numbers<2, uint64>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SU3_TYPE>
  get_quantumnumber<HILBERTSPACE_SU3_TYPE>
  (const typename state_t<HILBERTSPACE_SU3_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SU3_TYPE> qn;
    BasisStateSUNDetail::_get_color_numbers<3, uint64>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SU4_TYPE>
  get_quantumnumber<HILBERTSPACE_SU4_TYPE>
  (const typename state_t<HILBERTSPACE_SU4_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SU4_TYPE> qn;
    BasisStateSUNDetail::_get_color_numbers<4, uint64>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SU5_TYPE>
  get_quantumnumber<HILBERTSPACE_SU5_TYPE>
  (const typename state_t<HILBERTSPACE_SU5_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SU5_TYPE> qn;
    BasisStateSUNDetail::_get_color_numbers<5, uint64>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SU6_TYPE>
  get_quantumnumber<HILBERTSPACE_SU6_TYPE>
  (const typename state_t<HILBERTSPACE_SU6_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SU6_TYPE> qn;
    BasisStateSUNDetail::_get_color_numbers<6, uint64>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SU7_TYPE>
  get_quantumnumber<HILBERTSPACE_SU7_TYPE>
  (const typename state_t<HILBERTSPACE_SU7_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SU7_TYPE> qn;
    BasisStateSUNDetail::_get_color_numbers<7, uint64>(state, n_sites, &qn.val);
    return qn; }
  template <> inline quantumnumber_t<HILBERTSPACE_SU8_TYPE>
  get_quantumnumber<HILBERTSPACE_SU8_TYPE>
  (const typename state_t<HILBERTSPACE_SU8_TYPE>::type& state,
   const uint32& n_sites)
  { quantumnumber_t<HILBERTSPACE_SU8_TYPE> qn;
    BasisStateSUNDetail::_get_color_numbers<8, uint64>(state, n_sites, &qn.val);
    return qn; }

  // == operator for quantumnumbers
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& b)
  { return std::equal(a.val, a.val + 2, b.val); }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& b)
  { return std::equal(a.val, a.val + 3, b.val); }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& b)
  { return std::equal(a.val, a.val + 4, b.val); }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& b)
  { return std::equal(a.val, a.val + 5, b.val); }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& b)
  { return std::equal(a.val, a.val + 6, b.val); }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& b)
  { return std::equal(a.val, a.val + 7, b.val); }
  template <> inline bool operator ==
    (const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& b)
  { return std::equal(a.val, a.val + 8, b.val); }

  // <= operator for quantumnumbers
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& b)
  { return BasisStateSUNDetail::_less_equal<2>(a.val, b.val); }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& b)
  { return BasisStateSUNDetail::_less_equal<3>(a.val, b.val); }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& b)
  { return BasisStateSUNDetail::_less_equal<4>(a.val, b.val); }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& b)
  { return BasisStateSUNDetail::_less_equal<5>(a.val, b.val); }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& b)
  { return BasisStateSUNDetail::_less_equal<6>(a.val, b.val); }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& b)
  { return BasisStateSUNDetail::_less_equal<7>(a.val, b.val); }
  template <> inline bool operator <=
    (const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& b)
  { return BasisStateSUNDetail::_less_equal<8>(a.val, b.val); }

  // addition operator for quantum numbers
  template <> inline quantumnumber_t<HILBERTSPACE_SU2_TYPE> operator+
  (const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU2_TYPE> qn;
    BasisStateSUNDetail::_add_arrays<2>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU3_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU3_TYPE> qn;
    BasisStateSUNDetail::_add_arrays<3>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU4_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU4_TYPE> qn;
    BasisStateSUNDetail::_add_arrays<4>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU5_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU5_TYPE> qn;
    BasisStateSUNDetail::_add_arrays<5>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU6_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU6_TYPE> qn;
    BasisStateSUNDetail::_add_arrays<6>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU7_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU7_TYPE> qn;
    BasisStateSUNDetail::_add_arrays<7>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU8_TYPE> operator+
    (const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& a,
     const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU8_TYPE> qn;
    BasisStateSUNDetail::_add_arrays<8>(a.val, b.val, &qn.val); return qn;}

  // subtraction operator for quantum numbers
  template <> inline quantumnumber_t<HILBERTSPACE_SU2_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU2_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU2_TYPE> qn;
    BasisStateSUNDetail::_sub_arrays<2>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU3_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU3_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU3_TYPE> qn;
    BasisStateSUNDetail::_sub_arrays<3>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU4_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU4_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU4_TYPE> qn;
    BasisStateSUNDetail::_sub_arrays<4>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU5_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU5_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU5_TYPE> qn;
    BasisStateSUNDetail::_sub_arrays<5>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU6_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU6_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU6_TYPE> qn;
    BasisStateSUNDetail::_sub_arrays<6>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU7_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU7_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU7_TYPE> qn;
    BasisStateSUNDetail::_sub_arrays<7>(a.val, b.val, &qn.val); return qn;}
  template <> inline quantumnumber_t<HILBERTSPACE_SU8_TYPE> operator-
  (const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& a,
   const quantumnumber_t<HILBERTSPACE_SU8_TYPE>& b)
  { quantumnumber_t<HILBERTSPACE_SU8_TYPE> qn;
    BasisStateSUNDetail::_sub_arrays<8>(a.val, b.val, &qn.val); return qn;}


  // half filling
  template <> quantumnumber_t<HILBERTSPACE_SU2_TYPE> half_filling
    (const uint32& n_sites)
  {
    const quantumnumber_t<HILBERTSPACE_SU2_TYPE> qn = {{n_sites/2,n_sites/2}};
    return qn;
  }
  template <> quantumnumber_t<HILBERTSPACE_SU3_TYPE> half_filling
    (const uint32& n_sites)
  {
    quantumnumber_t<HILBERTSPACE_SU3_TYPE> qn = {{n_sites/3,n_sites/3,n_sites/3}};
    return qn;
  }
  template <> quantumnumber_t<HILBERTSPACE_SU4_TYPE> half_filling
    (const uint32& n_sites)
  {
    quantumnumber_t<HILBERTSPACE_SU4_TYPE> qn =
      {{n_sites/4,n_sites/4,n_sites/4,n_sites/4}};
    return qn;
  }
  template <> quantumnumber_t<HILBERTSPACE_SU5_TYPE> half_filling
    (const uint32& n_sites)
  {
    quantumnumber_t<HILBERTSPACE_SU5_TYPE> qn =
      {{n_sites/5,n_sites/5,n_sites/5,n_sites/5,n_sites/5}};
    return qn;
  }
  template <> quantumnumber_t<HILBERTSPACE_SU6_TYPE> half_filling
    (const uint32& n_sites)
  {
    quantumnumber_t<HILBERTSPACE_SU6_TYPE> qn =
      {{n_sites/6,n_sites/6,n_sites/6,n_sites/6,n_sites/6,n_sites/6}};
    return qn;
  }
  template <> quantumnumber_t<HILBERTSPACE_SU7_TYPE> half_filling
    (const uint32& n_sites)
  {
    quantumnumber_t<HILBERTSPACE_SU7_TYPE> qn =
      {{n_sites/7,n_sites/7,n_sites/7,n_sites/7,n_sites/7,n_sites/7, n_sites/7}};
    return qn;
  }
  template <> quantumnumber_t<HILBERTSPACE_SU8_TYPE> half_filling
    (const uint32& n_sites)
  {
    quantumnumber_t<HILBERTSPACE_SU8_TYPE> qn =
      {{n_sites/8, n_sites/8, n_sites/8, n_sites/8, n_sites/8, n_sites/8,
	n_sites/8, n_sites/8}};
    return qn;
  }
  
}
#endif
