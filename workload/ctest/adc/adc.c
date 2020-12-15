#include "stdlib.h"
#include "stdint.h"

#include "util.h"

#define ITERS 1000

volatile uint8_t * sensor_in = (volatile uint8_t *)0x81000000; 
volatile uint8_t * driver_out = (volatile uint8_t *)0x82000000; 


int main()
{
    // setStats(1);
    for (int i = 0; i < ITERS; i++) {
magic_start_stamp(1)
        // begin
        uint8_t input = *sensor_in;
        float data = (float)(input) / 256.0;
        if (data > 0.5) {
            *driver_out = 100;
        }
        else
        {
            *driver_out = 50;
        }
        // end
magic_end_stamp(1)
    }
    // setStats(0);
    return 0;
}