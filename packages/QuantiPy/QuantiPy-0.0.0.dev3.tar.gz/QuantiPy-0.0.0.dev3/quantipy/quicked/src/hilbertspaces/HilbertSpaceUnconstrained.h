/** @file HilbertSpace_SpinHalf_incl.h
 *  @brief Template Specialization for Unconstrained Hilbertspaces
 *  @author Alexander Wietek  
 */

#ifndef __QUICKED_HILBERTSPACES_HILBERTSPACEUNCONSTRAINED_H__
#define __QUICKED_HILBERTSPACES_HILBERTSPACEUNCONSTRAINED_H__

#include "HilbertSpace.h"
#include "BasisState.h"
#include "BasisStateUnconstrained.h"
#include <math.h>

namespace quicked
{

  template <uint32 LocalDim, class state_t>
  class HilbertSpaceUnconstrained
  {
  public:
    HilbertSpaceUnconstrained(const uint32& _n_sites)
      : n_sites__(_n_sites)
    {}
      
    inline state_t operator[](const uint64& idx) const
    {
      state_t comp = idx;
      return BasisStateSUNDetail::_decompress_state<LocalDim, state_t>(comp);
    }
    inline uint64 index(const state_t& state) const
    { return BasisStateSUNDetail::_compress_state<LocalDim, state_t>(state); }
    
  protected:
    inline state_t get_first_state() const
    {return 0;}
    inline state_t get_next_state(const state_t& state) const 
    {
      state_t comp = BasisStateSUNDetail::_compress_state<LocalDim, state_t>(state);
      comp += 1; 
      return BasisStateSUNDetail::_decompress_state<LocalDim, state_t>(comp);
    }
    inline state_t get_last_state() const
    {
      state_t comp = (state_t)pow(LocalDim, n_sites__) - 1;
      return BasisStateSUNDetail::_decompress_state<LocalDim, state_t>(comp);
    }
    inline state_t get_stopper() const
    {
      state_t comp = (state_t)pow(LocalDim, n_sites__);
      return BasisStateSUNDetail::_decompress_state<LocalDim, state_t>(comp);
    }
  private:
    const uint32 n_sites__;
  };

  
  ///////////////////////////////////////////////////////////////
  // SpinHalf HilbertSpace Template Specialization
  ///////////////////////////////////////////////////////////////
  
  template <> inline uint32 local_dimension<HILBERTSPACE_2_TYPE>() {return 2;}
  template <> inline uint32 local_dimension<HILBERTSPACE_3_TYPE>() {return 3;}
  template <> inline uint32 local_dimension<HILBERTSPACE_4_TYPE>() {return 4;}
  template <> inline uint32 local_dimension<HILBERTSPACE_5_TYPE>() {return 5;}
  template <> inline uint32 local_dimension<HILBERTSPACE_6_TYPE>() {return 6;}
  template <> inline uint32 local_dimension<HILBERTSPACE_7_TYPE>() {return 7;}
  template <> inline uint32 local_dimension<HILBERTSPACE_8_TYPE>() {return 8;}
  

