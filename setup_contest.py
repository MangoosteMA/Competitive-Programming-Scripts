import sys
import argparse
import subprocess

from Library.default_classes import Contest
from Library.helpers import determine_system
from Codeforces.get_contest import get_contest_from_args as cf_get_contest_from_args
from Atcoder.get_contest import get_contest_from_args as atcoder_get_contest_from_args
from setup_problem import setup_problem


def setup_contest(contest, contest_title, extra_files=None, extra_problem_files=None):
    subprocess.run(['rm', '-r', f'{contest_title}'], capture_output=True)
    subprocess.run(['mkdir', contest_title])
    if extra_files is not None:
        for file_name, template in extra_files:
            subprocess.run(['cp', '-r', template, f'{contest_title}/{file_name}'])

    if contest.problems is not None:
        for problem in contest.problems:
            setup_problem(problem, directory=contest_title, extra_files=extra_problem_files)
            print(f'Problem {problem.index} is created!')
            n_tests = 0 if problem.inputs is None else len(problem.inputs)
            print(f'Tests created: {n_tests}\n')


def setup_contest_from_args(args):
    contest = Contest()
    if args.url is not None:
        system = determine_system(args.url)
        print(f'Judge system: {system}')
        if system == 'codeforces':
            contest = cf_get_contest_from_args(args)
        elif system == 'atcoder':
            contest = atcoder_get_contest_from_args(args)
        else:
            print(f'System \'{system}\' is not avaliable yet.')
            sys.exit(0)

        if contest is None:
            print(colored('Failed', 255, 0, 0), 'to load the contest.')
            sys.exit(0)
    else:
        print('No url was given.')

    contest_title = contest.title if args.title is None else ''.join(x for x in args.title)
    setup_contest(contest, contest_title, extra_files=args.contest_files, extra_problem_files=args.problem_files)
    n_problems = 0 if contest.problems is None else len(contest.problems)
    print(f'Problems created: {n_problems}')


def main():
    parser = argparse.ArgumentParser(description='Contest arguments parser.')
    parser.add_argument('-url',
                        dest='url',
                        metavar='url',
                        default=None,
                        help='Link to the problems of the contest.')

    parser.add_argument('-problem_file',
                        dest='problem_files',
                        nargs=2,
                        action='append',
                        metavar=('file_name', 'file_template'),
                        help='Add file inside each problem (copies from file_template).')

    parser.add_argument('-contest_file',
                        dest='contest_files',
                        nargs=2,
                        action='append',
                        metavar=('file_name', 'file_template'),
                        help='Add file inside the contest.')

    parser.add_argument('-name',
                        dest='title',
                        nargs='+',
                        metavar='contest_name',
                        help='Set the name of the contest (contest title from url is set by default).')

    parser.add_argument('-selenium',
                        action='store_true',
                        default=False,
                        help='Add if you want only to use selenium (useful only during the contest).')

    setup_contest_from_args(parser.parse_args())


if __name__ == '__main__':
    main()
