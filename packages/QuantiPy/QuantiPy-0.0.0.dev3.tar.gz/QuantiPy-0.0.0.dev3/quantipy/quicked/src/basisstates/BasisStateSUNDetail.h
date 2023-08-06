/** @file HilbertSpace_SUNDetail_incl.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Detailed implementations of SU(N) Hilbertspace functions
 *  
 */

#ifndef __QUICKED_BASISSTATES_BASISSTATESUNDETAIL_H__
#define __QUICKED_BASISSTATES_BASISSTATESUNDETAIL_H__

#include <string.h>

#include "BasisStateSpinhalfDetail.h"

#include "bitops.h"
#include "common.h"

namespace quicked{
namespace BasisStateSUNDetail
{
  // Define how many bits are used for SU(N)
  template <uint32 N>  inline uint32 n_bits_for_su();
  template <> inline uint32 n_bits_for_su<2>(){return 1;}
  template <> inline uint32 n_bits_for_su<3>(){return 2;}
  template <> inline uint32 n_bits_for_su<4>(){return 2;}
  template <> inline uint32 n_bits_for_su<5>(){return 3;}
  template <> inline uint32 n_bits_for_su<6>(){return 3;}
  template <> inline uint32 n_bits_for_su<7>(){return 3;}
  template <> inline uint32 n_bits_for_su<8>(){return 3;}

  // function to get a bitmask (i.e. something like (000000011100000)_2 )
  // at a specified site
  template<uint32 N, class T>
  inline T _get_site_mask(const uint32& site)
  {
    const uint32 nb = n_bits_for_su<N>(); 
    const uint32 nb_times_site = nb*site;
    return ((T)((1<<nb)-1) << nb_times_site);
  }

  // functions to get/set the color at a specified site for sun states
  template<uint32 N, class T> inline uint32 _get_site_value_sun
  (const T& state, const uint32& site)
  {
    T site_value = 0;
    for(uint32 b=0; b<n_bits_for_su<N>(); ++b) 
      site_value |= (gbit(state, n_bits_for_su<N>()*site+b)) << b; 
    return uint32(site_value);
  }

  template<uint32 N, class T>
  inline void _set_site_value_sun
  (T* state, const uint32& site, const uint32& value)
  {
    const uint32 nb = n_bits_for_su<N>(); 
    const uint32 nb_times_site = nb*site;
    const T mask  = ~((T)((1<<nb)-1) << nb_times_site);
    *state= (*state & mask) | ((T)value << nb_times_site);
  }

  template<uint32 N, class T>
  inline void _get_color_numbers
  (const T& state, const uint32& n_sites, uint32 (*n_in_colors)[N]);

  template<uint32 N>
  inline bool _valid_quantumnumber_sun
  (const uint32& n_sites,const uint32 (&n_in_colors)[N])
  { return uint32(std::accumulate(n_in_colors, n_in_colors+N, 0))==n_sites;}

  template <uint32 N> inline bool _less_equal(const uint32 (&a)[N],
					      const uint32 (&b)[N])
  {
    bool lessequal = true;
    for(uint32 i = 0; i < N; ++i) lessequal &= (a[i] <= b[i]);
    return lessequal;
  }

  template<uint32 N> inline void _add_arrays(const uint32 (&a)[N],
					     const uint32 (&b)[N],
					     uint32 (*res)[N])
  {for(uint32 i = 0; i < N; ++i) (*res)[i] = a[i] + b[i];}

  template<uint32 N> inline void _sub_arrays(const uint32 (&a)[N],
					     const uint32 (&b)[N],
					     uint32 (*res)[N])
  {for(uint32 i = 0; i < N; ++i) (*res)[i] = a[i] - b[i];}
  
  // various other helping functions for SU(N) Hilbertspaces 
  template <uint32 N> inline bool _valid_quantumnumbers
  (const uint32 (&n_in_colors)[N], const uint32& n_sites);
  template <uint32 N, class T> inline T _get_first_state
  (const uint32 (&n_in_colors)[N]);
  template <uint32 N, class T> inline T _get_last_state
  (const uint32 (&n_in_colors)[N]);
  template <uint32 N, class T> inline T _exchange_site_values
  (const uint64& state, const uint32& site1, const uint32& site2);
  template <uint32 N, class T> inline void _get_color_numbers
  (const T& state, const uint32& n_sites, uint32 (*n_in_colors)[N]);
  template <uint32 N, class T> T _compress_state(const T& state);
  template <uint32 N, class T> T _decompress_state(const T& state);
  template <uint32 N, class T> T _get_next_state(const T& state,
						 const uint32& n_sites);


