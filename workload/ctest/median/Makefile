
XLEN ?= 32


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

median.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)

median.dump: median.riscv
	$(RISCV_OBJDUMP) $< > $@

median.dump.annot: median.riscv
	$(RISCV_OBJDUMP) -S $< > $@

all: median.riscv median.dump median.dump.annot

clean:
	-rm -rf *.riscv *.dump *.dump.annot



