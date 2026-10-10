# CS-441 Computer Architecture Project 1

Brad Ames, Evan Huizinga, Zion Andrade, Nathan Ulmen, Isaac Hager

## Running

```sh
python3 main.py -<r|s> <program_file> 
```

EX:
```sh
python3 main.py -r test.txt
```

## Progress

Status describes the handlers in `main.py`. **Implemented** means the handler has
logic; it does not necessarily mean the instruction is connected to execution.
Registers currently store 24-bit values (writes are masked with `0xFFFFFF`).

All implemented handlers are connected to the execution lookup, including the
extra `DIV` instruction and the temporary `LDR` implementation. Stub instructions
are excluded and raise `KeyError` if used.

### ALU - 14

| Instruction | Handler status | Available through lookup |
| --- | --- | --- |
| ADD | Implemented | Yes |
| SUB | Implemented | Yes |
| MUL | Implemented | Yes |
| SDIV | Stub | No |
| UDIV | Stub | No |
| AND | Implemented | Yes |
| OR | Implemented | Yes |
| XOR | Implemented | Yes |
| BIC | Implemented | Yes |
| NOT | Implemented | Yes |
| MOV | Implemented | Yes |
| LSL | Implemented | Yes |
| LSR | Implemented | Yes |
| TEQ | Stub | No |

`DIV` is implemented using Python integer floor division, but is not part of the
32-opcode ISA. It does not replace the separate `SDIV` and `UDIV` stubs.

### MEM - 4

| Instruction | Handler status | Available through lookup |
| --- | --- | --- |
| LDR | Temporary immediate load; does not read memory | Yes |
| STR | Stub (`str_`) | No |
| LDI | Stub | No |
| STI | Stub | No |

Currently, `LDR 0x10 R1` writes the value `0x10` into `R1`, rather than loading
from address `0x10`. Memory is not implemented yet.

### FP - 5

| Instruction | Handler status | Available through lookup |
| --- | --- | --- |
| FADD | Stub | No |
| FSUB | Stub | No |
| FMUL | Stub | No |
| FDIV | Stub | No |
| FCMP | Stub | No |

### CONTROL - 7

| Instruction | Handler status | Available through lookup |
| --- | --- | --- |
| B | Register target supported; immediate target unsupported | Yes |
| BEQ | Implemented (register target) | Yes |
| BNE | Implemented (register target) | Yes |
| BGT | Implemented (register target) | Yes |
| BLT | Implemented (register target) | Yes |
| BGE | Implemented (register target) | Yes |
| BLE | Implemented (register target) | Yes |

### OTHER - 2

| Instruction | Handler status | Available through lookup |
| --- | --- | --- |
| NOP | Implemented | Yes |
| HALT | Implemented | Yes |

### Known issues and ISA ambiguities

- `LSL` shifts left and `LSR` shifts right, following the ISA mnemonics and
  descriptions rather than the reversed RTL in the supplied table.
- `B` takes a register target (for example, `B R1`), so the ISA example `B 0x80`
  raises `KeyError`. The current PC indexes parsed instructions; any mapping from
  ISA memory addresses to instruction indexes still needs to be defined.
- Ordered branches compare the stored nonnegative register values. If signed
  comparisons are intended, 24-bit two's-complement values need conversion first;
  the table does not specify comparison signedness.
- The parser accepts whitespace-separated operands, not the comma-separated
  syntax in the ISA table. Use `ADD R1 R2 R3` for now.
- Stub handlers return `None`; wiring them in without implementing them would
  leave the PC unchanged.
