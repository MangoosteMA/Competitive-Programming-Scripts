import argparse
import os
import subprocess
import sys

from typing                  import Optional
from .lib.contest            import Contest
from .utils                  import colored, getHtml, JudgeSystem, dumpError, loadSettings, runProcess
from .codeforces.get_contest import parseContestFromHtml as cfParseContestFromHtml
from .atcoder.get_contest    import parseContestFromHtml as atcoderParseContestFromHtml
from .setup_problem          import File, createProblemFiles

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

    def __init__(self, args: argparse.Namespace):
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
        elif judgeSystem == JudgeSystem.ATCODER:
            dumpError('Importing yandex contest is not supported (only single problem so far).')

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
    problemFiles = list(loadSettings().get('problem_files', {}).items())
    contestFiles = list(loadSettings().get('contest_files', {}).items())

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
                        default=problemFiles,
                        help='File to be created for each problem (copy of file-template).')

    parser.add_argument('-contest-file',
                        dest='contestFiles',
                        nargs=2,
                        action='append',
                        metavar=('file-name', 'file-template'),
                        default=contestFiles,
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
    runProcess(contestSetter.run)