  template <uint32 N, class T> inline std::string _state_string_sun
  (const T& state, const uint32& n_sites)
  {
    std::ostringstream ss;
    for (uint32 i = 0; i < n_sites-1; ++i)
      ss << _get_site_value_sun<N,T>(state, i);
    ss << _get_site_value_sun<N,T>(state, n_sites-1);
    return ss.str();
  }

  // function to check whether quantum numbers fit with n_sites
  template <uint32 N>
  inline bool _valid_quantumnumbers(const uint32 (&n_in_colors)[N], const uint32& n_sites)
  {
    uint32 sum = 0;
    for (uint32 i = 0; i < N; ++i) sum += n_in_colors[i];
    return sum == n_sites;
  }


  // function to get the first state of an SU(N) Hilbertspace
  template <uint32 N, class T> 
  inline T _get_first_state(const uint32 (&n_in_colors)[N])
  {
    T first_state(0);
    int siteshift = 0;
    for (uint32 coloridx = 0; coloridx < N; ++coloridx)
      for (uint32 i = 0; i < n_in_colors[N-1-coloridx]; ++i, ++siteshift)
	first_state |= T(N - 1 - coloridx) << (n_bits_for_su<N>()*siteshift);
    
    return first_state;
  }


  // function to get the last state of an SU(N) Hilbertspace
  template <uint32 N, class T> 
  inline T _get_last_state(const uint32 (&n_in_colors)[N])
  {
    T last_state(0);
    int siteshift = 0;
    for (uint32 coloridx = 0; coloridx < N; ++coloridx)
      for (uint32 i = 0; i < n_in_colors[coloridx]; ++i, ++siteshift)
	last_state |= T(coloridx) << (n_bits_for_su<N>()*siteshift);
    // for (uint32 i=0; i < N; ++i)
    //   std::cout << n_in_colors[i] << " ";
    // std::cout << std::endl;
    return last_state;
  }


  // function to get stopper state of an SU(N) Hilbertspace
  template <uint32 N, class T> 
  inline T _get_stopper(const uint32 (&n_in_colors)[N])
  {
    return T(-1);
    // uint32 min_color = 0;
    // while (n_in_colors[min_color] == 0) ++min_color;

    // uint32 second_min_color = min_color + 1;
    // while (n_in_colors[second_min_color] == 0) ++second_min_color;
        
    // T stopper(_get_first_state<N,T>(n_in_colors));
    // uint32 sum_nonzero_colors = 0;
    // for (uint32 i=second_min_color; i < N; ++i)
    //   sum_nonzero_colors += n_in_colors[i];
    // const uint32 n_sites = sum_nonzero_colors + n_in_colors[0];
    // stopper &= ~(_get_site_mask<N,T>(sum_nonzero_colors-1));
    // stopper |= T(min_color) << (n_bits_for_su<N>()*(sum_nonzero_colors-1));
    // stopper |= T(second_min_color) << (n_bits_for_su<N>()*n_sites);
    // for (uint32 i=0; i < N; ++i)
    //   std::cout << n_in_colors[i] << " ";
    // std::cout << std::endl << "ahoi " <<  _state_string_sun<N,T>(stopper, n_sites+2) << std::endl;
    // return stopper;
  }



  // function to exchange the two colors at two given sites
  template<uint32 N, class T>
  inline T _exchange_site_values(const T& state, const uint32& site1, const uint32& site2)
  {
    const T site1_mask = _get_site_mask<N, T>(site1);
    const T site2_mask = _get_site_mask<N, T>(site2);
    const T site1_bits = (site1 > site2  ? (site1_mask & state) >> ((site1 - site2)*n_bits_for_su<N>()) :
			       (site1_mask & state) << ((site2 - site1)*n_bits_for_su<N>()));
    const T site2_bits = (site2 > site1  ? (site2_mask & state) >> ((site2 - site1)*n_bits_for_su<N>()) :
			       (site2_mask & state) << ((site1 - site2)*n_bits_for_su<N>()));;  
    return (state & (~site1_mask) & (~site2_mask)) | site1_bits | site2_bits;
  }


  // function to get the number of colors for a specified state
  template<uint32 N, class T>
  inline void _get_color_numbers(const T& state, const uint32& n_sites, uint32 (*n_in_colors)[N])
  {
    memset(*n_in_colors, 0, sizeof(*n_in_colors));
    T workstate = state;
    const T site_zero_mask = ((T)1 << n_bits_for_su<N>()) - 1;
    for(uint32 i = 0; i < n_sites; ++i)
      {
	uint32 site_value = uint32(workstate & site_zero_mask);
	/* if (site_value < N) */
	++(*n_in_colors)[site_value];  // Error here means too big site Value
	workstate >>= n_bits_for_su<N>();
      }
  }


