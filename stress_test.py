from argparse import ArgumentParser
import os
import re
import subprocess
import sys

from library.utils import colored, dumpError, compareOutput, addEmptyLine, colorfulLinesPrint

class StressTester:
    '''
    Variables:
    testsNumber:     int
    solveExecutable: str
    genExecutable:   str
    bruteExecutable: str
    '''

    TEST_NAME = 'in_stress'
    TEST = colored('Test:', 255, 255, 50)
    SOLVE_OUTPUT = colored('Solve output:', 255, 165, 0)
    CORRECT_OUTPUT = colored('Correct output:', 255, 165, 0)
    ERR = colored('Err', 255, 165, 0)

    def __init__(self, args):
        self.testsNumber = args.tests
        self.solveExecutable = args.solve
        self.genExecutable = args.gen
        self.bruteExecutable = args.brute
        self.__checkExecutableFiles()

    def run(self) -> None:
        print("\033[?25l", end='') # hide the cursor
        for testIndex in range(1, self.testsNumber + 1):
            print(colored('\rTesting on test #', 255, 255, 50), colored(str(testIndex), 0, 200, 200), sep='', end='')
            self.__runOneTest(testIndex)

        print(colored('\nLooks like everything is working fine!', 20, 255, 20))

# Private:

    def __checkExecutableFiles(self) -> None:
        for executableFile in [self.solveExecutable, self.genExecutable, self.bruteExecutable]:
            if executableFile is not None and not os.path.isfile(executableFile):
                dumpError(f'No such file: {executableFile}')
                sys.exit(0)

    def __generateTest(self, testIndex: int) -> None:
        with open(StressTester.TEST_NAME, 'w') as testFile:
            runResult = subprocess.run([f'./{self.genExecutable}', str(testIndex)], stdout=testFile)

        if runResult.returncode != 0:
            dumpError('\nGenerator got RE.')
            sys.exit(0)

    @staticmethod
    def __dumpTest() -> None:
        with open(StressTester.TEST_NAME, 'r') as testFile:
            lines = testFile.read().split('\n')

        print(StressTester.TEST)
        print('\n'.join(addEmptyLine(lines)))

    @staticmethod
    def __dumpErr(solutionRunResult: subprocess.CompletedProcess) -> None:
        errOutput = solutionRunResult.stderr.decode()
        print(StressTester.ERR)
        print(errOutput)
        if len(errOutput) == 0 or errOutput[-1] != '\n':
            print()

    @staticmethod
    def __dumpSolutionsOutput(solutionOutputLines: list[str], bruteOutputLines: list[str]) -> None:
        differentLines = compareOutput(solutionOutputLines, bruteOutputLines)
        print(StressTester.SOLVE_OUTPUT)
        colorfulLinesPrint(addEmptyLine(solutionOutputLines), differentLines, 255, 120, 120)

        print(StressTester.CORRECT_OUTPUT)
        colorfulLinesPrint(addEmptyLine(bruteOutputLines), differentLines, 120, 255, 120)

    def __validateOutput(self, solutionRunResult: subprocess.CompletedProcess) -> None:
        with open(StressTester.TEST_NAME, 'r') as testFile:
            bruteRunResult = subprocess.run([f'./{self.bruteExecutable}'],
                                             stdin=testFile,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

        if bruteRunResult.returncode != 0:
            dumpError('\nBrute force solution got RE.')
            self.__dumpTest()
            sys.exit(0)

        solutionOutputLines = solutionRunResult.stdout.decode().split('\n')
        bruteOutputLines = bruteRunResult.stdout.decode().split('\n')
        if len(compareOutput(solutionOutputLines, bruteOutputLines)) != 0:
            dumpError('\nWrong answer')
            self.__dumpTest()
            self.__dumpSolutionsOutput(solutionOutputLines, bruteOutputLines)
            sys.exit(0)

    def __runOneTest(self, testIndex: int) -> tuple[str, str]:
        self.__generateTest(testIndex)

        with open(StressTester.TEST_NAME, 'r') as testFile:
            solutionRunResult = subprocess.run([f'./{self.solveExecutable}'],
                                               stdin=testFile,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)

        if solutionRunResult.returncode != 0:
            dumpError('\nSolution got RE.')
            self.__dumpTest()
            self.__dumpErr(solutionRunResult)
            sys.exit(0)

        if self.bruteExecutable is not None:
            self.__validateOutput(solutionRunResult)

def main():
    parser = ArgumentParser()
    parser.add_argument('-solve',
                        action='store',
                        required=True,
                        help='Path to the maby incorrect executable solution.')

    parser.add_argument('-gen',
                        action='store',
                        required=True,
                        help='Path to the executable generator.')

    parser.add_argument('-brute',
                        action='store',
                        default=None,
                        help='Path to the executable correct solution. ' +
                             'If not given, then stress test will look for RE.')

    parser.add_argument('-tests',
                        action='store',
                        type=int,
                        default=1000,
                        help='Number of tests (1000 by default).')

    args = parser.parse_args()
    stressTester = StressTester(args)
    stressTester.run()

if __name__ == '__main__':
    main()
