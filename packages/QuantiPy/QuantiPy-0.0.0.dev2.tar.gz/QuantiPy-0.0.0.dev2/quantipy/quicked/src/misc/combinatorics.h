/** @file combinatorics.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief collection combinatorical functions 
 */

#ifndef __QUICKED_MISC_COMBINATORICS_H__
#define __QUICKED_MISC_COMBINATORICS_H__

#include "common.h"
#include "bitops.h"

namespace quicked{ namespace combinatorics
  {
    int factorial(int n)
    {
      return (n == 1 || n == 0) ? 1 : factorial(n - 1) * n;
    }
    
    // Binomial coefficient
    inline unsigned long long binomial(const int l,const int n)
    {
      if(n>l || n<0) return 0;
      unsigned long long res = 1;
      for (int i=1;i<=n;i++) res = (res*(l-i+1))/i;
      return res;
    }

    // Multinomial coefficient
    template <uint32 N>
    uint64 multinomial(const uint32 n, const uint32 (&ks)[N])
    {
      uint64 result = 1;
      for(int i=n; i > 1; --i)
	result *= i;

      for(uint32 i=0; i < N; ++i)
	{
	  for(uint32 j=ks[i]; j>1; --j)
	    result /= j;
	}
      return result;
    }

    // Bounded partition function
    // number of partition of number N into S pieces where every piece < X
    // implemented via recursion
    uint64 bounded_partition(const uint32& N, const uint32& S, const uint32& X)
    {
      if (S==0) return 0;
      if (S==1)
	{
	  if (N < X) return 1;
	  else return 0;
	}
    
      uint64 sum = 0;
      for (uint32 i = 0; i < X; ++i)
	sum += bounded_partition(N - i, S - 1, X);
      return sum;
    
    }
    
    inline uint64 get_next_pattern(const uint64& v)
    {
      // Bit twiddling Hack from
      // http://graphics.stanford.edu/~seander/bithacks.html
      // #NextBitPermutation
      uint64 t = (v | (v - 1)) + 1;  
      return t | ((((t & -t) / (v & -v)) >> 1) - 1);  
    }
    
    uint64 get_nth_pattern(const uint64& n, const uint64& n_upspins, const int& n_sites)
    {
      uint64 state = 0;
      uint64 counter = n;
      for (int n_varying_bits = n_upspins-1; n_varying_bits >= 0; --n_varying_bits)
	{
	  uint64 n_combinations = 0;
	  for(int n_allowed_pos = n_varying_bits; n_allowed_pos <= n_sites;
	      ++n_allowed_pos)
	    {
	      n_combinations += binomial(n_allowed_pos,n_varying_bits);

	      if( n_combinations > counter)
		{
		  counter -= n_combinations -
		    binomial(n_allowed_pos,n_varying_bits);
		  state |= (uint64(1) << n_allowed_pos);
		  break;
		}
	    }
	}
      return state;
    }

    // inverse of get_nth_pattern
    uint64 get_n_for_pattern(const uint64& pattern, const uint64& n_upspins,
			     const int& n_sites)
    {
      uint64 n=0;
      uint64 workpattern = pattern;
      for (int n_varying_bits = n_upspins-1; n_varying_bits >= 0;
	   --n_varying_bits)
	{
	  for (int i=0; i <= n_sites; ++i)
	    {
	      // MSB is at 2^i
	      if ((uint64(1) << (i+1)) > workpattern)
		{
		  n += binomial(i,n_varying_bits+1);
		  workpattern ^= (uint64(1) << i);
		  break;
		}
	    }
	}
      return n;
    }


    inline uint64 n_multisets(const uint32& nboxes, const uint32& nballs)
    { return binomial(nboxes + nballs - 1, nballs); }

    
    // function for enumerating all multisets with nballs elements taking nboxes values ...
    std::vector<uint32> get_nth_multiset(const uint32& nboxes, const uint32& nballs,
					 const uint32& num)
    {
      std::vector<uint32> multiset(nboxes, 0);

      uint64 stars_and_bars = get_nth_pattern(num, nballs, nboxes + nballs - 1);
      uint32 current_star = 0;
      for (uint32 current_star_or_bar = 0; current_star_or_bar < nboxes + nballs - 1;
	   ++ current_star_or_bar)
	{
	  if (gbit(stars_and_bars, current_star_or_bar) == 0)
            current_star += 1;
	  else
            multiset[current_star] += 1;
	}
      return multiset;
    }

    
    // ... and its inverse 
    uint32 get_n_for_multiset(const uint32& nboxes,const uint32& nballs,
			      const std::vector<uint32>& multiset)
    {
      uint64 stars_and_bars = 0;
      uint32 current_star_or_bar=0;
      for (uint32 current_star=0; current_star < multiset.size(); ++current_star)
	{
	  for (uint32 i = 0; i < multiset[current_star]; ++i)
	    {
	      stars_and_bars |= uint64(1) << current_star_or_bar;
	      current_star_or_bar += 1;
	    }
	  current_star_or_bar += 1;
	}
      return get_n_for_pattern(stars_and_bars, nballs, nboxes + nballs - 1);
    }
    
    
  }// end namespace combinatorics
}// end namespace quicked

#endif
