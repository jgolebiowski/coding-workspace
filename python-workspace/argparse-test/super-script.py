"""Super test script"""

import argparse
import numpy as np


def str2bool(v):
    """Convert a string to a boolean value"""
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Test matmul times on random arrays")
    parser.add_argument("-d",
                        dest="dimensions",
                        action="store",
                        type=int,
                        nargs="?",
                        default="3",
                        help="Dimensionality of the Matrixes [D x D], default=3")
    parser.add_argument("--random",
                        dest="rand_flag",
                        action="store",
                        type=str2bool,
                        nargs="?",
                        default=True,
                        help="Set to 0 to use arange() arrays, leave at 1 for random")
    parser.add_argument("--print",
                        dest="print_flag",
                        action="store",
                        type=str2bool,
                        nargs="?",
                        default=True,
                        help="Set 0 to not print the arrays out, leave 1 to print")
    args = parser.parse_args()

    if args.rand_flag:
        A = np.random.rand(args.dimensions, args.dimensions)
        B = np.random.rand(args.dimensions, args.dimensions)
    else:
        A = np.arange(args.dimensions * args.dimensions).reshape(args.dimensions, args.dimensions)
        B = np.arange(args.dimensions * args.dimensions).reshape(args.dimensions, args.dimensions)

    C = np.matmul(A, B)
    if args.print_flag:
        print("A\n", A)
        print("B\n", B)
        print("C = A @ B\n", C)
