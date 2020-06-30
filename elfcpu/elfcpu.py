######
#
# ElfCpu from Advent of Code 2018 day 16
#

from .opcodes import opcodes

class ElfCpu():
    def __init__(self, code, ip_register, max_registers=6, debug=False):
        self.max_registers = max_registers
        self.code = code
        self.ip_r = ip_register
        self.debug = debug
        self.reset()
    
    def reset(self):
        self.r = [0 for _ in range(self.max_registers)]
        self.ip = -1

    @classmethod
    def from_file(cls, filename, max_registers=6, debug=False):
        opcode_names = {o.__name__: i for i, o in enumerate(opcodes)}
        code = list()
        with open(filename) as f:
            for line in f:
                if line.startswith('#ip'):
                    ip_register = int(line[4:])
                else:
                    o, a, b, c = line.split()
                    o_id = opcode_names[o]
                    code.append((o_id, int(a), int(b), int(c)))
        return cls(code, ip_register, max_registers, debug)

    def step(self):
        self.ip += 1
        if self.ip >= len(self.code):
            return True
        i, a, b, c = self.code[self.ip]
        self.r[self.ip_r] = self.ip
        if self.debug:
            print(f'{self.ip:2} {opcodes[i].__name__} ({a}, {b}, {c}) {self.r}') 
        opcodes[i](a, b, c, self.r)
        self.ip = self.r[self.ip_r]
        if self.debug:
            print(f'Result: {self.r}')
        return False

    def run(self):
        terminated = False
        while not terminated:
            terminated = self.step()