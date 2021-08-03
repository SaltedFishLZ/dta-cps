#include "stdlib.h"
#include "stdint.h"

#include "util.h"

#define ITERS 1000

volatile float * float_in = (volatile float *)0x81000000; 
volatile float * float_out = (volatile float *)0x82000000; 


int main()
{
    // setStats(1);
    for (int i = 0; i < ITERS; i++) {
magic_start_stamp(0)
        // begin
        *float_out = (*float_in) + (rand()/(float)RAND_MAX) * 0.2;
        // end
magic_end_stamp(0)
    }
    // setStats(0);
    return 0;
}