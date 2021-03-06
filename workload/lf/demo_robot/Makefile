
XLEN ?= 32

src_dir = ../../../

RISCV_PREFIX ?= riscv$(XLEN)-unknown-elf-
RISCV_GCC ?= $(RISCV_PREFIX)gcc

RISCV_GCC_OPTS ?= \
				-DPREALLOCATE=1 -mcmodel=medany -static \
				-std=gnu99 \
				-Og -g\
				-ffast-math -fno-common -fno-builtin-printf

RISCV_LINK ?= $(RISCV_GCC) -T $(src_dir)lib/common/link.ld $(incs)
RISCV_LINK_OPTS ?= -static -nostartfiles -lm -lgcc -T $(src_dir)lib/common/link.ld

RISCV_OBJDUMP ?= $(RISCV_PREFIX)objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.text.init --section=.data

incs  += -I$(src_dir)lib/common

demo_robot.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)

demo_robot.dump: demo_robot.riscv
	$(RISCV_OBJDUMP) $< > $@

demo_robot.dump.annot: demo_robot.riscv
	$(RISCV_OBJDUMP) -S $< > $@


demo_robot_printf.riscv: $(wildcard ./*.c) $(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) -D PRINTF $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard $(src_dir)lib/common/*.c) $(wildcard $(src_dir)lib/common/*.S)

demo_robot_printf.dump: demo_robot_printf.riscv
	$(RISCV_OBJDUMP) $< > $@

demo_robot_printf.dump.annot: demo_robot_printf.riscv
	$(RISCV_OBJDUMP) -S $< > $@


all: demo_robot.riscv demo_robot.dump demo_robot.dump.annot \
	 demo_robot_printf.riscv demo_robot_printf.dump demo_robot_printf.dump.annot

clean:
	-rm -rf *.riscv *.dump *.dump.annot



