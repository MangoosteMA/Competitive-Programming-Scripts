import requests

from enum   import Enum
from typing import Optional

def compareOutput(outputLines: list[str], correctOutputLines: list[str]) -> list[int]:
    if correctOutputLines is None or outputLines is None:
        return []

    differentLines = []
    for i in range(0, max(len(outputLines), len(correctOutputLines))):
        outputLine = outputLines[i] if i < len(outputLines) else ''
        correctLine = correctOutputLines[i] if i < len(correctOutputLines) else ''
        if outputLine.strip() != correctLine.strip():
            differentLines.append(i)

    return differentLines

def addEmptyLine(lines: list[str]) -> list[str]:
    clone = [line for line in lines]
    if len(clone) == 0 or len(clone[-1]) != 0:
        clone.append('')
    return clone

def colorfulLinesPrint(lines: list[str], differentLines: list[int], r: int, g: int, b: int) -> None:
    differentLines.sort()
    linePtr = 0
    for i, line in enumerate(lines):
        while linePtr < len(differentLines) and differentLines[linePtr] < i:
            linePtr += 1

        if linePtr < len(differentLines) and differentLines[linePtr] == i:
            print(colored(line, r, g, b))
        else:
            print(line)

class JudgeSystem(Enum):
    CODEFORCES = 0
    ATCODER    = 1

    @staticmethod
    def determineFromHtml(html: str):
        codeforcesCount = html.count('codeforces')
        atcoderCount = html.count('atcoder')
        if codeforcesCount > atcoderCount:
            return JudgeSystem.CODEFORCES
        elif atcoderCount > codeforcesCount:
            return JudgeSystem.ATCODER
        else:
            return None

def colored(text: str, red: int, green: int, blue: int) -> str:
    return f'\033[38;2;{red};{green};{blue}m{text}\033[0m'

def dumpError(message: str) -> None:
    print(colored(message, 255, 70, 0))

def getHtml(url: str) -> Optional[str]:
    result = requests.get(url)
    return None if result.status_code != 200 else result.text
