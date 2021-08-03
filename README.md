# Deterministic Timing-Aware Cyber-Physical Systems

## Folder Nagivation




## Quickstart


## Hardware

### Memory Map

```
          0 -     1000 ARWX  debug-controller@0
            3000 -     4000 ARWX  error-device@3000
           10000 -    20000  R X  rom@10000
         2000000 -  2010000 ARW   clint@2000000
         c000000 - 10000000 ARW   interrupt-controller@c000000
        60000000 - 80000000  RWX  mmio-port-axi4@60000000
        80000000 - 90000000  RWXC memory@80000000
```

## RTL-based Cycle-level Emulator

### Build Rocket Emulators

* Download the modified rocket-chip repo: https://github.com/SaltedFishLZ/rocket-chip
* Use `CONFIG=DefaultRV32Config` to build a default 32-bit Rocket system (Please check `rocket-chip/src/main/scala/system/Configs.scala`)

### Using GDB on Emulators


