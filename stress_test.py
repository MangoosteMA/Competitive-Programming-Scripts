from argparse import ArgumentParser
import re
import subprocess
import sys
from library.utils import colored

parser = ArgumentParser()
parser.add_argument('-solve',
                    action='store',
                    required=True,
                    help='Path to the file to stress test.')

parser.add_argument('-gen',
                    action='store',
                    required=True,
                    help='Path to the generator (must be executable).')

parser.add_argument('-brute',
                    action='store',
                    help='Path to the correct solution (if not given, then it would RE stress test).')

parser.add_argument('-tests',
                    action='store',
                    type=int,
                    default=500,
                    help='Number of tests (500 by default).')

parser.add_argument('-no_output',
                    default=False,
                    action='store_true',
                    help='Add if you want not to show test and another data at the end.')

args = parser.parse_args()

print("\033[?25l", end='')

TEST_NAME = 'in_stress'
for test_num in range(1, args.tests + 1):
    print(colored('\rTesting on test #', 255, 255, 50), colored(str(test_num), 0, 200, 200), sep='', end='')
    with open(TEST_NAME, 'w') as test:
        generator_returncode = subprocess.run([f'./{args.gen}'], stdout=test, stderr=subprocess.PIPE).returncode

    if generator_returncode != 0:
        print(colored('\nGenerator got RE.', 255, 70, 0))
        sys.exit(0)

    with open(TEST_NAME, 'r') as test:
        solve_result = subprocess.run([f'./{args.solve}'], stdin=test, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if solve_result.returncode != 0:
        print(colored('\nSolution got RE.', 255, 70, 0))
        if not args.no_output:
            print(colored('Test:', 255, 255, 50))
            subprocess.run(['cat', TEST_NAME])
        sys.exit(0)

    if args.brute is None:
        continue

    with open(TEST_NAME, 'r') as test:
        brute_result = subprocess.run([f'./{args.brute}'], stdin=test, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if brute_result.returncode != 0:
        print(colored('\nCorrect solution got RE.', 255, 70, 0))
        sys.exit(0)

    if solve_result.stdout.decode().strip() != brute_result.stdout.decode().strip():
        print(colored('\nWrong answer', 255, 70, 0))
        if not args.no_output:
            print(colored('Test:', 255, 255, 50))
            subprocess.run(['cat', TEST_NAME])
            print(colored('\nSolve output:', 255, 165, 0))
            print(solve_result.stdout.decode().strip('\n'))
            print(colored('\nCorrect output:', 255, 165, 0))
            print(brute_result.stdout.decode().strip('\n'))
        sys.exit(0)

print(colored('\nLooks like everything is working fine!', 0, 255, 0))
