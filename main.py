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

    def __init__(self, memory) -> None:
        self.should_halt = False
        self.program_counter = 0
        self.registers : dict[str, int] = {f"R{i}" : 0 for i in range(16)}
        self.registers["PC"] = 0
        self.flags = {
            "negative" : False, 
            "zero" : False,
            "carry" : False,
            "overflow" : False,
            "saturation" : False
        }
        self.memory = memory[2]

    def __str__(self) -> str:
        output = [
            "===== CPU STATE =====",
            f"Program Counter: {self.program_counter}",
            f"Halted: {self.should_halt}",
            "",
            "----- REGISTERS -----"
        ]

        for register, value in self.registers.items():
            output.append(f"{register:>3}: 0x{value:06X} ({value}) ({to_signed_int(value)})")

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
    memory_file = args[2]

    program_as_str = None
    with open(program_file) as file:
        program_as_str = file.read()

    mem_as_str = None
    with open(memory_file) as file:
        mem_as_str = file.read()

    program = parse_program(program_as_str)
    memory = init_memory(mem_as_str)
    for i in program:
        print(i)
    execute_program(program, memory)

def parse_program(program : str) -> list[Instruction]:
    program_instrs = []
    for line in program.splitlines():
        line = line.split("//", 1)[0].split() # strip out comments and then split on whitespace
        if not line :
            continue
        instr = Instruction(line[0].upper(), line[1:])
        program_instrs.append(instr)
    
    return program_instrs

# returns a tuple of (name, specs, mem_contens)
def init_memory(mem_file : str) -> tuple[str, list[str], list[int]]:
    split_file = mem_file.splitlines()
    name = split_file[0].strip("//")
    specs = split_file[1].split(",")
    max_address = (1 << int(specs[0]))
    mem_contents = [0 for i in range(max_address)]
    for line in split_file[2:]:
        line = line.split("//", 1)[0].strip()
        if not line:
            continue
        address, value = line.split(",")
        mem_contents[parse_int(address)] = parse_int(value)

    return (name, specs, mem_contents)


def execute_program(program : list[Instruction], memory) -> CPU:
    cpu = CPU(memory)
    # All instructions MUST return a bool that indicates whether or not
    # the program counter is incremented. Branch instrs will opt out if condition is met
    opcode_lookup = {
        "LDR" : ldr,
        "LDI" : ldi,
        "STR" : str_,
        "STI" : sti,
        "HALT" : halt,
        "ADD" : add,
        "SUB" : sub,
        "MUL" : mul,
        "UDIV" : udiv,
        "SDIV" : sdiv,
        "TEQ" : teq,
        "MOV" : mov,
        "AND" : and_,
        "OR" : or_,
        "XOR" : xor,
        "BIC" : bic,
        "NOT" : not_,
        "LSL" : lsl,
        "LSR" : lsr,
        "B" : b,
        "BEQ" : beq,
        "BNE" : bne,
        "BGT" : bgt,
        "BLT" : blt,
        "BGE" : bge,
        "BLE" : ble,
        "NOP" : nop
    }
    while not cpu.should_halt:
        instr = program[cpu.program_counter]
        if opcode_lookup[instr.opcode](cpu, instr.operands):
            cpu.set_program_counter(cpu.program_counter + 1)

    print(cpu)
    return cpu

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

# Same as udiv
# def div(cpu : CPU, operands : list[str]) -> bool:
#     result = cpu.registers[operands[1]] // cpu.registers[operands[2]]
#     cpu.write_register(operands[0], result)
#     return True

def mov(cpu : CPU, operands : list[str]) -> bool:
    cpu.write_register(operands[0], cpu.registers[operands[1]])
    return True

def sdiv(cpu : CPU, operands : list[str]) -> bool:
    result = to_signed_int(cpu.registers[operands[1]]) // to_signed_int(cpu.registers[operands[2]])
    cpu.write_register(operands[0], result)
    return True

def udiv(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] // cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def and_(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] & cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def or_(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] | cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def xor(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] ^ cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def bic(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] & ~cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def not_(cpu : CPU, operands : list[str]) -> bool:
    result = ~ cpu.registers[operands[1]] 
    cpu.write_register(operands[0], result)
    return True

def lsl(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] << cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def lsr(cpu : CPU, operands : list[str]) -> bool:
    result = cpu.registers[operands[1]] >> cpu.registers[operands[2]]
    cpu.write_register(operands[0], result)
    return True

def teq(cpu : CPU, operands : list[str]) -> bool:
    cmp = cpu.registers[operands[0]] ^ cpu.registers[operands[1]]
    cpu.flags["zero"] = cmp == 0
    return True

# Memory
def ldr(cpu : CPU, operands : list[str]) -> bool:
    value_from_mem = cpu.memory[parse_int(operands[0])]
    cpu.write_register(operands[1], value_from_mem)
    return True

def ldi(cpu : CPU, operands : list[str]) -> bool:
    value_from_mem = cpu.memory[cpu.memory[parse_int(operands[0])]]
    cpu.write_register(operands[1], value_from_mem)
    return True

def str_(cpu : CPU, operands : list[str]) -> bool:
    cpu.memory[parse_int(operands[0])] = cpu.registers[operands[1]]
    return True

def sti(cpu : CPU, operands : list[str]) -> bool:
    cpu.memory[cpu.memory[parse_int(operands[0])]] = cpu.registers[operands[1]]
    return True

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
    # TODO: Currently doesnt work with address like 
    # we specified in our document.
    cpu.set_program_counter(cpu.registers[operands[0]])
    return False

def beq(cpu: CPU, operands : list[str]) -> bool:
    if cpu.registers[operands[1]] == cpu.registers[operands[2]]: 
        cpu.set_program_counter(cpu.registers[operands[0]])
        return False
    return True


def blt(cpu: CPU, operands : list[str]) -> bool:
    if cpu.registers[operands[1]] < cpu.registers[operands[2]]: 
        cpu.set_program_counter(cpu.registers[operands[0]])
        return False
    return True

def bne(cpu : CPU, operands : list[str]) -> bool:
    if cpu.registers[operands[1]] != cpu.registers[operands[2]]: 
        cpu.set_program_counter(cpu.registers[operands[0]])
        return False
    return True

def bgt(cpu : CPU, operands : list[str]) -> bool:
    if cpu.registers[operands[1]] > cpu.registers[operands[2]]: 
        cpu.set_program_counter(cpu.registers[operands[0]])
        return False
    return True

def bge(cpu : CPU, operands : list[str]) -> bool:
    if cpu.registers[operands[1]] >= cpu.registers[operands[2]]: 
        cpu.set_program_counter(cpu.registers[operands[0]])
        return False
    return True

def ble(cpu : CPU, operands : list[str]) -> bool:
    if cpu.registers[operands[1]] <= cpu.registers[operands[2]]: 
        cpu.set_program_counter(cpu.registers[operands[0]])
        return False
    return True

# Other
def nop(cpu : CPU, operands : list[str]) -> bool:
    return True

def halt(cpu : CPU, operands : list[str]) -> bool:
    cpu.should_halt = True
    return False

# Helpers
def parse_int(num : str) -> int:
    return int(num.strip(), 0)

def to_signed_int(num : int) -> int:
    if num & 0x800000:
        return num - 0x1000000
    return num

if __name__ == "__main__":
    main()
