import argparse
import math
import random

from enum import Enum

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--version", default=2, type=int, 
                        help="OpenQASM version. For now, only version 2 is supported.")
    parser.add_argument("--num_qubits", default=5, type=int, 
                        help="number of qubits.")
    parser.add_argument( "--num_gates", default=10, type=int,
                        help="number of gates.")
    parser.add_argument( "--use_if", default=False, type=bool,
                        action=argparse.BooleanOptionalAction,
                        help="whether or not to use 'if' statement.")
    parser.add_argument( "--use_measure", default=False, type=bool,
                        action=argparse.BooleanOptionalAction,
                        help="whether or not to use measurement.")
    parser.add_argument( "--use_reset", default=False, type=bool,
                        action=argparse.BooleanOptionalAction,
                        help="whether or not to use reset.")
    parser.add_argument( "--use_barrier", default=False, type=bool,
                        action=argparse.BooleanOptionalAction,
                        help="whether or not to use barrier.")
    return parser.parse_args()


class RandomQASMInstruction:
    @staticmethod
    def U(num_qubits):
        qubit = random.randint(0, num_qubits-1)
        theta = random.random() * 4 * math.pi
        phi = random.random() * 4 * math.pi
        lbmda = random.random() * 4 * math.pi
        return f"U({theta},{phi},{lbmda}) q[{qubit}];";

    @staticmethod
    def CX(num_qubits):
        qubit1 = random.randint(0, num_qubits-1)
        qubit2 = qubit1
        while qubit2 == qubit1:
            qubit2 = random.randint(0, num_qubits-1)
        return f"CX q[{qubit1}] q[{qubit2}];";

    @staticmethod
    def IF(num_qubits):
        val = random.randint(0, (2**num_qubits)-1)
        if random.randint(0, 1) == 0:
            instr = RandomQASMInstruction.U(num_qubits)
            return f"if (c == {val}) {instr}"
        else:
            instr = RandomQASMInstruction.CX(num_qubits)
            return f"if (c == {val}) {instr}"

    @staticmethod
    def MEASURE(num_qubits):
        qubit = random.randint(0, num_qubits-1)
        clbit = random.randint(0, num_qubits-1)
        return f"measure q[{qubit}] -> c[{clbit}];";

    @staticmethod
    def RESET(num_qubits):
        qubit = random.randint(0, num_qubits-1)
        return f"reset q[{qubit}];";

    @staticmethod
    def BARRIER(num_qubits):
        qubit = random.randint(0, num_qubits-1)
        return f"barrier q[{qubit}];";


class InstructionType(Enum):
    U = 1
    CX = 2
    IF = 3
    MEASURE = 4
    RESET = 5
    BARRIER = 6


def generate(num_qubits,
             num_gates,
             use_if=False,
             use_measure=False,
             use_reset=False,
             use_barrier=False):
    operators = [ InstructionType.U, InstructionType.CX ]
    if use_if:
        operators = operators + [ InstructionType.IF ]
    if use_measure:
        operators = operators + [ InstructionType.MEASURE ]
    if use_reset:
        operators = operators + [ InstructionType.RESET ]
    if use_barrier:
        operators = operators + [ InstructionType.BARRIER ]


    qasm_str = "OPENQASM 2.0;\n"
    qasm_str += f"qreg q[{num_qubits}];\n"
    qasm_str += f"creg c[{num_qubits}];\n"

    for _ in range(num_gates):
        idx = random.randint(0, len(operators)-1)
        op = operators[idx]
        if op == InstructionType.U: instr = RandomQASMInstruction.U(num_qubits)
        elif op == InstructionType.CX: instr = RandomQASMInstruction.CX(num_qubits)
        elif op == InstructionType.IF: instr = RandomQASMInstruction.IF(num_qubits)
        elif op == InstructionType.MEASURE: instr = RandomQASMInstruction.MEASURE(num_qubits)
        elif op == InstructionType.RESET: instr = RandomQASMInstruction.RESET(num_qubits)
        elif op == InstructionType.BARRIER: instr = RandomQASMInstruction.BARRIER(num_qubits)
        qasm_str += f"{instr}\n";

    return qasm_str

def main():
    args = parse_args()

    num_qubits, num_gates = args.num_qubits, args.num_gates
    use_if, use_measure = args.use_if, args.use_measure
    use_reset, use_barrier = args.use_reset, args.use_barrier

    qasm = generate(num_qubits, num_gates, use_if, use_measure, use_reset, use_barrier)
    print(qasm)

if __name__ == '__main__':
    main()
