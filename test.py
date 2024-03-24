import os
import re
import subprocess
import sys
import time

from enum          import Enum
from dataclasses   import dataclass
from argparse      import ArgumentParser
from library.utils import colored, dumpError

class Tester:
    '''
    Variables:
    mainExecutable:   str
    extention:        str
    tests:            list[Tester.Test]
    compileOnly:      bool
    compilerPath:     str or None
    compilationFlags: list[str] or NOne
    noErr:            bool
    '''

    TEST_NAME_REGEX = re.compile('in[0-9]+')
    SEPARATOR = '=============================================='

    OK = colored('OK', 20, 255, 20)
    WA = colored('WA', 255, 70, 0)
    RE = colored('RE', 255, 70, 0)
    UNKNOWN = colored('Unknown', 120, 200, 235)

    OUTPUT = colored('Output', 255, 165, 0)
    EXPECTED_OUTPUT = colored('Expected output', 255, 165, 0)
    ERR = colored('Err', 255, 165, 0)

    @dataclass
    class Test:
        testPath:   str
        testAnswer: str

        def getTestIndex(self) -> int:
            indexStart = self.testPath.find('in')
            if indexStart == -1:
                return -1
            return int(self.testPath[indexStart + 2:])

    class TestResult(Enum):
        OK      = 0
        WA      = 1
        RE      = 2
        UNKNOWN = 3

    def __init__(self, args):
        self.mainExecutable = args.exec
        self.extention = args.ext

        self.__parseCompiler(args)
        self.compileOnly = args.cmplonly
        if not self.compileOnly:
            self.__registerTests(args.tests)

        self.noErr = args.noerr

    def run(self) -> None:
        if self.compilerPath is not None:
            self.__compile()

        if not self.compileOnly:
            print()
            self.__runTests()

