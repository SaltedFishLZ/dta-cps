# Bare-metal C Library for RISC-V Emulators Based on fesvr/HTIF

## Introduction

This C library is adapted from [`riscv-tests`](https://github.com/riscv/riscv-tests/tree/master/benchmarks/common). It implements some basic system calls (e.g., `sbrk` and `vprintfmt`), a simple "bootloader", linking script and other utilies.

## Usage

```makefile

RISCV_GCC_OPTS ?= \
				-DPREALLOCATE=1 -mcmodel=medany -static \
				-std=gnu99 \
				-Og -g \
				-ffast-math -fno-common -fno-builtin-printf

# set linking script
RISCV_LINK_OPTS ?= -static -nostartfiles -lm -lgcc -T $(src_dir)lib/common/link.ld


incs  += -I$(src_dir)lib/common


```



## Details

### System Calls

These "system call"s use the RISC-V HTIF to communicate with the host side (in our case, the host side codes of the emulator). System calls will write/read the `fromhost` and `tohost` "registers" (actually, 2 magic memory address) to interact with the host.
*
For example, to print messages on the console (of course, the console of the host), we can call `putchar` to ***forward*** characters to the host, and then the host side codes will display the messages (implemented by riscv-fesvr, the RISC-V frontend server).


### The "Bootloader"

The "bootloader" is very simple. Currently, it only contains the c runtime startup routines (crt.S)

References:

https://en.wikipedia.org/wiki/Crt0


