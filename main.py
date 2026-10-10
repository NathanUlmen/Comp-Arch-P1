import sys

class Instruction:

    def __init__(self, opcode : str, operands : list) -> None:
        self.opcode = opcode
        self.operands = operands

    def __str__(self):
        s = f"{self.opcode}"
        for operand in self.operands:
            s += " " + operand
        return s

class CPU:

    def __init__(self) -> None:
        self.should_halt = False
        self.program_counter = 0
        self.registers = {f"R{i}" : 0 for i in range(16)}
        self.registers["PC"] = 0
        self.flags = {
            "negative" : False, 
            "zero" : False,
            "carry" : False,
            "overflow" : False,
            "saturation" : False
        }

    def __str__(self) -> str:
        output = [
            "===== CPU STATE =====",
            f"Program Counter: {self.program_counter}",
            f"Halted: {self.should_halt}",
            "",
            "----- REGISTERS -----"
        ]

        for register, value in self.registers.items():
            output.append(f"{register:>3}: 0x{value:08X} ({value})")

        output.append("")
        output.append("------ FLAGS ------")

        for flag, value in self.flags.items():
            output.append(f"{flag.capitalize():<12}: {int(value)}")

        return "\n".join(output)


    # IDK if we will use this, but we might need it 
    def write_register(self, target : str, value : int):
        self.registers[target] = value & 0xFFFFFF

    def set_program_counter(self, value : int):
        self.program_counter = value
        self.registers["PC"] = value


def main() -> None:
    args = sys.argv[1:]
    run_mode = args[0] # TODO: implement different run modes, does nothing currently
    program_file = args[1]
    memory_file = "test.mem" # TODO: udpate once we have memory figured out

    file_as_str = None
    with open(program_file) as file:
        file_as_str = file.read()

    program = parse_program(file_as_str)
    for i in program:
        print(i)
    execute_program(program)

def parse_program(program : str) -> list[Instruction]:
    program_instrs = []
    for line in program.splitlines():
        split_line = line.split("//", 1)[0].split() # strip out comments and then split on whitespace
        if len(split_line) > 0:
            instr = Instruction(split_line[0].upper(), split_line[1:])
            program_instrs.append(instr)
    
    return program_instrs


def execute_program(program : list[Instruction]) -> CPU:
    cpu = CPU()
    while not cpu.should_halt:
        instr = program[cpu.program_counter]
        execute_instr(cpu, instr)

    print(cpu)
    return cpu

def execute_instr(cpu : CPU, instr: Instruction) -> None:
    # All instructions MUST return a bool that indicates whether or not
    # the program counter is incremented. Branch instrs will opt out of this
    lookup = {
        "LDR" : ldr,
        "HALT" : halt,
        "ADD" : add,
        "SUB" : sub,
        "MUL" : mul,
        "DIV" : div,
        "MOV" : mov
    }
    if lookup[instr.opcode](cpu, instr.operands):
        cpu.set_program_counter(cpu.program_counter + 1)

# ALU
def add(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] + cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def sub(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] - cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def mul(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] * cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def div(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] // cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def mov(cpu : CPU, operands : list[str]) -> bool:
    cpu.write_register(operands[0], cpu.registers[operands[1]])
    return True

def sdiv(cpu : CPU, operands : list[str]) -> bool:
    pass

def udiv(cpu : CPU, operands : list[str]) -> bool:
    pass

def and_(cpu : CPU, operands : list[str]) -> bool:
    pass

def or_(cpu : CPU, operands : list[str]) -> bool:
    pass

def xor(cpu : CPU, operands : list[str]) -> bool:
    pass

def bic(cpu : CPU, operands : list[str]) -> bool:
    pass

def not_(cpu : CPU, operands : list[str]) -> bool:
    pass

def lsl(cpu : CPU, operands : list[str]) -> bool:
    pass

def lsr(cpu : CPU, operands : list[str]) -> bool:
    pass

def teq(cpu : CPU, operands : list[str]) -> bool:
    pass

# Memory
def ldr(cpu : CPU, operands : list[str]) -> bool:
    # TODO: this currently functions like ldri
    # Once memory if figured out needs to be udpated to pull value at address instead
    cpu.write_register(operands[1], int(operands[0], 16))
    return True

def ldi(cpu : CPU, operands : list[str]) -> bool:
    pass

def store(cpu: CPU, operands : list[str]) -> bool:
    pass

def str_(cpu : CPU, operands : list[str]) -> bool:
    pass

def sti(cpu : CPU, operands : list[str]) -> bool:
    pass

# Floating point
def fadd(cpu : CPU, operands : list[str]) -> bool:
    pass

def fsub(cpu : CPU, operands : list[str]) -> bool:
    pass

def fmul(cpu : CPU, operands : list[str]) -> bool:
    pass

def fdiv(cpu : CPU, operands : list[str]) -> bool:
    pass

def fcmp(cpu : CPU, operands : list[str]) -> bool:
    pass

# Control
def b(cpu : CPU, operands : list[str]) -> bool:
    pass

def eq(cpu: CPU, operands : list[str]) -> bool:
    pass

def blt(cpu: CPU, operands : list[str]) -> bool:
    pass

def beq(cpu: CPU, operands : list[str]) -> bool:
    pass

def bne(cpu : CPU, operands : list[str]) -> bool:
    pass

def bgt(cpu : CPU, operands : list[str]) -> bool:
    pass

def bge(cpu : CPU, operands : list[str]) -> bool:
    pass

def ble(cpu : CPU, operands : list[str]) -> bool:
    pass

# Other
def nop(cpu : CPU, operands : list[str]) -> bool:
    pass

def halt(cpu : CPU, operands : list[str]) -> bool:
    cpu.should_halt = True
    return False

if __name__ == "__main__":
    main()
