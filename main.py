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

def main() -> None:
    args = sys.argv[1:]
    program_file = "test.txt"
    memory_file = "test.mem"

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


def execute_program(program : list[Instruction]) -> None:
    cpu = CPU()
    while not cpu.should_halt:
        tick(program, cpu)
    print(cpu)


def tick(program : list[Instruction], cpu : CPU):
    instr = program[cpu.program_counter]
    execute_instr(cpu, instr)

def execute_instr(cpu : CPU, instr: Instruction):
    lookup = {
        "LDR" : ldr,
        "HALT" : halt
    }
    lookup[instr.opcode](cpu, instr.operands)

def ldr(cpu : CPU, operands : list[str]):
    cpu.write_register(operands[1], int(operands[0], 16))
    cpu.program_counter += 1

def halt(cpu : CPU, operands : list[str]):
    cpu.should_halt = True

if __name__ == "__main__":
    main()

