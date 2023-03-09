import subprocess
import re
import time
import sys
from os import listdir
from argparse import ArgumentParser
from Library.helpers import colored

parser = ArgumentParser()
parser.add_argument('-exec',
                    dest='solve',
                    nargs=1,
                    required=True,
                    metavar='exec',
                    help='Path to the executable file.')

parser.add_argument('-test',
                    dest='tests',
                    nargs='*',
                    metavar='test',
                    help='Add test.')

parser.add_argument('-compiler',
                    metavar='compiler',
                    help='Set the compiler in case you want to compile the code.')

parser.add_argument('-compile_flags',
                    dest='compile_flags',
                    nargs='*',
                    metavar='compile_flags',
                    default=[],
                    help='Add compiler flags.')

parser.add_argument('-cmpl',
                    action='store_true',
                    default=False,
                    help='Add if you want only to compile.')

args = parser.parse_args()

main = args.solve[0]
tests = args.tests
if tests is None:
    tests = []
    r = re.compile('in[0-9]+')
    for test in listdir():
        if r.match(test):
            tests.append(test)
    tests.sort(key=lambda test: 0 if len(test) == 2 else int(test[2:]))
else:
    tests.sort()


if args.compiler is not None:
    compilation = [args.compiler, f'{main}.cpp', '-o', main]
    for x in args.compile_flags:
        compilation.append(f'-{x}')
    result = subprocess.run(compilation)
    if result.returncode != 0:
        sys.exit(0)

if args.cmpl:
    sys.exit(0)


def get_ans(test):
    pos = test.find('in')
    if pos == -1:
        return None
    return test[:pos] + 'out' + test[pos + 2:]


def get_colored_result(first, second, must_be_equal):
    text = ''
    for i in range(len(first)):
        cur = []
        for j in range(len(first[i])):
            if i >= len(second) or j >= len(second[i]) or first[i][j] != second[i][j]:
                cur.append(colored(first[i][j], 255, 120, 120) if must_be_equal else colored(first[i][j], 120, 255, 120))
            else:
                cur.append(first[i][j])
        text += ' '.join(cur) + '\n'
    return text


SEPARATOR = '==================================================='
OK = colored('OK', 0, 255, 0)
WA = colored('WA', 255, 70, 0)
RE = colored('RE', 255, 70, 0)
UNKNOWN = colored('Unknown', 120, 200, 235)

ok = 0; wa = 0; re = 0; unknown = 0
for test in tests:
    if ok + wa + re + unknown != 0:
        print(SEPARATOR)

    expected_ans = get_ans(test)
    if not expected_ans in listdir():
        expected_ans = None

    start_time = time.time()
    result = subprocess.run([f'./{main}'], stdin=open(test, 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    total_time = time.time() - start_time

    colored_output = None
    colored_expected_output = None
    print_data = False

    if result.returncode != 0:
        re += 1
        verdict = RE
        print_data = True
    elif expected_ans is None:
        unknown += 1
        verdict = UNKNOWN
        print_data = True
    else:
        lines = [x.strip().split() for x in result.stdout.decode().split('\n') if len(x.strip()) > 0]
        correct_lines = [x.strip().split() for x in open(expected_ans, 'r').read().split('\n') if len(x.strip()) > 0]
        if lines == correct_lines:
            ok += 1
            verdict = OK
        else:
            wa += 1
            print_data = True
            verdict = WA
            colored_output = get_colored_result(lines, correct_lines, True)
            colored_expected_output = get_colored_result(correct_lines, lines, False)


    print(f'Test ', colored(test, 255, 255, 50), ': ', verdict, f' ({int(total_time * 1000)} ms)', sep='')
    if print_data:
        print(open(test, 'r').read().strip('\n'))

        if expected_ans is not None:
            print('\nExpected output (', colored(expected_ans, 255, 255, 50), '):', sep='')
            if colored_expected_output is not None:
                print(colored_expected_output.strip('\n'))
            else:
                for line in correct_lines:
                    print(' '.join(line))

        print('\nOutput:')
        if colored_output is None:
            print(result.stdout.decode().strip('\n'))
        else:
            print(colored_output)

        if len(result.stderr.decode().strip('\n')) > 0:
            print('\nErr:')
            print(result.stderr.decode().strip('\n'))

print(SEPARATOR)
if ok == len(tests):
    print(colored('All tests passed!', 0, 255, 0))
else:
    print(f'{ok} {OK}, {wa} {WA}, {re} {RE}, {unknown} {UNKNOWN}.')
