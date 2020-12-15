#!/bin/bash


EXP=0
EXP_DIR=experiments/${EXP}/

SEC=10
EMULATOR=$ROCKET/emulator/emulator-freechips.rocketchip.system-DefaultRV32Config

mkdir -p ${EXP_DIR} && \
cp /dta-cps/workload/lf/demo_robot/demo_robot.riscv ${EXP_DIR} && \
cp /dta-cps/workload/lf/demo_robot/demo_robot.dump.annot ${EXP_DIR} && \
timeout ${SEC}s  ${EMULATOR} +verbose ${EXP_DIR}/demo_robot.riscv 2>${EXP_DIR}demo_robot.log && \
python3 /dta-cps/analyzer/main.py ${EXP_DIR} demo_robot --dump --sid 0 1 2 3 4 5 6