  template <>
  class HilbertSpace<HILBERTSPACE_2_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_2_TYPE>,
    public HilbertSpaceUnconstrained<2, uint64>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_2_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_2_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_2_TYPE>& b);
    
  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_2_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_2_TYPE>(const uint32& _n_sites,
				      const qn_t& _quantumnumber)
      : HilbertSpaceBase<HILBERTSPACE_2_TYPE>(_n_sites, (uint32)pow(2, _n_sites)),
      HilbertSpaceUnconstrained<2, uint64>(_n_sites),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { }

    inline qn_t quantumnumber() const { const qn_t qn = {0}; return qn; } 
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     

  private:
    const iterator begin_;
    const iterator end_;
  };


  template <>
  class HilbertSpace<HILBERTSPACE_3_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_3_TYPE>,
    public HilbertSpaceUnconstrained<3, uint64>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_3_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_3_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_3_TYPE>& b);
    
  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_3_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_3_TYPE>(const uint32& _n_sites,
				      const qn_t& _quantumnumber)
      : HilbertSpaceBase<HILBERTSPACE_3_TYPE>(_n_sites, (uint32)pow(3, _n_sites)),
      HilbertSpaceUnconstrained<3, uint64>(_n_sites),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { }

    inline qn_t quantumnumber() const { const qn_t qn = {0}; return qn; } 
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     

  private:
    const iterator begin_;
    const iterator end_;
  };

  
  template <>
  class HilbertSpace<HILBERTSPACE_4_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_4_TYPE>,
    public HilbertSpaceUnconstrained<4, uint64>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_4_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_4_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_4_TYPE>& b);
    
  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_4_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_4_TYPE>(const uint32& _n_sites,
				      const qn_t& _quantumnumber)
      : HilbertSpaceBase<HILBERTSPACE_4_TYPE>(_n_sites, (uint32)pow(4, _n_sites)),
      HilbertSpaceUnconstrained<4, uint64>(_n_sites),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { }

    inline qn_t quantumnumber() const { const qn_t qn = {0}; return qn; } 
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     

  private:
    const iterator begin_;
    const iterator end_;
  }; 


  template <>
  class HilbertSpace<HILBERTSPACE_5_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_5_TYPE>,
    public HilbertSpaceUnconstrained<5, uint64>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_5_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_5_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_5_TYPE>& b);
    
  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_5_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_5_TYPE>(const uint32& _n_sites,
				      const qn_t& _quantumnumber)
      : HilbertSpaceBase<HILBERTSPACE_5_TYPE>(_n_sites, (uint32)pow(5, _n_sites)),
      HilbertSpaceUnconstrained<5, uint64>(_n_sites),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { }

    inline qn_t quantumnumber() const { const qn_t qn = {0}; return qn; } 
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     

  private:
    const iterator begin_;
    const iterator end_;
  };

  
  template <>
  class HilbertSpace<HILBERTSPACE_6_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_6_TYPE>,
    public HilbertSpaceUnconstrained<6, uint64>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_6_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_6_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_6_TYPE>& b);
    
  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_6_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_6_TYPE>(const uint32& _n_sites,
				      const qn_t& _quantumnumber)
      : HilbertSpaceBase<HILBERTSPACE_6_TYPE>(_n_sites, (uint32)pow(6, _n_sites)),
      HilbertSpaceUnconstrained<6, uint64>(_n_sites),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { }

    inline qn_t quantumnumber() const { const qn_t qn = {0}; return qn; } 
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     

  private:
    const iterator begin_;
    const iterator end_;
  }; 


  
  template <>
  class HilbertSpace<HILBERTSPACE_7_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_7_TYPE>,
    public HilbertSpaceUnconstrained<7, uint64>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_7_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_7_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_7_TYPE>& b);
    
  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_7_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_7_TYPE>(const uint32& _n_sites,
				      const qn_t& _quantumnumber)
      : HilbertSpaceBase<HILBERTSPACE_7_TYPE>(_n_sites, (uint32)pow(7, _n_sites)),
      HilbertSpaceUnconstrained<7, uint64>(_n_sites),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { }

    inline qn_t quantumnumber() const { const qn_t qn = {0}; return qn; } 
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     

  private:
    const iterator begin_;
    const iterator end_;
  };


  template <>
  class HilbertSpace<HILBERTSPACE_8_TYPE> :
    public HilbertSpaceBase<HILBERTSPACE_8_TYPE>,
    public HilbertSpaceUnconstrained<8, uint64>
  {
    friend class HilbertSpaceDetail::iterator<HILBERTSPACE_8_TYPE>;
    friend bool operator==<>(const HilbertSpace<HILBERTSPACE_8_TYPE>& a,
			     const HilbertSpace<HILBERTSPACE_8_TYPE>& b);
    
  public:
    typedef HilbertSpaceDetail::iterator<HILBERTSPACE_8_TYPE> iterator;

    HilbertSpace<HILBERTSPACE_8_TYPE>(const uint32& _n_sites,
				      const qn_t& _quantumnumber)
      : HilbertSpaceBase<HILBERTSPACE_8_TYPE>(_n_sites, (uint32)pow(8, _n_sites)),
      HilbertSpaceUnconstrained<8, uint64>(_n_sites),
      begin_(iterator(*this, 0)),
      end_(iterator(*this, -1))	
    { }

    inline qn_t quantumnumber() const { const qn_t qn = {0}; return qn; } 
    inline const iterator& begin() const { return begin_; };
    inline const iterator& end() const { return end_;};     

  private:
    const iterator begin_;
    const iterator end_;
  }; 


  
}

#endif

