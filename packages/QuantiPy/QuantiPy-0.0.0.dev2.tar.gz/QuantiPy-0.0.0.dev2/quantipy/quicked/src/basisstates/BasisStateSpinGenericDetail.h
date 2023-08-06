/** @file BasisStateSpinGenericDetail.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @brief Detailed implementations of Spinhalf Hilbertspace functions
 *  
 */

#ifndef __QUICKED_BASISSTATES_BASISSTATESPINGENERICDETAIL_H__
#define __QUICKED_BASISSTATES_BASISSTATESPINGENERICDETAIL_H__

#include "bitops.h"
#include "common.h"

namespace quicked{
  ///////////////////////////////////////////////////////////////
  //Implementation of Detail namespace
  namespace BasisStateSpinGenericDetail
  {
    template<uint32 NBits>
    void _get_sz(const uint64& state, const uint32& n_sites, uint32* sz)
    {
      uint64 workstate = state;
      *sz=0;
      while (workstate)
	{
	  *sz += (workstate & ((1 << NBits)-1));
	  workstate >>= NBits;
	}
    }
    
  }
}

#endif
