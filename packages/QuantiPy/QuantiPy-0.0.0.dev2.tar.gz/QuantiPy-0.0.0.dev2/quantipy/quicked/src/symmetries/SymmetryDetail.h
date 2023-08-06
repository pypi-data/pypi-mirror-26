/** @file SymmetryDetail.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @version 0.1 
 *  @brief helping functions for symmetry engines
 *  
 */

#ifndef __QUICKED_SYMMETRIES_SYMMETRYDETAIL_H__
#define __QUICKED_SYMMETRIES_SYMMETRYDETAIL_H__

#include <algorithm>
#include <string>
#include <sstream>

#include "BasisState.h"
#include "HilbertSpace.h"

#include "common.h"

namespace quicked {
  namespace SymmetryDetail
  {
    bool is_valid_permutation(const std::vector<uint32>& permutation)
    {
      for (uint32 i = 0; i < permutation.size(); ++i)
	if (std::find(permutation.begin(), permutation.end(), i) == permutation.end())
	  return false;
      return true;  
    }

    template<hilbert_t THilbertSpace>
    inline typename state_t<THilbertSpace>::type apply_permutation
    (const typename state_t<THilbertSpace>::type& state, const uint32& n_sites,
     const uint32* permutation)
    {
      typename state_t<THilbertSpace>::type tstate = 0;
      for(uint32 i=0; i < n_sites; ++i)
	{
	  const uint32 val = get_site_value<THilbertSpace>(state, i);
	  set_site_value<THilbertSpace>(&tstate, permutation[i], val);
	}
      return tstate;
    }

    bool is_valid_symmetry_collection(const std::vector<std::vector<uint32> >& symmetries)
    {
      bool is_valid = true;
      const uint32 n_sites = symmetries[0].size();
      for (uint32 i = 0; i < symmetries.size(); ++i)
	is_valid &= ((symmetries[i].size() == n_sites) && (is_valid_permutation(symmetries[i])));
      return is_valid;
    }

    std::string to_string(const std::vector<uint32>& symmetry)
    {
      std::ostringstream ss;
      for (uint32 i = 0; i < symmetry.size(); ++i)
	ss << symmetry[i] << " ";
      return ss.str();
    }
    
  }
}
#endif
