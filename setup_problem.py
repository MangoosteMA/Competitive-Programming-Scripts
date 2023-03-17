import argparse
import subprocess
from Library.helpers import determine_system
from Codeforces.get_problem import get_problem_from_args as cf_get_problem_from_args


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
    system = determine_system(args.url)
    print(f'Judge system: {system}')
    problem = None
    if system == 'codeforces':
        problem = cf_get_problem_from_args(args)
    else:
        print(f'System \'{system}\' is not avaliable yet.')
        sys.exit(0)

    if problem is None:
        print(colored('Failed', 255, 0, 0), 'to load the problem.')
        sys.exit(0)
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
                        required=True,
                        metavar='url',
                        help='Link to the problem.')

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

    setup_problem_from_args(parser.parse_args())


if __name__ == '__main__':
    main()
