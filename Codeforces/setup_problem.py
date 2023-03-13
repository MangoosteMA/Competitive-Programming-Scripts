import argparse
import subprocess
from os import system

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Codeforces.get_problem import get_problem
from Library.helpers import colored


def create_file(file, data):
    with open(file, 'w') as f:
        print(data, file=f)


def setup_problem(problem, directory='.', extra_files=None):
    assert problem.index is not None
    subprocess.run(['rm', '-r', f'{directory}/{problem.index}'], capture_output=True)
    subprocess.run(['mkdir', f'{directory}/{problem.index}'])
    if problem.inputs is not None:
        for test in range(len(problem.inputs)):
            create_file(f'{directory}/{problem.index}/in{test + 1}', problem.inputs[test])
            create_file(f'{directory}/{problem.index}/out{test + 1}', problem.outputs[test])

    if extra_files is not None:
        for file_name, template in extra_files:
            subprocess.run(['cp', '-r', template, f'{directory}/{problem.index}/{file_name}'])


def setup_problem_from_args(args):
    problem = get_problem(args.url, use_selenium=args.selenium)
    if problem is None:
        print(colored('Failed', 255, 0, 0), 'to load the problem.')
        sys.exit(0)
    if problem.index is None:
        print(colored('Failed', 255, 0, 0), 'to load the problem index.')
        sys.exit(0)

    setup_problem(problem, extra_files=args.problem_files)
    n_tests =  0 if problem.inputs is None else len(problem.inputs)
    print(f'Tests created: {n_tests}')
