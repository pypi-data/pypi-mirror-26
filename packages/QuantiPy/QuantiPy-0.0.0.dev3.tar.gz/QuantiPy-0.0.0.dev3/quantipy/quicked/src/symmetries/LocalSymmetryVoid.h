/** @file LocalSymmetryVoid.h
 *   
 *  @author Alexander Wietek  
 * 
 *  @version 0.1 
 *  @brief applying symmetries and finding representatives the naive way
 *  
 */

#ifndef __QUICKED_SYMMETRIES_LOCALSYMMETRYVOID_H__
#define __QUICKED_SYMMETRIES_LOCALSYMMETRYVOID_H__

#include "BasisState.h"
#include "HilbertSpace.h"

namespace quicked
{
  
  template<hilbert_t THilbertSpace>
  class LocalSymmetryVoid
  {
    typedef typename state_t<THilbertSpace>::type state_t;
  public:
    friend void swap(LocalSymmetryVoid& se1, LocalSymmetryVoid& se2){};
    inline uint32 n_symmetries() const {return 1;}
    inline void apply_symmetry(const int& num_sym, state_t* derivedstate) const {};
    inline double bloch(const uint32& idx) {return 1.0;}
  };
  
}

#endif
