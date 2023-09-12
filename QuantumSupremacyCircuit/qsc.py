import argparse
import math
import random

from enum import Enum

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--row", default=6, type=int, 
                        help="number of rows of the lattice pattern.")
    parser.add_argument("--col", default=6, type=int, 
                        help="number of columns of the lattice pattern.")
    parser.add_argument( "--depth", default=10, type=int,
                        help="depth to generate. depth+1 circuit will be generated for initial hardamard.")
    return parser.parse_args()


class InstructionType(Enum):
    CZ = 1
    SX = 2
    SY = 3
    T = 4


def get_random_gate(idx, board, first):
    choices = [ "SX", "SY", "T" ]
    if first[idx]:
        first[idx] = False
        return "T";
    else:
        cur = board[idx]
        while board[idx] == cur:
            cur = choices[random.randint(0, len(choices)-1)]
        return cur

def generate(row, col, depth):
    patterns = []
    patterns.append([
            (r, c) for r in range(0, row, 1) for c in range(2 if (r % 2) == 0 else 0, col-1, 4)
            ])
    patterns.append([
            (r, c) for r in range(0, row, 1) for c in range(0 if (r % 2) == 0 else 2, col-1, 4)
            ])
    patterns.append([
            (r, c) for r in range(1, row-1, 2) for c in range(1 if (r - 1) % 4 == 0 else 0, col, 2)
            ])
    patterns.append([
            (r, c) for r in range(1, row-1, 2) for c in range(0 if (r - 1) % 4 == 1 else 0, col, 2)
            ])
    patterns.append([
            (r, c) for r in range(0, row, 1) for c in range(3 if (r % 2) == 0 else 1, col-1, 4)
            ])
    patterns.append([
            (r, c) for r in range(0, row, 1) for c in range(1 if (r % 2) == 0 else 3, col-1, 4)
            ])
    patterns.append([
            (r, c) for r in range(0, row-1, 2) for c in range(0 if r % 4 == 0 else 1, col, 2)
            ])
    patterns.append([
            (r, c) for r in range(0, row-1, 2) for c in range(1 if r % 4 == 0 else 0, col, 2)
            ])

    def tup_to_idx(tup):
        return tup[0] * col + tup[1]

    qasm_str = "OPENQASM 2.0;\n"
    qasm_str += f"qreg q[{row*col}];\n"

    qasm_str += f'# Cycle 0\n'
    for idx in range(row*col):
        qasm_str += f'H q[{idx}];\n'

    board = ["H" for _ in range(row) for _ in range(col)]
    first = [True for _ in range(row) for _ in range(col)]

    for i in range(depth):
        pat = patterns[i % len(patterns)]
        qasm_str += f'# Cycle {i+1}\n'

        for idx in range(row*col):
            if board[idx] == "CZ":
                gate = get_random_gate(idx, board, first)
                qasm_str += f'{gate} q[{idx}];\n'
                board[idx] = gate

        for tup in pat:
            idx1 = tup_to_idx(tup)
            idx2 = (idx1+1) if (i // 2) % 2 == 0 else (idx1 + col)
            qasm_str +=  f'CZ q[{idx1}], q[{idx2}];\n';
            board[idx1] = "CZ"
            board[idx2] = "CZ"


    return qasm_str

def main():
    args = parse_args()

    row, col, depth = args.row, args.col, args.depth

    qasm = generate(row, col, depth)
    print(qasm)

if __name__ == '__main__':
    main()
