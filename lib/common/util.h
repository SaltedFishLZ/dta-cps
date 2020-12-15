// See LICENSE for license details.

#ifndef __UTIL_H
#define __UTIL_H

extern void setStats(int enable);

#include <stdint.h>
#include <sys/signal.h>

#define static_assert(cond) switch(0) { case 0: case !!(long)(cond): ; }

static int verify(int n, const volatile int* test, const int* verify)
{
  int i;
  // Unrolled for faster verification
  for (i = 0; i < n/2*2; i+=2)
  {
    int t0 = test[i], t1 = test[i+1];
    int v0 = verify[i], v1 = verify[i+1];
    if (t0 != v0) return i+1;
    if (t1 != v1) return i+2;
  }
  if (n % 2 != 0 && test[n-1] != verify[n-1])
    return n;
  return 0;
}

static int verifyDouble(int n, const volatile double* test, const double* verify)
{
  int i;
  // Unrolled for faster verification
  for (i = 0; i < n/2*2; i+=2)
  {
    double t0 = test[i], t1 = test[i+1];
    double v0 = verify[i], v1 = verify[i+1];
    int eq1 = t0 == v0, eq2 = t1 == v1;
    if (!(eq1 & eq2)) return i+1+eq1;
  }
  if (n % 2 != 0 && test[n-1] != verify[n-1])
    return n;
  return 0;
}

static void __attribute__((noinline)) barrier(int ncores)
{
  static volatile int sense;
  static volatile int count;
  static __thread int threadsense;

  __sync_synchronize();

  threadsense = !threadsense;
  if (__sync_fetch_and_add(&count, 1) == ncores-1)
  {
    count = 0;
    sense = threadsense;
  }
  else while(sense != threadsense)
    ;

  __sync_synchronize();
}

static uint64_t lfsr(uint64_t x)
{
  uint64_t bit = (x ^ (x >> 1)) & 1;
  return (x >> 1) | (bit << 62);
}

static uintptr_t insn_len(uintptr_t pc)
{
  return (*(unsigned short*)pc & 3) ? 4 : 2;
}

#ifdef __riscv
#include "encoding.h"
#endif

#define stringify_1(s) #s
#define stringify(s) stringify_1(s)
#define stats(code, iter) do { \
    unsigned long _c = -read_csr(mcycle), _i = -read_csr(minstret); \
    code; \
    _c += read_csr(mcycle), _i += read_csr(minstret); \
    if (cid == 0) \
      printf("\n%s: %ld cycles, %ld.%ld cycles/iter, %ld.%ld CPI\n", \
             stringify(code), _c, _c/iter, 10*_c/iter%10, _c/_i, 10*_c/_i%10); \
  } while(0)

#endif //__UTIL_H

/*
 * magic stamp for cycle-level timing probing
 * Zheng Liang
 * TODO:
 * automatic probe inserting;
 * multi-core support;
 * Questions:
 * can we disable -g compiling flag?
 */


/*
 * currently, to prevent gcc from optimizing out the symbols
 * in annotations, we use external symbol in linker script
 * since linker is the last step
 * Note: we use stamp +1 to force all stamp id to be translated
 * into an addi instruction, which is convinient for processing
 */

#ifndef NO_MAGIC_STAMP
extern volatile uint32_t magic_stamp;
// notice the valid id range !!!
// write (0x149A0000 | (stamp_id + 1))
#define magic_start_stamp(stamp_id) \
  magic_stamp = (0x149A0000 | (stamp_id + 1));
// write (0x149A0000 | (stamp_id + 1))
#define magic_end_stamp(stamp_id) \
  magic_stamp = (0x249A0000 | (stamp_id + 1));
#else
#define magic_start_stamp(stamp_id) ; // do nothing
#define magic_end_stamp(stamp_id)  ; // do nothing
#endif



// #ifndef NO_MAGIC_STAMP
// #define magic_stamp_addr (volatile uint32_t *)0x8F000000
// // write 0x8F_id_149A
// #define magic_start_stamp(stamp_id) \
//   *magic_stamp_addr = ((stamp_id & 0x00FF0000) | 0x149a);
// // write 0x8F_id_249a
// #define magic_end_stamp(stamp_id) \
//   *magic_stamp_addr = ((stamp_id & 0x00FF0000) | 0x249a);
// #else
// #define magic_start_stamp(stamp_id) ; // do nothing
// #define magic_end_stamp(stamp_id)  ; // do nothing
// #endif