  // function to compress a state to N-ary representation 
  template<uint32 N, class T>
  T _compress_state(const T& state)
  {
    /* T state_compressed = 0; */
    /* T basis = 1; */
    /* for (uint32 i = 0; i < n_sites; ++i) */
    /*   { */
    /* 	state_compressed += _get_site_value<N>(state, i)*basis; */
    /* 	basis *= N; */
    /*   } */
    /* return state_compressed; */
    T state_compressed = 0;
    T workstate = state;
    T basis = 1;
    const T site_zero_mask = ((T)1 << n_bits_for_su<N>()) - 1;
    while (workstate != 0)
      {
	/* state_compressed += _get_site_value<N>(workstate, 0)*basis; */
	state_compressed += (workstate & site_zero_mask)*basis; 
	basis *= N;
	workstate >>= n_bits_for_su<N>();
      }
    return state_compressed;
  }


  // function to decompress a state from N-ary representation 
  template<uint32 N, class T>
    T _decompress_state(const T& state)
  {
    T state_decompressed = 0;
    T workstate = state;
    int shift = 0;
    while (workstate != 0)
      {
	state_decompressed |= ((T)(workstate%N)) << (n_bits_for_su<N>()*shift);
	++shift;
	workstate /= N;
      }
    return state_decompressed;
  }

  
  // Function from bit twiddling hacks for next bit permutation
  template <class T> inline T get_next_pattern(const T& v)
  {
    T t = (v | (v - 1)) + 1;  
    return t | ((((t & (0-t)) / (v & (0-v))) >> 1) - 1);  // inserted zero for multiprecision
  }
  template <> inline uint64 get_next_pattern<uint64>(const uint64& v)
  {return combinatorics::get_next_pattern(v);}



  // function to get the next state of a given state
  template <uint32 N, class T>
  T _get_next_state(const T& state, const uint32& n_sites)
  {
    uint32 original_n_in_colors[N];
    _get_color_numbers(state, n_sites, &original_n_in_colors);
    // std::cout << "last "  << _state_string_sun<N,T>(_get_last_state<N,T>(original_n_in_colors),7)
    // 	      << " ?? " << _state_string_sun<N,T>(state, 7)<<  std::endl;

    if (state == _get_last_state<N,T>(original_n_in_colors))
      return _get_stopper<N,T>(original_n_in_colors); // not fast but necessary

    // compress
    uint32 n_in_colors[N];
    T candidate_state = state;
    while(true)
      {
	candidate_state = get_next_pattern(candidate_state);
	_get_color_numbers(candidate_state, n_sites, &n_in_colors);

	bool state_has_right_color_numbers = true;
	for (uint32 i = 1; i < N; ++i) 
	  if (n_in_colors[i] != original_n_in_colors[i])
	    {
	      state_has_right_color_numbers = false;
	      goto moveon;
	    }
      moveon:
	if (state_has_right_color_numbers) break;
      }
    return candidate_state;
  }

  using quicked::utils::base_print;

