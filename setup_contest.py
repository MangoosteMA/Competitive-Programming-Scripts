import argparse
import os
import subprocess
import sys

from typing                 import Optional
from library.contest        import Contest
from library.utils          import colored, getHtml, JudgeSystem, dumpError
from codeforces.get_contest import parseContestFromHtml as cfParseContestFromHtml
from atcoder.get_contest    import parseContestFromHtml as atcoderParseContestFromHtml
from setup_problem          import File, createProblemFiles

# from setup_problem          import setup_problem

# def setup_contest(contest, contest_title, extra_files=None, extra_problem_files=None):
#     subprocess.run(['rm', '-r', f'{contest_title}'], capture_output=True)
#     subprocess.run(['mkdir', contest_title])
#     if extra_files is not None:
#         for file_name, template in extra_files:
#             subprocess.run(['cp', '-r', template, f'{contest_title}/{file_name}'])

#     if contest.problems is not None:
#         for problem in contest.problems:
#             setup_problem(problem, directory=contest_title, extra_files=extra_problem_files)
#             print(f'Problem {problem.index} is created!')
#             n_tests = 0 if problem.inputs is None else len(problem.inputs)
#             print(f'Tests created: {n_tests}\n')

# def setup_contest_from_args(args):
#     if args.html_code is not None:
#         f = open(args.html_code, 'r')
#         if not args.keep_html:
#             subprocess.run(['rm', f'{args.html_code}'], capture_output=True)
#         args.html_code = f.read()
#         f.close()

#     contest = Contest()
#     if args.url is not None or args.html_code is not None:
#         if args.url is not None:
#             system = determineJudgeSystemFromUrl(args.url)
#         else:
#             system = determineJudgeSystemFromHtml(args.html_code)

#         print(f'Judge system: {system}')
#         if system == 'codeforces':
#             contest = cf_get_contest_from_args(args)
#         elif system == 'atcoder':
#             contest = atcoder_get_contest_from_args(args)
#         else:
#             print(f'System \'{system}\' is not avaliable yet.')
#             sys.exit(0)

#         if contest is None:
#             print(colored('Failed', 255, 0, 0), 'to load the contest.')
#             sys.exit(0)
#     else:
#         print('No url was given.')

#     contest_title = contest.title if args.title is None else ''.join(x for x in args.title)
#     setup_contest(contest, contest_title, extra_files=args.contest_files, extra_problem_files=args.problem_files)
#     n_problems = 0 if contest.problems is None else len(contest.problems)
#     print(f'Problems created: {n_problems}')

class ContestSetter:
    '''
    Variables:
    contestUrl:   str or None
    contestName:  str or None
    htmlPath:     str or None
    saveHtml:     bool
    conststFiles: list[File]
    problemFiles: list[File]
    const:        Contest or None
    '''

    def __init__(self, args):
        self.contestUrl = args.url
        self.contestName = args.title
        self.htmlPath = args.html
        self.saveHtml = args.saveHtml
        self.contestFiles = self.__parseFiles(args.contestFiles)
        self.problemFiles = self.__parseFiles(args.problemFiles)

    def run(self) -> None:
        self.contest = Contest()
        self.__handleHtml()

        if self.contestName is None:
            dumpError('Failed to parse contest name.')
            return

        self.__createContestFiles()

# Private:

    def __parseFiles(self, argFiles) -> None:
        if argFiles is None:
            return []

        parsedFiles = []
        for fileName, templatePath in argFiles:
            if not os.path.isfile(templatePath):
                dumpError(f'No such file: {templatePath}')
            else:
                parsedFiles.append(File(fileName=fileName, templatePath=templatePath))

        return parsedFiles

    def __loadHtml(self) -> Optional[None]:
        if not os.path.isfile(self.htmlPath):
            dumpError(f'No such file: {self.htmlPath}')
            return None

        with open(self.htmlPath, 'r') as htmlFile:
            htmlData = htmlFile.read()

        if not self.saveHtml:
            os.remove(self.htmlPath)

        return htmlData

    def __parseHtml(self, html: str) -> None:
        judgeSystem = JudgeSystem.determineFromHtml(html)
        if judgeSystem is None:
            dumpError('Failed to determine judge system.')
            return

        print('Judge system: ', end='')
        if judgeSystem == JudgeSystem.CODEFORCES:
            print('codeforces')
            self.contest = cfParseContestFromHtml(html, link=self.contestUrl)
        elif judgeSystem == JudgeSystem.ATCODER:
            print('atcoder')
            self.contest = atcoderParseContestFromHtml(html, link=self.contestUrl)

        if self.contest is not None and self.contest is not None and self.contestName is None:
            self.contestName = self.contest.title

    def __handleHtml(self) -> None:
        html = None
        if self.htmlPath is not None:
            html = self.__loadHtml()

        if html is None and self.contestUrl is not None:
            html = getHtml(self.contestUrl)

        if html is not None:
            self.__parseHtml(html)

    def __createProblems(self, directory: str) -> None:
        if self.contest.problems is None:
            return

        for problem in self.contest.problems:
            if problem.index is None:
                dumpError('Failed to load index of one of the problems.')
                continue

            createProblemFiles(problem, self.problemFiles, f'{directory}/{problem.index}')
            print(f'Problem {problem.index} is created.\n')

    def __createContestFiles(self) -> None:
        directory = f'./{self.contestName}'
        subprocess.run(['rm', '-r', directory], capture_output=True)
        os.mkdir(directory)

        for contestFile in self.contestFiles:
            subprocess.run(['cp', '-r', contestFile.templatePath, f'{directory}/{contestFile.fileName}'])

        self.__createProblems(directory)

def main():
    parser = argparse.ArgumentParser(description='Contest arguments parser.')
    parser.add_argument('-url',
                        dest='url',
                        metavar='url',
                        default=None,
                        help='Link to all problems of the contest.')

    parser.add_argument('-problem-file',
                        dest='problemFiles',
                        nargs=2,
                        action='append',
                        metavar=('file-name', 'file-template'),
                        help='File to be created for each problem (copy of file-template).')

    parser.add_argument('-contest-file',
                        dest='contestFiles',
                        nargs=2,
                        action='append',
                        metavar=('file-name', 'file-template'),
                        help='File to be created (copy of file-template).')

    parser.add_argument('-title',
                        dest='title',
                        metavar='contest-name',
                        default=None,
                        help='Name of the contest.')

    parser.add_argument('-html',
                        action='store',
                        default=None,
                        help='Path to the files that contains problem html.')

    parser.add_argument('-save-html',
                        action='store_true',
                        dest='saveHtml',
                        default=False,
                        help='Don\'t delete html file.')

    args = parser.parse_args()
    contestSetter = ContestSetter(args)
    contestSetter.run()

if __name__ == '__main__':
    main()
