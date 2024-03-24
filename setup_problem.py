import sys
import argparse
import subprocess

from library.problem        import Problem
from library.utils          import determine_system, colored, determine_system_from_html
from codeforces.get_problem import get_problem_from_args as cf_get_problem_from_args
from atcoder.get_problem    import get_problem_from_args as atcoder_get_problem_from_args

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
    if args.html_code is not None:
        f = open(args.html_code, 'r')
        if not args.keep_html:
            subprocess.run(['rm', f'{args.html_code}'], capture_output=True)
        args.html_code = f.read()
        f.close()

    problem = Problem()
    if args.url is not None or args.html_code is not None:
        if args.url is not None:
            system = determine_system(args.url)
        else:
            system = determine_system_from_html(args.html_code)

        print(f'Judge system: {system}')
        if system == 'codeforces':
            problem = cf_get_problem_from_args(args)
        elif system == 'atcoder':
            problem = atcoder_get_problem_from_args(args)
        else:
            print(f'System \'{system}\' is not avaliable yet.')
            sys.exit(0)

        if problem is None:
            print(colored('Failed', 255, 0, 0), 'to load the problem.')
            sys.exit(0)
    else:
        print('No url was given.')

    if args.index is not None:
        problem.index = args.index

    if problem.index is None:
        print(colored('Failed', 255, 0, 0), 'to load the problem index.')
        sys.exit(0)

    setup_problem(problem, extra_files=args.problem_files)
    n_tests =  0 if problem.inputs is None else len(problem.inputs)
    print(f'Tests created: {n_tests}')

def main():
    parser = argparse.ArgumentParser(description='Problem arguments parser.')
    parser.add_argument('-url',
                        dest='url',
                        metavar='url',
                        default=None,
                        help='Link to the problem.')

    parser.add_argument('-index',
                        dest='index',
                        metavar='index',
                        default=None,
                        help='Index of the problem.')

    parser.add_argument('-problem_file',
                        dest='problem_files',
                        nargs=2,
                        action='append',
                        metavar=('file_name', 'file_template'),
                        help='Add file inside the problem (copies from file_template).')

    parser.add_argument('-selenium',
                        action='store_true',
                        default=False,
                        help='Add if you want only to use selenium (useful only during the contest).')

    parser.add_argument('-html_code',
                        action='store',
                        default=None,
                        help='Path to the files that contains problem html.')

    parser.add_argument('-keep_html',
                        action='store_true',
                        default=False,
                        help='Set in case you want to keep html file.')

    setup_problem_from_args(parser.parse_args())


if __name__ == '__main__':
    main()