  template <uint32 N, class T>
  T _get_nth_state(const uint64& n, const uint32 (&n_in_colors)[N], const uint32& n_sites)
  {
    // Return stopper if n is dimension of hilbertspace
    if (n == combinatorics::multinomial(n_sites, n_in_colors))
      return _get_stopper<N,T>(n_in_colors);
    
    // Get minimum color in quantumnumbers as active color
    uint32 active_color = 0;
    while (n_in_colors[active_color] == 0) ++active_color;

    T state = 0;
    const uint32 total_min_color = active_color;
    // for (uint32 i = 0; i < n_sites; ++i)
    //   _set_site_value_sun<N,T>(&state, i, total_min_color);

      
    // get array with minimum color set to zero und compute trailing colors
    uint32 remainder_colors[N] = {0};
    uint32 active_site = 0;
    for (uint32 coloridx = active_color; coloridx < N; ++coloridx)
      {
	remainder_colors[coloridx] = n_in_colors[coloridx];
	active_site += n_in_colors[coloridx];
      }
    --remainder_colors[active_color];
    --active_site;
    
    uint64 counter = n;

    // std::cout << "n="  <<n << std::endl;

    // std::cout << "active_color "  << active_color << std::endl;

    while(true)
      {
	uint64 n_combinations = combinatorics::multinomial(active_site, remainder_colors);
	// std::cout << "n_comb1 " <<  n_combinations  << " counter " << counter << std::endl;

	while(n_combinations <= counter)
	  {
	    
	    // n_combinations += combinatorics::multinomial(active_site, remainder_colors);
	    // if (n_combinations > counter)
	    //   break;
	    // std::cout << "remainder colors b " ;
	    // for (uint32 i = 0; i < N; ++i)
	    //   std::cout << remainder_colors[i] << " ";
	    // std::cout << std::endl;
	    // std::cout << "  n_comb2 " <<  n_combinations  << " counter " << counter << std::endl;

	    // advance leading color or site
	    
	    // Check whether there is a higher color left
	    uint32 c = active_color+1;
	    uint32 min_higher_color;
	    // bool higher_color_exists = false;
	    while (c<N)
	      {
		if (remainder_colors[c] > 0)
		  {
		    min_higher_color = c;
		    // higher_color_exists = true;
		    break;
		  }
		++c;
	      }
	    
	    // std::cout << "  active     color c " << active_color << std::endl;
	    // std::cout << "  min higher color c " << min_higher_color << std::endl;
	    // std::cout << "  remainder colors c " ;
	    // for (uint32 i = 0; i < N; ++i)
	    //   std::cout << remainder_colors[i] << " ";
	    // std::cout << std::endl;
	    // std::cout << "  c " << c << std::endl;
	    // Advance active color 
	    if (c<N)
	      {
		++remainder_colors[active_color];
		active_color = min_higher_color;
		--remainder_colors[min_higher_color];
		// std::cout << "  huhu" << std::endl;
		// std::cout << "  remainder colors i " ;
		// for (uint32 i = 0; i < N; ++i)
		//   std::cout << remainder_colors[i] << " ";
		// std::cout << std::endl;
		// std::cout << "  a_c " << active_color << ", a_s " << active_site <<std::endl;

	      }
	    // Advance active site
	    else
	      {
		// std::cout << "  bef haha" << std::endl;
		// std::cout << "  bef remainder colors i " ;
		// for (uint32 i = 0; i < N; ++i)
		//   std::cout << remainder_colors[i] << " ";
		// std::cout << std::endl;
		// std::cout << "  bef a_c " << active_color << ", a_s " << active_site <<std::endl;

		uint32 min_remainder_color = 1;
		while (remainder_colors[min_remainder_color] == 0) ++min_remainder_color;
		
		++remainder_colors[active_color];
		active_color = min_remainder_color;
		--remainder_colors[min_remainder_color];
		++remainder_colors[total_min_color];
		++active_site;
		// std::cout << "  aft haha" << std::endl;
		// std::cout << "  aft remainder colors i " ;
		// for (uint32 i = 0; i < N; ++i)
		//   std::cout << remainder_colors[i] << " ";
		// std::cout << std::endl;
		// std::cout << "  aft a_c " << active_color << ", a_s " << active_site <<std::endl;

	      }
	    n_combinations += combinatorics::multinomial(active_site, remainder_colors);
		    
	  }

	// std::cout << "before a_c " << active_color << ", a_s " << active_site <<std::endl;
	_set_site_value_sun<N,T>(&state, active_site, active_color);
	// std::cout << "state " << _state_string_sun<N,T>(state, n_sites+2) << std::endl;
	if (active_site == 0) break;
	
	counter -= n_combinations - combinatorics::multinomial(active_site, remainder_colors);
	
	active_color = 0;
	while (remainder_colors[active_color] == 0) ++active_color;

	--remainder_colors[active_color];

	active_site = 0;
	for (uint32 c = active_color; c < N; ++c)
	    active_site += remainder_colors[c];
	// std::cout << "after a_c " << active_color << ", a_s " << active_site <<std::endl;
	// std::cout << "remainder colors a " ;
	// for (uint32 i = 0; i < N; ++i)
	//   std::cout << remainder_colors[i] << " ";
	// std::cout << std::endl;

	// // std::cout << "n_comb " <<  n_combinations << std::endl;
	// std::cout << std::endl;
	// std::cout << std::endl;
	// std::cout << std::endl;
      }
    
    // state |= ((uint64)active_color << active_site*n_bits_for_su<N>());
    // std::cout << "finalstate " << _state_string_sun<N,T>(state, n_sites+2) << std::endl;
    // std::cout << "--------------------------------" << std::endl;

    return state;

    }
  
  template <uint32 N, class T> inline void _get_sun_quantumnumber
  (const T& state, const uint32& n_sites, uint32* val)
  {
    memset(val, 0, N*sizeof(uint32));
    for(uint32 i = 0; i< n_sites; ++i)
      ++val[_get_site_value_sun<N,T>(state, i)];    
  }

}}

#endif
