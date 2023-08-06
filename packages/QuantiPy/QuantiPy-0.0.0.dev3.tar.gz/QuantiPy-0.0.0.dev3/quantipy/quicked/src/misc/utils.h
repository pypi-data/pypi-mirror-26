/** @file utils.h
 *  @brief some nice and handy functions collected here
 *  @author Alexander Wietek  
 */

#ifndef __QUICKED_MISC_UTILS_H__
#define __QUICKED_MISC_UTILS_H__

#include <string>
#include <complex>

#include "bitops.h"
#include "common.h"

namespace quicked { namespace utils
{
  template <class T>
  std::string matrix_print(T* A, const int& matrix_dim)
  {
    std::ostringstream res_string;
    for (int i = 0; i < matrix_dim; ++i) 
      {
	for (int j = 0; j < matrix_dim; ++j)
	  res_string << A[i*matrix_dim + j] << " ";
	res_string << std::endl;
      }
    return res_string.str();
  }

  template <class T>
  std::string vector_print(T* v, const int& vector_dim)
  {
    std::ostringstream res_string;
    for (int j = 0; j < vector_dim; ++j)
      res_string << v[j] << std::endl;
    return res_string.str();  
  }

  std::string base_print(uint64 number,int base,int digits) {
    std::ostringstream res_string;
    
    for(int d=0;d<digits-1;++d) {
      res_string<<(number%base)<<" ";
      number/=base;
    }
    res_string<<(number%base);
	      
    return res_string.str();
  }


  inline uint64 apply_permutation(const uint64& state,
				  const int& n_sites, 
				  const int* permutation)
  {
    uint64 tstate=0;
    for(int i=0; i < n_sites;++i)
      tstate |= ((uint64) gbit(state, n_sites - 1 - i )) <<
	(n_sites - 1 - permutation[i]);
    return tstate;
  }

  
  namespace complex 
  {
    template <class TCoeffs> inline double real(const TCoeffs& x);
    template <> inline double real(const std::complex<double>& x){return std::real(x);}
    template <> inline double real(const double& x){return x;}
    
    template <class TCoeffs> inline double imag(const TCoeffs& x);
    template <> inline double imag(const std::complex<double>& x){return std::imag(x);}
    template <> inline double imag(const double& x){return 0.;}
        
    template <class TCoeffs> inline TCoeffs conj(const TCoeffs& x);
    template <> inline std::complex<double> conj(const std::complex<double>& x){return std::conj(x);}
    template <> inline double conj(const double& x){return x;}
  }

  uint32 index_multisite(const uint32& n_local_vals, const uint32 *local_vals,
			 const uint32& local_dim)
  {
    uint32 index = 0;
    for (uint32 i = 0; i < n_local_vals; ++i)
      index += local_vals[i] * pow(local_dim, i);
    return index;
  }

  void localvals_multisite(const uint32& index, const uint32& n_local_vals,
			   const uint32& local_dim, uint32 *local_vals)
  {
    uint32 workindex = index;
    for (uint32 i = 0; i < n_local_vals; ++i)
      {
	
	local_vals[i] = workindex % local_dim;
	workindex /= local_dim;
      }
  }

}}

#endif
