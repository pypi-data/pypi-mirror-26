/** @file BasisStateSpinhalfDetail.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Detailed implementations of Spinhalf Hilbertspace functions
 *  
 */

#ifndef __QUICKED_BASISSTATES_BASISSTATESPINHALFDETAIL_H__
#define __QUICKED_BASISSTATES_BASISSTATESPINHALFDETAIL_H__

#include "bitops.h"
#include "utils.h"
#include "combinatorics.h"
#include "common.h"

namespace quicked{
  ///////////////////////////////////////////////////////////////
  //Implementation of Detail namespace
  namespace BasisStateSpinhalfDetail
  {

    template <class T> inline T zero(const int& n_sites);
    template <> inline uint64 zero<uint64>(const int& n_sites){return 0;}

    template <class T> inline T one(const int& n_sites);
    template <> inline uint64 one<uint64>(const int& n_sites){return 1;}
  
    template <class T>
    T get_nth_pattern(const uint64& n, const uint64& n_upspins, const int& n_sites)
    {
      T state = zero<T>(n_sites);
      uint64 counter = n;
      for (int n_varying_bits = n_upspins-1; n_varying_bits >= 0; --n_varying_bits)
    	{
    	  uint64 n_combinations = 0;
    	  for(int n_allowed_pos = n_varying_bits; n_allowed_pos <= n_sites;
    	      ++n_allowed_pos)
    	    {
    	      n_combinations += combinatorics::binomial(n_allowed_pos,n_varying_bits);

    	      if( n_combinations > counter)
    		{
    		  counter -= n_combinations -
    		    combinatorics::binomial(n_allowed_pos,n_varying_bits);
    		  state |= (one<T>(n_sites) << n_allowed_pos);
    		  break;
    		}
    	    }
    	}
      return state;
    }


    // inverse of get_nth_pattern
    template <class T>
    uint64 get_n_for_pattern(const T& pattern, const uint64& n_upspins,
    			     const int& n_sites)
    {
      uint64 n=0;
      T workpattern = pattern;
      for (int n_varying_bits = n_upspins-1; n_varying_bits >= 0;
    	   --n_varying_bits)
    	{
    	  for (int i=0; i <= n_sites; ++i)
    	    {
    	      // MSB is at 2^i
    	      if ((one<T>(n_sites) << (i+1)) > workpattern)
    		{
    		  n += combinatorics::binomial(i,n_varying_bits+1);
    		  workpattern ^= (one<T>(n_sites) << i);
    		  break;
    		}
    	    }
    	}
      return n;
    }

  }
}

#endif
