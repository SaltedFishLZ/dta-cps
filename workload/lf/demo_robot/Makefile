
XLEN ?= 32


src_dir = ../../

#--------------------------------------------------------------------
# Build rules
#--------------------------------------------------------------------

RISCV_PREFIX ?= riscv$(XLEN)-unknown-elf-
RISCV_GCC ?= $(RISCV_PREFIX)gcc
RISCV_GCC_OPTS ?= \
	-DPREALLOCATE=1 \
	-mcmodel=medany \
	-static -std=gnu99 \
	-Og -g \
	-ffast-math -fno-common -fno-builtin-printf
RISCV_LINK ?= $(RISCV_GCC) -T $(src_dir)/common/test.ld $(incs)
RISCV_LINK_OPTS ?= -static -nostartfiles -lm -lgcc -T $(src_dir)/common/test.ld
RISCV_OBJDUMP ?= $(RISCV_PREFIX)objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.text.init --section=.data

incs  += -I$(src_dir)/common


deps := $(wildcard ./src-gen/*.c) \
		$(wildcard ./src-gen/*.h) \
		$(wildcard ./src-gen/core/*.c) \
		$(wildcard ./src-gen/core/*.h) \
		$(wildcard $(src_dir)/common/*.c) \
		$(wildcard $(src_dir)/common/*.S)


demo_robot_with_print.riscv: ${deps}
	$(RISCV_GCC) $(incs) $(RISCV_GCC_OPTS) $(RISCV_LINK_OPTS) -o $@ \
	$(wildcard ./*.c) \
	$(wildcard ./*.h) \
	$(wildcard $(src_dir)/common/*.c) \
	$(wildcard $(src_dir)/common/*.S)


demo_robot_with_print.dump: demo_robot_with_print.riscv
	$(RISCV_OBJDUMP) $< > $@

demo_robot_with_print.dump.annot: demo_robot_with_print.riscv
	$(RISCV_OBJDUMP) -S $< > $@


all: demo_robot_with_print.riscv demo_robot_with_print.dump demo_robot_with_print.dump.annot


clean:
	-rm -rf *.riscv *.dump *.dump.annot



