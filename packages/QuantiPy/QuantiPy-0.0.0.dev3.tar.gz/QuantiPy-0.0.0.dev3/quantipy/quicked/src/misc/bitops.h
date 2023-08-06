#ifndef QUICKED_MISC_BITOPS_H
#define QUICKED_MISC_BITOPS_H

#include <iostream>
#include <string.h>

inline unsigned int gbit(unsigned int x, long n) { return (x>>n)&(1U); }
inline unsigned long gbit(unsigned long x, long n) { return (x>>n)&(1UL); }
inline unsigned long long gbit(unsigned long long x,long n) {return (x>>n)&(1ULL);}

inline unsigned int maskr(unsigned int i) {return (i==32 ? 0xFFFFFFFFU : (1U<<i)-1 );}
inline unsigned long maskr(unsigned long i) {return ( i==32 ? 0xFFFFFFFFUL : (1UL<<i)-1 );}
inline unsigned long long maskr(unsigned long long i) {return ( i==64 ? 0xFFFFFFFFFFFFFFFFULL : (1ULL<<i)-1 ) ;}

inline long BX_(unsigned int x) { return ((x) - (((x)>>1)&0x77777777U)
		                              - (((x)>>2)&0x33333333U)
					      - (((x)>>3)&0x11111111U));}

inline long BX_(unsigned long x) { return ((x) - (((x)>>1)&0x77777777UL)
                                               - (((x)>>2)&0x33333333UL)
                                               - (((x)>>3)&0x11111111UL));}

inline unsigned long long BX_(unsigned long long x) {
  return (
	  (x)
	  -(((x)>>1)&0x7777777777777777ULL)
	  -(((x)>>2)&0x3333333333333333ULL)
	  -(((x)>>3)&0x1111111111111111ULL));
}

inline unsigned int popcnt(unsigned int x)
{ return    (((BX_(x)+(BX_(x)>>4)) & 0x0F0F0F0FU) % 255);}

inline unsigned int popcnt(unsigned long x) 
{ return    (((BX_(x)+(BX_(x)>>4)) & 0x0F0F0F0FUL) % 255);}

inline unsigned int popcnt(unsigned long long x)
{ return    (((BX_(x)+(BX_(x)>>4)) & 0x0F0F0F0F0F0F0F0FULL) % 255);}  

#endif
