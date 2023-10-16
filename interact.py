import subprocess
from queue import Queue
from threading import Thread
from argparse import ArgumentParser
from time import time

from Library.helpers import colored

parser = ArgumentParser()
parser.add_argument('-solve',
                    action='store',
                    required=True,
                    help='Path to the executable solution.')

parser.add_argument('-interactor',
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
solve_exec = args.solve
interactor_exec = args.interactor


class ExecutingPopen:
    @staticmethod
    def read_loop(stream, queue):
        for line in iter(stream.readline, b''):
            queue.put(line.decode())
        stream.close()

    def __init__(self, executable_file):
        self.running_popen = subprocess.Popen([f'./{executable_file}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.poll = None
        self.reading_threads = dict()
        self.reading_queues = dict()
        for stream_type, stream in zip(['stdout', 'stderr'], [self.running_popen.stdout, self.running_popen.stderr]):
            self.reading_queues[stream_type] = Queue()
            self.reading_threads[stream_type] = Thread(target=self.read_loop, args=(stream, self.reading_queues[stream_type]))
            self.reading_threads[stream_type].start()

    def is_running(self):
        self.poll = self.running_popen.poll()
        return self.poll is None

    def get_line(self, stream):
        assert stream in self.reading_queues
        if self.reading_queues[stream].empty():
            return None
        return self.reading_queues[stream].get()

    def communicate(self, new_line):
        if self.is_running():
            self.running_popen.stdin.write(new_line.encode())
            self.running_popen.stdin.flush()

    def any_thread_alive(self):
        for stream_type, thread in self.reading_threads.items():
            if thread.is_alive():
                return True
        return False

    def terminate(self):
        self.running_popen.terminate()


solve_process = ExecutingPopen(solve_exec)
interactor_process = ExecutingPopen(interactor_exec)

if args.input is not None:
    with open(args.input, 'r') as file:
        for line in file:
            interactor_process.communicate(line)

solve_unprocess_output = ''
interactor_unprocess_output = ''
INTERACTOR_SEPARATOR = '---------------------------------------: '

def process_stderr():
    while True:
        new_line = solve_process.get_line('stderr')
        if new_line is None:
            break
        print(colored('Solve err: ' + new_line, 255, 70, 0), end='')

    while True:
        new_line = interactor_process.get_line('stderr')
        if new_line is None:
            break
        print(colored('Interactor err: ' + new_line, 255, 150, 50), end='')


exit_error = None
start_time = time()

while solve_process.is_running() or interactor_process.is_running():
    process_stderr()

    if time() - start_time > args.timeout:
        exit_error = f'Termiating interaction due to the timeout ({args.timeout} seconds).'
        break

    if not solve_process.is_running() and solve_process.poll != 0:
        exit_error = 'Solution got RE.'
        break

    if not interactor_process.is_running() and interactor_process.poll != 0:
        exit_error = 'Interactor got RE.'
        break

    solve_unprocess_output = solve_process.get_line('stdout')
    interactor_unprocess_output = interactor_process.get_line('stdout')

    if solve_unprocess_output is not None:
        print(colored(solve_unprocess_output, 255, 255, 255), end='')
        interactor_process.communicate(solve_unprocess_output)
    elif interactor_unprocess_output is not None:
        if len(interactor_unprocess_output) > 0:
            print(colored(INTERACTOR_SEPARATOR + interactor_unprocess_output, 255, 255, 0), end='')
        solve_process.communicate(interactor_unprocess_output)

solve_process.terminate()
interactor_process.terminate()

while solve_process.any_thread_alive() or solve_process.any_thread_alive():
    process_stderr()

if exit_error is not None:
    print(colored('\n' + exit_error, 255, 70, 0))
