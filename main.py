import os
import sys

class Instruction:

    def __init__(self) -> None:
        pass

class CPU:

    def __init__(self) -> None:
        self.should_halt = False
        pass

def main() -> None:
    args = sys.argv[1:]
    target_file = "test.txt"

    
    pass

def parse_program(program : str) -> list[Instruction]:
    pass

def execute_program(program : list[Instruction]) -> None:
    cpu = CPU()
    while not cpu.should_halt:
        tick(program, cpu)


def tick(program : list[Instruction], cpu : CPU):
    pass

