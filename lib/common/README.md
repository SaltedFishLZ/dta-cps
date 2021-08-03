# Bare-metal C Library for RISC-V Emulators Based on fesvr/HTIF

## Introduction

This C library is adapted from [`riscv-tests`](https://github.com/riscv/riscv-tests/tree/master/benchmarks/common). It implements some basic system calls (e.g., `sbrk` and `vprintfmt`), a simple "bootloader", linking script and other utilies.

## Usage

To use this library, you need to compile your C codes with the following settings (assuming you will use Makefile).

* Set the gcc compiling options

  `RISCV_GCC_OPTS ?= -DPREALLOCATE=1 -mcmodel=medany -static -ffast-math -fno-common -fno-builtin-printf`

* Set the gcc linking options

  `RISCV_LINK_OPTS ?= -static -nostartfiles -lm -lgcc -T $PATH_TO_THIS_FOLDER/link.ld`

* Set the included files

  `incs  += -I$PATH_TO_THIS_FOLDER`

* Then compile the binary

  `$(YOUR_RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) $(RISCV_LINK_OPTS) -o $@ $YOUR_SOURCE_CODES $(wildcard $PATH_TO_THIS_FOLDER/*.c) $(wildcard $PATH_TO_THIS_FOLDER/*.S)`



Here is the an example for the helloworld program (`workload/ctest/hello`).

```makefile

src_dir = ../../../

# set up gcc path
RISCV_PREFIX ?= riscv$(XLEN)-unknown-elf-
RISCV_GCC ?= $(RISCV_PREFIX)gcc

RISCV_GCC_OPTS ?= \
				-DPREALLOCATE=1 -mcmodel=medany -static \
				-std=gnu99 \
				-Og -g \
				-ffast-math -fno-common -fno-builtin-printf

# set up gcc linking options
RISCV_LINK_OPTS ?= -static -nostartfiles -lm -lgcc -T $(src_dir)lib/common/link.ld

# set up objdump & options
RISCV_OBJDUMP ?= $(RISCV_PREFIX)objdump --disassemble-all --disassemble-zeroes \
				 --section=.text --section=.text.startup --section=.text.init --section=.data

# set up included files
incs  += -I$(src_dir)lib/common

hello.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)

```


Now, we can test it with `spike`. For example, run `spike hello.riscv`, and you will get the message printed. Running the binary on a Rocket Chip emulator is similar (Note: you need to build the correct 32-bit emulator. The default binary is compiled with riscv32-unknown-elf-gcc while the default Rocket Core configuration is 64-bit).



## Details

### System Calls (WIP)

These "system call"s use the RISC-V HTIF to communicate with the host side (in our case, the host side codes of the emulator). System calls will write/read the `fromhost` and `tohost` "registers" (actually, 2 magic memory address) to interact with the host.

For example, to print messages on the console (of course, the console of the host), we can call `putchar` to ***forward*** characters to the host, and then the host side codes will display the messages (implemented by riscv-fesvr, the RISC-V frontend server).

Note: I still do not fully understand the details of riscv-fesvr. It is a Berkeley-internal debug interface and there is no official document. I am still discussing with the authors.

References:

+ https://github.com/riscv/riscv-tests/issues/207


### The "Bootloader" (WIP)

The "bootloader" is very simple. Currently, it only contains the C runtime startup routines (crt.S) and only supports single core.

References:

+ https://en.wikipedia.org/wiki/Crt0
+ https://stackoverflow.com/questions/51684188/what-is-the-use-of-crt-s-file
+ http://www.vishalchovatiya.com/crt-run-time-before-starting-main/


### The Linking Script

`link.ld` specifies the memory address of each segement/symbol (e.g., `tohost` and the address of the heap) of the ELF binary.

