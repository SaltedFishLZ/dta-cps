
XLEN ?= 32


src_dir = ../../

RISCV_PREFIX ?= riscv$(XLEN)-unknown-elf-
RISCV_GCC ?= $(RISCV_PREFIX)gcc

RISCV_GCC_OPTS ?= \
				-DPREALLOCATE=1 -mcmodel=medany -static \
				-std=gnu99 \
				-Og -g \
				-ffast-math -fno-common -fno-builtin-printf

RISCV_LINK ?= $(RISCV_GCC) -T $(src_dir)/common/test.ld $(incs)
RISCV_LINK_OPTS ?= -static -nostartfiles -lm -lgcc -T $(src_dir)/common/test.ld

RISCV_OBJDUMP ?= $(RISCV_PREFIX)objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.text.init --section=.data

incs  += -I$(src_dir)/common

noise.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)/common/*.c) $(wildcard $(src_dir)/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)/common/*.c) $(wildcard $(src_dir)/common/*.S)

noise.nostamp.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)/common/*.c) $(wildcard $(src_dir)/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) -D NO_MAGIC_STAMP $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)/common/*.c) $(wildcard $(src_dir)/common/*.S)

noise.dump: noise.riscv
	$(RISCV_OBJDUMP) $< > $@

noise.dump.annot: noise.riscv
	$(RISCV_OBJDUMP) -S $< > $@

noise.nostamp.dump.annot: noise.nostamp.riscv
	$(RISCV_OBJDUMP) -S $< > $@

all: noise.riscv noise.nostamp.riscv noise.dump noise.dump.annot noise.nostamp.dump.annot

clean:
	-rm -rf *.riscv *.dump *.dump.annot



