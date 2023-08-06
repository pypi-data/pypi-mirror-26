/** @file HilbertSpaceSpinGenericDetail.h
 *  @brief Detail implementations for Generic Spin Hilbertspaces
 *  @author Alexander Wietek  
 */

#ifndef __QUICKED_HILBERTSPACES_HILBERTSPACESPINGENERICDETAIL_H__
#define __QUICKED_HILBERTSPACES_HILBERTSPACESPINGENERICDETAIL_H__

#include "BasisStateSUNDetail.h" // for _compress_state, _decompress_state

namespace quicked{
  namespace HilbertSpaceSpinGenericDetail
  {
    // Get starting spin configuration
    template <hilbert_t THilbertSpace, uint32 SPIN>
    uint64 _get_spin_start(const uint32& quantumnumber)
    {
      uint64 spin_start = 0;
      for(uint32 i = 0; i < quantumnumber/(SPIN-1); ++i)
	spin_start |= ((uint64)(SPIN-1) << (n_bits<THilbertSpace>::value*i));
      spin_start |= ((uint64)(quantumnumber % (SPIN-1)) <<
		     (n_bits<THilbertSpace>::value*(quantumnumber/(SPIN-1))));
      return spin_start;
    }

    // Get end spin configuration
    template <hilbert_t THilbertSpace, uint32 SPIN>
    uint64 _get_spin_end(const uint32 & n_sites, const uint32& quantumnumber)
    {
      uint64 spin_end = 0;
      for(uint32 i = 0; i < quantumnumber/(SPIN-1); ++i)
	spin_end |= ((uint64)(SPIN-1) << (n_bits<THilbertSpace>::value*(n_sites - 1 - i)));
      spin_end |= ((uint64)(quantumnumber % (SPIN-1)) <<
		     (n_bits<THilbertSpace>::value*(n_sites - 1 - quantumnumber/(SPIN-1))));
      return spin_end;
      
    }

    // get stopper spin configuration
    template <hilbert_t THilbertSpace, uint32 SPIN>
    uint64 _get_spin_stopper(const uint32 & n_sites, const uint32& quantumnumber)
    {
      uint64 state = _get_spin_end<THilbertSpace, SPIN>(n_sites, quantumnumber);
      uint64 state_compressed =
      	BasisStateSUNDetail::_compress_state<SPIN, uint64>(state) + 1;
      return BasisStateSUNDetail::_decompress_state<SPIN,uint64>(state_compressed);
      // quantumnumber_t<THilbertSpace>  qnstart =
      // 	get_quantumnumber<THilbertSpace>(state, n_sites);
      // quantumnumber_t<THilbertSpace> qn;

      // do
      // 	{
      // 	  ++state_compressed;
      // 	  state =
      // 	    BasisStateSUNDetail::_decompress_state<SPIN,uint64>(state_compressed);
      // 	  qn = get_quantumnumber<THilbertSpace>(state, n_sites);
      // 	  std::cout << qn.val << " " << state_string<THilbertSpace>(state, n_sites + 3) << std::endl;
      // 	} while(!(valid_quantumnumber<THilbertSpace>(qn, n_sites) &&
      // 		  (qn==qnstart)));

      // return state
	// ;
     }
    
    template <hilbert_t THilbertSpace, uint32 SPIN> // 2S + 1
    class iterator
    {
    public:
      typedef typename state_t<THilbertSpace>::type state_t;
      iterator(const uint32& _quantumnumber, const uint32& _n_sites,
	       const uint32& index)
	: n_sites_(_n_sites)
      {
	if (index == 0) // create start state
	  {
	    current_state_ = _get_spin_start<THilbertSpace, SPIN>(_quantumnumber);
	    current_state_compressed_ =
	      BasisStateSUNDetail::_compress_state<SPIN, uint64>(current_state_);
	  }	  
	else // create stopper
	  {
	    current_state_ =
	      _get_spin_stopper<THilbertSpace, SPIN>(n_sites_, _quantumnumber);
	    current_state_compressed_ =
	      BasisStateSUNDetail::_compress_state<SPIN, uint64>(current_state_); 
	  }
	 stopper_ = _get_spin_stopper<THilbertSpace, SPIN>(n_sites_, _quantumnumber);
      }

      
      inline bool operator==
      (const iterator& rhs) const 
      { return (current_state_ == rhs.current_state_); }

      inline bool operator!=
      (const iterator& rhs) const 
      {  return !operator==(rhs); }

      inline iterator& operator++() 
      {
	quantumnumber_t<THilbertSpace>  qnstart =
	  get_quantumnumber<THilbertSpace>(current_state_, n_sites_);
	quantumnumber_t<THilbertSpace> qn;
	do
	{
	  ++current_state_compressed_;
	  current_state_ = BasisStateSUNDetail::_decompress_state<SPIN, uint64>
	    (current_state_compressed_);
	  if (current_state_ == stopper_) return *this;
	  qn = get_quantumnumber<THilbertSpace>(current_state_, n_sites_);
	} while(!(valid_quantumnumber<THilbertSpace>(qn, n_sites_) &&
		  (qn==qnstart)));
	return *this;
      }
      
      inline state_t operator*() const
      { return current_state_; }
      
    private:
      uint32 n_sites_;
      state_t current_state_;
      state_t current_state_compressed_;
      state_t stopper_;
    };
    
   
      
  } // detail namespace 
} // QL namespace

#endif
