/** @file HilbertSpaceTypes.h
 *   
 *  @author Alexander Wietek  
 *  @date 25.7.2015 
 * 
 *  @version 0.1 
 *  @brief Defines the Types of Hilbertspaces that are possible
 *  
 */

#ifndef __QUICKED_HILBERTSPACETYPES_H__
#define __QUICKED_HILBERTSPACETYPES_H__
#include <string>

typedef unsigned int hilbert_t;

///////////////////////////////////////////////////////////////
// Defining Makros for different Hilbertspace types
#define HILBERTSPACE_SPINHALF_TYPE 1

#define HILBERTSPACE_SU2_TYPE 2
#define HILBERTSPACE_SU3_TYPE 3
#define HILBERTSPACE_SU4_TYPE 4
#define HILBERTSPACE_SU5_TYPE 5
#define HILBERTSPACE_SU6_TYPE 6
#define HILBERTSPACE_SU7_TYPE 7
#define HILBERTSPACE_SU8_TYPE 8

#define HILBERTSPACE_SPIN_HALF_GEN_TYPE 17
#define HILBERTSPACE_SPIN_ONE_GEN_TYPE 18
#define HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE 19
#define HILBERTSPACE_SPIN_TWO_GEN_TYPE 20

#define HILBERTSPACE_2_TYPE 21
#define HILBERTSPACE_3_TYPE 22
#define HILBERTSPACE_4_TYPE 23
#define HILBERTSPACE_5_TYPE 24
#define HILBERTSPACE_6_TYPE 25
#define HILBERTSPACE_7_TYPE 26
#define HILBERTSPACE_8_TYPE 27

template<hilbert_t THilbertSpace>
inline std::string hs_name();
template <> inline std::string hs_name<HILBERTSPACE_SPINHALF_TYPE>()
{ return "HILBERTSPACE_SPINHALF_TYPE"; }

template <> inline std::string hs_name<HILBERTSPACE_SU2_TYPE>()
{ return "HILBERTSPACE_SU2_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SU3_TYPE>()
{ return "HILBERTSPACE_SU3_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SU4_TYPE>()
{ return "HILBERTSPACE_SU4_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SU5_TYPE>()
{ return "HILBERTSPACE_SU5_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SU6_TYPE>()
{ return "HILBERTSPACE_SU6_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SU7_TYPE>()
{ return "HILBERTSPACE_SU7_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SU8_TYPE>()
{ return "HILBERTSPACE_SU8_TYPE"; }

template <> inline std::string hs_name<HILBERTSPACE_SPIN_HALF_GEN_TYPE>()
{ return "HILBERTSPACE_SPIN_HALF_GEN_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SPIN_ONE_GEN_TYPE>()
{ return "HILBERTSPACE_SPIN_ONE_GEN_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>()
{ return "HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_SPIN_TWO_GEN_TYPE>()
{ return "HILBERTSPACE_SPIN_TWO_GEN_TYPE"; }

template <> inline std::string hs_name<HILBERTSPACE_2_TYPE>()
{ return "HILBERTSPACE_2_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_3_TYPE>()
{ return "HILBERTSPACE_3_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_4_TYPE>()
{ return "HILBERTSPACE_4_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_5_TYPE>()
{ return "HILBERTSPACE_5_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_6_TYPE>()
{ return "HILBERTSPACE_6_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_7_TYPE>()
{ return "HILBERTSPACE_7_TYPE"; }
template <> inline std::string hs_name<HILBERTSPACE_8_TYPE>()
{ return "HILBERTSPACE_8_TYPE"; }


#endif
