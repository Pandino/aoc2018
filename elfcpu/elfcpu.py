######
#
# ElfCpu from Advent of Code 2018 day 16
#
#
# API:
# - cpu = ElfCpu()
# - cpu.evaluate(instruction) Evaluate instruction, return nothing
# - cpu.reset() Clear all registers
# - cpu.r return register array
# - 



class ElfCpu():
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.r = [0, 0, 0]

    def evaluate(self, instruction):
        opcode, a, b, c = instruction
        ...

