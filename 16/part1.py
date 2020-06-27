from elfcpu.opcodes import opcodes
from collections import defaultdict
from pprint import pprint

if __name__ == "__main__":
    test_cases = list()
    with open('16/input_a') as f:
        for line in f:
            if line.startswith('Before:'):
                #Before: line
                start = line.index('[')
                before_registers = [int(i) for i in line.strip()[start+1:-1].split(',')]
                instruction = [int(i) for i in f.readline().split()]
                start = line.index('[')
                end_registers = [int(i) for i in f.readline().strip()[start+1:-1].split(',')]
                test_cases.append((instruction, before_registers, end_registers))

    solution = 0    # number of test cases that are compatible with 3 or more opcodes
    for instruction, before_registers, expected_registers in test_cases:
        success = 0
        for operation in opcodes:
            registers = before_registers[:]
            operation(*instruction[1:], registers)
            if registers == expected_registers:
                success += 1
                if success >=3:
                    solution += 1
                    break
    print(f'First part solution: {solution}')

    opcode_frequency = defaultdict(set)
    for instruction, before_registers, expected_registers in test_cases:
        opcode = instruction[0]
        for op_id, operation in enumerate(opcodes):
            registers = before_registers[:]
            operation(*instruction[1:], registers)
            if registers == expected_registers:
                opcode_frequency[opcode].add(op_id)
            else:
                opcode_frequency[opcode].discard(op_id)
    opcode_mappings = [False for _ in range(len(opcodes))]
    while not all(opcode_mappings):
        for opcode in opcode_frequency:
            if len(opcode_frequency[opcode]) == 1:
                op_id = opcode_frequency[opcode].pop()
                opcode_mappings[opcode] = opcodes[op_id]
                break
        del opcode_frequency[opcode]
        for frequencies in opcode_frequency.values():
            frequencies.discard(op_id)
    opcodes.clear()
    opcodes.extend(opcode_mappings)

    registers = [0, 0, 0 ,0]
    with open('16/input_b') as f:
        for line in f:
            instruction = [int(c) for c in line.split()]
            opcode = instruction[0]
            opcodes[opcode](*instruction[1:], registers)
    print(f'Ordered opcodes: {[op.__name__ for op in opcodes]}')
    print(f'Solution Part2: {registers[0]}')
    