# Private:

    def __parseCompiler(self, args) -> None:
        self.compilerPath = args.compiler
        self.compilationFlags = ['-' + flag for flag in args.flags]

    def __registerSingleTest(self, testPath: str) -> None:
        if not os.path.isfile(testPath):
            dumpError(f'No such file: {testPath}')
            return

        answerFileName = os.path.basename(testPath).replace('in', 'out')
        directory = os.path.dirname(testPath)
        testAnswer = None
        if answerFileName in os.listdir('./' if len(directory) == 0 else directory):
            testAnswer = os.path.join(directory, answerFileName)

        self.tests.append(Tester.Test(testPath=testPath, testAnswer=testAnswer))

    def __registerTests(self, testsNames: list[str] or None) -> None:
        self.tests = []
        if testsNames is not None:
            for test in testsNames:
                self.__registerSingleTest(test)
            return

        for testCandidate in os.listdir():
            if Tester.TEST_NAME_REGEX.match(testCandidate) and os.path.isfile(testCandidate):
                self.__registerSingleTest(testCandidate)
        self.tests.sort(key=lambda test: test.getTestIndex())

    def __compile(self) -> None:
        solutionPath = f'{self.mainExecutable}.{self.extention}'
        if not os.path.isfile(solutionPath):
            dumpError(f'No solution file: {solutionPath}')
            sys.exit(0)

        command = [self.compilerPath, solutionPath, '-o', self.mainExecutable] + self.compilationFlags
        compilationStartTime = time.time()
        status = subprocess.run(command)
        compilationTime = int((time.time() - compilationStartTime) * 1000)

        if status.returncode != 0:
            dumpError(f'\nDid not compile. ({compilationTime}ms)')
            sys.exit(0)

        print(colored('Compiled successfully.', 20, 255, 20), f'({compilationTime}ms)')

    @staticmethod
    def __compareOutput(outputLines, correctOutputLines) -> list[int]:
        if correctOutputLines is None:
            return []

        differentLines = []
        for i in range(0, max(len(outputLines), len(correctOutputLines))):
            outputLine = outputLines[i] if i < len(outputLines) else ''
            correctLine = correctOutputLines[i] if i < len(correctOutputLines) else ''
            if outputLine.strip() != correctLine.strip():
                differentLines.append(i)
        
        return differentLines

    @staticmethod
    def __addEmptyLine(lines: list[str]) -> list[str]:
        if len(lines) == 0 or len(lines[-1]) != 0:
            lines.append('')
        return lines

    def __dumpSingleTestOutput(self, test, outputLines, errOutput, correctOutputLines) -> None:
        with open(test.testPath, 'r') as testFile:
            print(testFile.read())

        differentLines = self.__compareOutput(outputLines, correctOutputLines)

        outputLines = Tester.__addEmptyLine(outputLines)
        print(f'{Tester.OUTPUT}:')
        for i, line in enumerate(outputLines):
            if i in differentLines:
                line = colored(line, 255, 120, 120)
            print(line)

        if not self.noErr and len(errOutput.strip()) > 0:
            print(f'{Tester.ERR}:')
            print(errOutput)
            if len(errOutput) == 0 or errOutput[-1] != '\n':
                print()

        if correctOutputLines is not None:
            print(f'{Tester.EXPECTED_OUTPUT}:')
            correctOutputLines = Tester.__addEmptyLine(correctOutputLines)
            for i, line in enumerate(correctOutputLines):
                if i in differentLines:
                    line = colored(line, 120, 255, 120)
                print(line)

    @staticmethod
    def __dumpSingleTestVerdict(verdict, executionTime) -> None:
        if verdict == Tester.TestResult.OK:
            print(Tester.OK, end='')
        elif verdict == Tester.TestResult.WA:
            print(Tester.WA, end='')
        elif verdict == Tester.TestResult.RE:
            print(Tester.RE, end='')
        else:
            print(Tester.UNKNOWN, end='')

        print(f' ({executionTime}ms)')

    def __runSingleTest(self, test) -> TestResult:
        print('Test ', colored(test.testPath, 255, 255, 50), ': ', sep='', end='', flush=True)

        with open(test.testPath, 'r') as testFile:
            processStartTime = time.time()
            processData = subprocess.run([f'./{self.mainExecutable}'],
                                         stdin=testFile,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
            executionTime = int((time.time() - processStartTime) * 1000)

        outputLines = processData.stdout.decode().split('\n')
        errOutput = processData.stderr.decode()

        correctOutputLines = None
        if test.testAnswer is not None:
            with open(test.testAnswer, 'r') as testAnswer:
                correctOutputLines = testAnswer.read().split('\n')

        if processData.returncode != 0:
            verdict = Tester.TestResult.RE
        elif test.testAnswer is None:
            verdict = Tester.TestResult.UNKNOWN
        elif len(Tester.__compareOutput(outputLines, correctOutputLines)) == 0:
            verdict = Tester.TestResult.OK
        else:
            verdict = Tester.TestResult.WA

        self.__dumpSingleTestVerdict(verdict, executionTime)
        if verdict != Tester.TestResult.OK:
            self.__dumpSingleTestOutput(test, outputLines, errOutput, correctOutputLines)

        return verdict

    def __dumpTestsVerdicts(self, verdictsCounter: dict[int: int]) -> None:
        oks      = verdictsCounter[Tester.TestResult.OK]
        was      = verdictsCounter[Tester.TestResult.WA]
        res      = verdictsCounter[Tester.TestResult.RE]
        unknowns = verdictsCounter[Tester.TestResult.UNKNOWN]

        print(Tester.SEPARATOR)
        if verdictsCounter[Tester.TestResult.OK] == len(self.tests):
            print(colored('All tests passed!', 20, 255, 20))
        else:
            print(f'{Tester.OK}: {oks}  ',
                  f'{Tester.WA}: {was}  ',
                  f'{Tester.RE}: {res}  ',
                  f'{Tester.UNKNOWN}: {unknowns}')

    def __runTests(self) -> None:
        verdictsCounter = {Tester.TestResult.OK:      0,
                           Tester.TestResult.WA:      0,
                           Tester.TestResult.RE:      0,
                           Tester.TestResult.UNKNOWN: 0}

        for i, test in enumerate(self.tests):
            if i != 0:
                print(Tester.SEPARATOR)
            status = self.__runSingleTest(test)
            verdictsCounter[status] += 1

        self.__dumpTestsVerdicts(verdictsCounter)

def main():
    parser = ArgumentParser()
    parser.add_argument('exec',
                        action='store',
                        metavar='exec',
                        help='Path to the executable file.')

    parser.add_argument('-ext',
                        action='store',
                        metavar='ext',
                        default='cpp',
                        help='Extention of the solution file (required for compilation).')

    parser.add_argument('-test',
                        dest='tests',
                        nargs='*',
                        metavar='test',
                        help='List of tests to run on. ' +
                             'By default it runs on tests which matches \"in[0-9]+\".')

    parser.add_argument('-compiler',
                        metavar='compiler',
                        help='Path to the compiler. ' +
                             'If not specified, then program will not be compiled.')

    parser.add_argument('-flags',
                        dest='flags',
                        nargs='*',
                        metavar='flags',
                        default=[],
                        help='Compilation flags.')

    parser.add_argument('-cmplonly',
                        action='store_true',
                        default=False,
                        help='Add if you want only to compile.')

    parser.add_argument('-noerr',
                        action='store_true',
                        default=False,
                        help='Hide err output.')

    args = parser.parse_args()
    tester = Tester(args)
    tester.run()

if __name__ == '__main__':
    main()
