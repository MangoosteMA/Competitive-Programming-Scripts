import argparse
from Library.helpers import determine_system
from Codeforces.setup_contest import setup_contest_from_args as cf_setup_contest_from_args


def main():
    parser = argparse.ArgumentParser(description='Contest arguments parser.')
    parser.add_argument('-url',
                        dest='url',
                        required=True,
                        metavar='url',
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

    args = parser.parse_args()
    system = determine_system(args.url)
    print(f'Judge system: {system}')
    if system == 'codeforces':
        cf_setup_contest_from_args(args)
    else:
        print(f'System \'{system}\' is not avaliable yet.')


if __name__ == '__main__':
    main()