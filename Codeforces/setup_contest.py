import argparse
import subprocess
from os import system

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Codeforces.get_contest import get_contest
from Codeforces.setup_problem import setup_problem


def setup_contest(contest, contest_title, extra_files=None, extra_problem_files=None):
    subprocess.run(['rm', '-r', f'{contest_title}'], capture_output=True)
    subprocess.run(['mkdir', contest_title])
    if extra_files is not None:
        for file, template in extra_files:
            subprocess.run(['cp', '-r', template, f'{contest_title}/{file_name}'])

    if contest.problems is not None:
        for problem in contest.problems:
            setup_problem(problem, directory=contest_title, extra_files=extra_problem_files)
            print(f'Problem {problem.index} is created!')
            n_tests = 0 if problem.inputs is None else len(problem.inputs)
            print(f'Tests created: {n_tests}\n')


def setup_contest_from_args(args):
    contest = get_contest(args.url)
    if contest is None:
        print('Failed to load the contest.')
        sys.exit(0)

    contest_title = contest.title if args.title is None else ''.join(x for x in args.title)
    setup_contest(contest, contest_title, extra_files=args.contest_files, extra_problem_files=args.problem_files)
    print('Done!')
    n_problems = 0 if contest.problems is None else len(contest.problems)
    print(f'Problems created: {n_problems}')
