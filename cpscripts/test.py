import os
import re
import subprocess
import sys
import time
import argparse

from dataclasses import dataclass
from enum        import Enum
from typing      import Any
from .utils      import colored, dumpError, compareOutput, addEmptyLine, coloredLinesPrint, loadSettings, runProcess

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

class Tester:
    '''
    Variables:
    mainExecutable:   str
    extention:        str
    tests:            list[Test]
    compileOnly:      bool
    compilerPath:     str or None
    compilationFlags: list[str] or NOne
    noErr:            bool
    '''

    TEST_NAME_REGEX = re.compile('in[0-9]+')
    SEPARATOR = '==========================================='

    OK = colored('OK', 20, 255, 20)
    WA = colored('WA', 255, 70, 0)
    RE = colored('RE', 255, 70, 0)
    UNKNOWN = colored('Unknown', 120, 200, 235)

    OUTPUT = colored('Output', 255, 165, 0)
    EXPECTED_OUTPUT = colored('Expected output', 255, 165, 0)
    ERR = colored('Err', 255, 165, 0)

    def __init__(self, args: argparse.Namespace):
        self.mainExecutable = args.exec
        self.extention = args.ext

        if self.mainExecutable.endswith('.cpp'):
            self.mainExecutable = self.mainExecutable[:-4]
            self.extention = 'cpp'

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

        if not self.compileOnly:
            self.__runTests()

# Private:

    def __parseCompiler(self, args: argparse.Namespace) -> None:
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

        self.tests.append(Test(testPath=testPath, testAnswer=testAnswer))

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

    def __dumpSingleTestOutput(self, test: Test, outputLines: list[str], errOutput: str, correctOutputLines: list[str]) -> None:
        with open(test.testPath, 'r') as testFile:
            print(testFile.read())

        outputLines = addEmptyLine(outputLines)
        print(f'{Tester.OUTPUT}:')
        coloredLinesPrint(outputLines, correctOutputLines, 255, 120, 120)

        if not self.noErr and len(errOutput.strip()) > 0:
            print(f'{Tester.ERR}:')
            print(errOutput)
            if len(errOutput) == 0 or errOutput[-1] != '\n':
                print()

        if correctOutputLines is not None:
            print(f'{Tester.EXPECTED_OUTPUT}:')
            correctOutputLines = addEmptyLine(correctOutputLines)
            coloredLinesPrint(correctOutputLines, outputLines, 120, 255, 120)

    @staticmethod
    def __dumpSingleTestVerdict(verdict: TestResult, executionTime: int) -> None:
        if verdict == TestResult.OK:
            print(Tester.OK, end='')
        elif verdict == TestResult.WA:
            print(Tester.WA, end='')
        elif verdict == TestResult.RE:
            print(Tester.RE, end='')
        else:
            print(Tester.UNKNOWN, end='')

        print(f' ({executionTime}ms)')

    def __runSingleTest(self, test: Test) -> TestResult:
        print('Test ', colored(test.testPath, 255, 255, 50), ': ', sep='', end='', flush=True)

        with open(test.testPath, 'r') as testFile:
            processStartTime = time.time()
            processData = subprocess.run([f'./{self.mainExecutable}'],
                                         stdin=testFile,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
            executionTime = int((time.time() - processStartTime) * 1000)

        outputLines = processData.stdout.decode().rstrip('\n').split('\n')
        errOutput = processData.stderr.decode().rstrip('\n')

        correctOutputLines = None
        if test.testAnswer is not None:
            with open(test.testAnswer, 'r') as testAnswer:
                correctOutputLines = testAnswer.read().rstrip('\n').split('\n')

        if processData.returncode != 0:
            verdict = TestResult.RE
        elif test.testAnswer is None:
            verdict = TestResult.UNKNOWN
        elif compareOutput(outputLines, correctOutputLines):
            verdict = TestResult.OK
        else:
            verdict = TestResult.WA

        self.__dumpSingleTestVerdict(verdict, executionTime)
        if verdict != TestResult.OK:
            self.__dumpSingleTestOutput(test, outputLines, errOutput, correctOutputLines)

        return verdict

    def __dumpTestsVerdicts(self, verdictsCounter: dict[int: int]) -> None:
        oks      = verdictsCounter[TestResult.OK]
        was      = verdictsCounter[TestResult.WA]
        res      = verdictsCounter[TestResult.RE]
        unknowns = verdictsCounter[TestResult.UNKNOWN]

        print(Tester.SEPARATOR)
        if verdictsCounter[TestResult.OK] == len(self.tests):
            print(colored('All tests passed!', 20, 255, 20))
        else:
            print(f'{Tester.OK}: {oks}  ',
                  f'{Tester.WA}: {was}  ',
                  f'{Tester.RE}: {res}  ',
                  f'{Tester.UNKNOWN}: {unknowns}')

    def __runTests(self) -> None:
        verdictsCounter = {TestResult.OK:      0,
                           TestResult.WA:      0,
                           TestResult.RE:      0,
                           TestResult.UNKNOWN: 0}

        for i, test in enumerate(self.tests):
            if i != 0:
                print(Tester.SEPARATOR)
            status = self.__runSingleTest(test)
            verdictsCounter[status] += 1

        self.__dumpTestsVerdicts(verdictsCounter)

def main(defaultArgs: dict[str: Any]={}) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('exec',
                        action='store',
                        metavar='exec',
                        help='Path to the executable file.')

    parser.add_argument('-ext',
                        action='store',
                        metavar='ext',
                        default=defaultArgs.get('ext', 'cpp'),
                        help='Extention of the solution file (required for compilation).')

    parser.add_argument('-test',
                        dest='tests',
                        nargs='*',
                        metavar='test',
                        help='List of tests to run on. ' +
                             'By default it runs on tests which matches \"in[0-9]+\".')

    parser.add_argument('-compiler',
                        metavar='compiler',
                        default=defaultArgs.get('compiler', None),
                        help='Path to the compiler. ' +
                             'If not specified, then program will not be compiled.')

    parser.add_argument('-flags',
                        dest='flags',
                        nargs='*',
                        metavar='flags',
                        default=defaultArgs.get('flags', []),
                        help='Compilation flags.')

    parser.add_argument('-cmplonly',
                        action='store_true',
                        default=defaultArgs.get('cmplonly', False),
                        help='Add if you want only to compile.')

    parser.add_argument('-noerr',
                        action='store_true',
                        default=defaultArgs.get('noerr', False),
                        help='Hide err output.')

    args = parser.parse_args()
    tester = Tester(args)
    runProcess(tester.run)

def bld(command: str='debug') -> None:
    settings = loadSettings().get(command, {})
    main({'compiler': settings.get('compiler', None),
          'flags':    settings.get('flags', [])     })

def fbld() -> None:
    bld('release')

def cmpl(command: str='debug') -> None:
    settings = loadSettings().get(command, {})
    main({'compiler': settings.get('compiler', None),
          'flags':    settings.get('flags', [])     ,
          'cmplonly': True                          })

def fcmpl() -> None:
    cmpl('release')
