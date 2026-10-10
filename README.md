# CS-441 Computer Architecture Project 1

Brad Ames, Evan Huizinga, Zion Andrade, Nathan Ulmen, Isaac Hager

## Running

```sh
python3 main.py -<r|s> <program_file>  <memory_file>
```

EX:
```sh
python3 main.py -r MINFINDER.txt FINDER.mem
```

## Progress

## TODO
Implement remaining instructions and look into the specs that the memory file defines. Right now 
we dont act differently if bits stored at each address are different.
* Step by step execution of program


### ALU - 14

* ADD - **DONE**
* SUB - **DONE**
* MUL - **DONE**
* SDIV
* UDIV
* AND - **DONE**
* OR - **DONE**
* XOR - **DONE**
* BIC - **DONE**
* NOT - **DONE**
* MOV - **DONE**
* LSL - **DONE**
* LSR - **DONE**
* TEQ

### MEM - 4

* LDR - **DONE**
* STR - **DONE**
* LDI - **DONE**
* STI - **DONE**


### FP - 5

* FADD
* FSUB
* FMUL
* FDIV
* FCMP

### CONTROL - 7

* B - **DONE (register target only)**
* BEQ - **DONE**
* BNE - **DONE**
* BGT - **DONE**
* BLT - **DONE**
* BGE - **DONE**
* BLE - **DONE**

### OTHER - 2

* NOP - **DONE**
* HALT - **DONE**
