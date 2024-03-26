import argparse
import os
import subprocess
import sys

from dataclasses                 import dataclass
from typing                      import Optional
from .lib.problem                import Problem
from .utils                      import colored, JudgeSystem, dumpError, getHtml, loadSettings
from .codeforces.get_problem     import parseProblemFromHtml as cfParseProblemFromHtml
from .atcoder.get_problem        import parseProblemFromHtml as atcoderParseProblemFromHtml
from .yandex_contest.get_problem import parseProblemFromHtml as yandexParseProblemFromHtml

@dataclass
class File:
    fileName:     str
    templatePath: str

def createSingleFile(filePath: str, fileData: str) -> None:
    with open(filePath, 'w') as file:
        print(fileData, file=file)

def createProblemFiles(problem: Problem, problemFiles: list[File], directory: str) -> None:
    subprocess.run(['rm', '-r', directory], capture_output=True)
    os.mkdir(directory)

    if problem.inputs is not None:
        for testIndex in range(0, len(problem.inputs)):
            createSingleFile(f'{directory}/in{testIndex + 1}', problem.inputs[testIndex])
            createSingleFile(f'{directory}/out{testIndex + 1}', problem.outputs[testIndex])

    for problemFile in problemFiles:
        subprocess.run(['cp', '-r', problemFile.templatePath, f'{directory}/{problemFile.fileName}'])

    testsCreated = 0 if problem.inputs is None else len(problem.inputs)
    print(f'Tests created: {testsCreated}')

class ProblemSetter:
    '''
    Variables:
    problemUrl:   str or None
    shortName:    str or None
    htmlPath:     str or None
    saveHtml:     bool
    problemFiles: list[File]
    problem:      Problem or None
    '''

    def __init__(self, args: argparse.Namespace):
        self.problemUrl = args.url
        self.shortName = args.index
        self.htmlPath = args.html
        self.saveHtml = args.saveHtml
        self.__parseProblemFiles(args)

    def run(self) -> None:
        self.problem = Problem()
        self.__handleHtml()

        if self.shortName is None:
            dumpError('Failed to parse problem short name.')
            return

        self.__createProblemFiles()

# Private:

    def __parseProblemFiles(self, args) -> None:
        self.problemFiles = []
        if args.problemFiles is None:
            return

        for fileName, templatePath in args.problemFiles:
            if not os.path.isfile(templatePath):
                dumpError(f'No such file: {templatePath}')
            else:
                self.problemFiles.append(File(fileName=fileName, templatePath=templatePath))
    
    def __loadHtml(self) -> Optional[str]:
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
            self.problem = cfParseProblemFromHtml(html, link=self.problemUrl)
        elif judgeSystem == JudgeSystem.ATCODER:
            print('atcoder')
            self.problem = atcoderParseProblemFromHtml(html, link=self.problemUrl)
        elif judgeSystem == JudgeSystem.YANDEX_CONTEST:
            print('yandex contest')
            self.problem = yandexParseProblemFromHtml(html, link=self.problemUrl)

        if self.problem is not None and self.problem.index is not None and self.shortName is None:
            self.shortName = self.problem.index

    def __handleHtml(self) -> None:
        html = None
        if self.htmlPath is not None:
            html = self.__loadHtml()

        if html is None and self.problemUrl is not None:
            html = getHtml(self.problemUrl)

        if html is not None:
            self.__parseHtml(html)

    def __createProblemFiles(self) -> None:
        print(f'Index: {self.shortName}')
        directory = f'./{self.shortName}'
        createProblemFiles(self.problem, self.problemFiles, directory)

def main():
    problemFiles = list(loadSettings().get('problem_files', {}).items())

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
                        help='Problem short name.')

    parser.add_argument('-problem-file',
                        dest='problemFiles',
                        nargs=2,
                        action='append',
                        metavar=('file-name', 'file-template'),
                        default=problemFiles,
                        help='File to be created (copy of file-template).')

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
    problemSetter = ProblemSetter(args)
    problemSetter.run()
