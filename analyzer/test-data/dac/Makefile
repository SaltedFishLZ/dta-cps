
XLEN ?= 32


src_dir = ../../../

RISCV_PREFIX ?= riscv$(XLEN)-unknown-elf-
RISCV_GCC ?= $(RISCV_PREFIX)gcc

RISCV_GCC_OPTS ?= \
				-DPREALLOCATE=1 -mcmodel=medany -static \
				-std=gnu99 \
				-Og -g \
				-ffast-math -fno-common -fno-builtin-printf

RISCV_LINK ?= $(RISCV_GCC) -T $(src_dir)lib/common/link.ld $(incs)
RISCV_LINK_OPTS ?= -static -nostartfiles -lm -lgcc -T $(src_dir)lib/common/link.ld

RISCV_OBJDUMP ?= $(RISCV_PREFIX)objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.text.init --section=.data

incs  += -I$(src_dir)lib/common

dac.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)

dac.nostamp.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) -D NO_MAGIC_STAMP $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)

dac.dump: dac.riscv
	$(RISCV_OBJDUMP) $< > $@

dac.dump.annot: dac.riscv
	$(RISCV_OBJDUMP) -S $< > $@

dac.nostamp.dump.annot: dac.nostamp.riscv
	$(RISCV_OBJDUMP) -S $< > $@

all: dac.riscv dac.nostamp.riscv dac.dump dac.dump.annot dac.nostamp.dump.annot

clean:
	-rm -rf *.riscv *.dump *.dump.annot



