import os
import sys
import subprocess
import time

from argparse  import ArgumentParser
from queue     import Queue
from threading import Thread
from typing    import Optional
from .utils    import colored, dumpError, runProcess

class ExecutingPopen:
    '''
    Variables:
    runningPopen:   subprocess.Popen
    poll:           int or None
    readingThreads: dict[str, Thread]
    readingQueues:  dict[str, Queue]
    '''

    def __init__(self, executableFile: str):
        self.runningPopen = subprocess.Popen([f'./{executableFile}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.poll = None
        self.readingThreads = dict()
        self.readingQueues = dict()

        for streamType, stream in zip(['stdout', 'stderr'], [self.runningPopen.stdout, self.runningPopen.stderr]):
            self.readingQueues[streamType] = Queue()
            self.readingThreads[streamType] = Thread(target=ExecutingPopen.__readLoop, args=(stream, self.readingQueues[streamType]))
            self.readingThreads[streamType].start()

    def isRunning(self) -> bool:
        self.poll = self.runningPopen.poll()
        return self.poll is None

    def getLine(self, stream: str) -> Optional[str]:
        if self.readingQueues[stream].empty():
            return None

        return self.readingQueues[stream].get()

    def communicate(self, newLine: str) -> None:
        if self.isRunning():
            self.runningPopen.stdin.write(newLine.encode())
            self.runningPopen.stdin.flush()

    def anyThreadAlive(self) -> bool:
        for streamType, thread in self.readingThreads.items():
            if thread.is_alive():
                return True

        return False

    def terminate(self) -> None:
        self.runningPopen.terminate()

# Private:

    @staticmethod
    def __readLoop(stream, queue: Queue) -> None:
        for line in iter(stream.readline, b''):
            queue.put(line.decode())

        stream.close()

class Interactor:
    '''
    Variables:
    solutionExecutable:   str
    interactorExecutable: str
    timeout:              float
    inputFile:            str or None
    '''

    INTERACTION_HEADER = '+-------------------------------------------+\n' +\
                         '|      Solution        |     Interactor     |\n' +\
                         '+-------------------------------------------+'
    PADDING        = len('........................')

    def __init__(self, args):
        self.solutionExecutable = args.sol
        self.interactorExecutable = args.int
        self.timeout = args.timeout

        if self.__checkFile(args.input):
            self.inputFile = args.input

        if not self.__checkFile(self.solutionExecutable) or\
           not self.__checkFile(self.interactorExecutable):
            sys.exit(0)

    def run(self) -> None:
        print(Interactor.INTERACTION_HEADER.replace('Interactor', colored('Interactor', 255, 255, 0)))
        self.__communicatingLoop()

# Private:

    @staticmethod
    def __checkFile(fileName: str) -> bool:
        if fileName is None or os.path.isfile(fileName):
            return True

        dumpError(f'No such file: {fileName}')
        return False

    @staticmethod
    def __printWithSeparator(line: str, padding: int, r: Optional[int], g: Optional[int], b: Optional[int]) -> None:
        if r is None or g is None or b is None:
            print(' ' * padding, line, sep='', end='', flush=True)
        else:
            print(' ' * padding, colored(line, r, g, b), sep='', end='', flush=True)

    def __openInputFile(self, interactorPopen: ExecutingPopen) -> None:
        if self.inputFile is None:
            return
        
        with open(self.inputFile, 'r') as inputFile:
            for line in inputFile:
                interactorPopen.communicate(line)

    def __processSingleStderr(self, popen: ExecutingPopen, padding, r: Optional[int], g: Optional[int], b: Optional[int]) -> None:
        while True:
            newLine = popen.getLine('stderr')
            if newLine is None:
                break

            self.__printWithSeparator(newLine, padding, r, g, b)

    def __processStderr(self, solutionPopen: ExecutingPopen, interactorPopen: ExecutingPopen) -> None:
        self.__processSingleStderr(solutionPopen, 0, None, None, None)
        self.__processSingleStderr(interactorPopen, Interactor.PADDING, 255, 255, 0)

    def __finish(self, solutionPopen: ExecutingPopen, interactorPopen: ExecutingPopen, exitError: Optional[str]) -> None:
        solutionPopen.terminate()
        interactorPopen.terminate()
        while solutionPopen.anyThreadAlive() or interactorPopen.anyThreadAlive():
            self.__processStderr(solutionPopen, interactorPopen)

        if exitError is not None:
            dumpError(exitError)

    def __communicatingLoop(self) -> None:
        solutionPopen = ExecutingPopen(self.solutionExecutable)
        interactorPopen = ExecutingPopen(self.interactorExecutable)
        self.__openInputFile(interactorPopen)

        exitError = None
        startTime = time.time()

        while solutionPopen.isRunning() or interactorPopen.isRunning():
            self.__processStderr(solutionPopen, interactorPopen)

            if time.time() - startTime > self.timeout:
                exitError = f'Termiating interaction due to the timeout ({self.timeout} seconds).'
                break

            if not solutionPopen.isRunning() and solutionPopen.poll != 0:
                exitError = 'Solution got RE.'
                break

            if not interactorPopen.isRunning() and interactorPopen.poll != 0:
                exitError = 'Interactor got RE.'
                break

            solutionUnprocessedOutput = solutionPopen.getLine('stdout')
            if solutionUnprocessedOutput is not None:
                self.__printWithSeparator(solutionUnprocessedOutput, 0, None, None, None)
                interactorPopen.communicate(solutionUnprocessedOutput)

            interactorUnprocessedOutput = interactorPopen.getLine('stdout')
            if interactorUnprocessedOutput is not None:
                self.__printWithSeparator(interactorUnprocessedOutput, Interactor.PADDING, 255, 255, 0)
                solutionPopen.communicate(interactorUnprocessedOutput)

        self.__finish(solutionPopen, interactorPopen, exitError)

def main():
    parser = ArgumentParser()
    parser.add_argument('-sol',
                        action='store',
                        required=True,
                        help='Path to the executable solution.')

    parser.add_argument('-int',
                        action='store',
                        required=True,
                        help='Path to the executable interactor.')

    parser.add_argument('-timeout',
                        action='store',
                        type=float,
                        required=False,
                        default=10,
                        help='Timeout in seconds.')

    parser.add_argument('-input',
                        action='store',
                        required=False,
                        help='Path to the input file for interactor.')

    args = parser.parse_args()
    interactor = Interactor(args)
    runProcess(interactor.run)
