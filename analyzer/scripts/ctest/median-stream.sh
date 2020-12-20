#!/bin/bash

cd /dta-cps/analyzer

# PROCESSOR=Scratchpad512KBRV32Config
PROCESSOR=DefaultRV32Config


WORKLOAD=median-stream
EMULATOR=$ROCKET/emulator/emulator-freechips.rocketchip.system-${PROCESSOR}
echo "${EMULATOR}"

EXP_DIR=expdir/ctest/${WORKLOAD}/${PROCESSOR}//

SRC_DIR="/dta-cps/workload/ctest/${WORKLOAD}/"

mkdir -p ${EXP_DIR} && \
cp ${SRC_DIR}/${WORKLOAD}.riscv ${EXP_DIR} && \
cp ${SRC_DIR}/${WORKLOAD}.dump.annot ${EXP_DIR}

ls $EXP_DIR


${EMULATOR} +verbose ${EXP_DIR}/${WORKLOAD}.riscv 2>${EXP_DIR}/${WORKLOAD}.log; \
python3 /dta-cps/analyzer/main.py ${EXP_DIR} ${WORKLOAD} --dump --sid 0
