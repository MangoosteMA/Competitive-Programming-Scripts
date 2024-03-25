import os
import argparse
import subprocess
import sys

from dataclasses            import dataclass
from typing                 import Optional
from library.problem        import Problem
from library.utils          import colored, JudgeSystem, dumpError, getHtml
from codeforces.get_problem import parseProblemFromHtml as cfParseProblemFromHtml
from atcoder.get_problem    import parseProblemFromHtml as atcoderParseProblemFromHtml

@dataclass
class ProblemFile:
    fileName:     str
    templatePath: str

class ProblemSetter:
    '''
    Variables:
    problemUrl:   str or None
    shortName:    str or None
    htmlPath:     str or None
    saveHtml:     bool
    problemFiles: list[ProblemFile]
    problem:      Problem or None
    '''

    def __init__(self, args):
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
        for fileName, templatePath in args.problemFiles:
            if not os.path.isfile(templatePath):
                dumpError(f'No such file: {templatePath}')
            else:
                self.problemFiles.append(ProblemFile(fileName=fileName, templatePath=templatePath))
    
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

    def __handleHtml(self) -> None:
        html = None
        if self.htmlPath is not None:
            html = self.__loadHtml()

        if html is None and self.problemUrl is not None:
            html = getHtml(self.problemUrl)

        if html is not None:
            self.__parseHtml(html)

    def __createSingleFile(self, filePath: str, fileData: str) -> None:
        with open(filePath, 'w') as file:
            print(fileData, file=file)

    def __createTests(self, directory: str) -> None:
        if self.problem.inputs is None:
            return
        
        for testIndex in range(0, len(self.problem.inputs)):
            self.__createSingleFile(f'{directory}/in{testIndex + 1}', self.problem.inputs[testIndex])
            self.__createSingleFile(f'{directory}/out{testIndex + 1}', self.problem.outputs[testIndex])
        
    def __createProblemFiles(self) -> None:
        directory = f'./{self.shortName}'
        subprocess.run(['rm', '-r', directory])
        os.mkdir(directory)

        self.__createTests(directory)
        for problemFile in self.problemFiles:
            subprocess.run(['cp', '-r', problemFile.templatePath, f'{directory}/{problemFile.fileName}'])

        testsCreated = 0 if self.problem.inputs is None else len(self.problem.inputs)
        print(f'Tests created: {testsCreated}')

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
                        help='Problem short name.')

    parser.add_argument('-problem-file',
                        dest='problemFiles',
                        nargs=2,
                        action='append',
                        metavar=('file-name', 'file-template'),
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

if __name__ == '__main__':
    main()
