import sys

class Instruction:

    def __init__(self, opcode : str, operands : list) -> None:
        self.name = opcode
        self.args = []
        pass

class CPU:

    def __init__(self) -> None:
        self.should_halt = False
        pass

def main() -> None:
    args = sys.argv[1:]
    target_file = "test.txt"

    file_as_str = None
    with open(target_file) as file:
        file_as_str = file.read()

    program = parse_program(file_as_str)
    execute_program(program)

def parse_program(program : str) -> list[Instruction]:
    # TODO 
    return []


def execute_program(program : list[Instruction]) -> None:
    cpu = CPU()
    while not cpu.should_halt:
        tick(program, cpu)


def tick(program : list[Instruction], cpu : CPU):
    pass

if __name__ == "__main__":
    main()

