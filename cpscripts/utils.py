import json
import os
import requests

from enum   import Enum
from typing import Optional, Any

def compareOutput(outputLines: list[str], correctOutputLines: list[str]) -> list[int]:
    if correctOutputLines is None or outputLines is None:
        return True

    for i in range(0, max(len(outputLines), len(correctOutputLines))):
        outputLine = outputLines[i] if i < len(outputLines) else ''
        correctLine = correctOutputLines[i] if i < len(correctOutputLines) else ''
        if outputLine.strip() != correctLine.strip():
            return False

    return True

def addEmptyLine(lines: list[str]) -> list[str]:
    clone = [line for line in lines]
    if len(clone) == 0 or len(clone[-1]) != 0:
        clone.append('')
    return clone

def colorfedLinesPrint(lines: list[str], correctLines: list[str], r: int, g: int, b: int) -> None:
    for i, line in enumerate(lines):
        if correctLines is None:
            print(line)
            continue

        lineParts = line.split(' ')
        correctParts = (correctLines[i] if correctLines is not None and i < len(correctLines) else '').split(' ')
        coloredParts = []
        for j, part in enumerate(lineParts):
            correctPart = correctParts[j] if j < len(correctParts) else ''
            if part != correctPart:
                coloredParts.append(colored(part, r, g, b))
            else:
                coloredParts.append(part)
        
        print(' '.join(coloredParts))

class JudgeSystem(Enum):
    CODEFORCES     = 0
    ATCODER        = 1
    YANDEX_CONTEST = 2

    @staticmethod
    def determineFromHtml(html: str):
        codeforcesCount = html.count('codeforces')
        atcoderCount = html.count('atcoder')
        yandexCount = html.count('yandex') + html.count('Yandex')

        if codeforcesCount > max(atcoderCount, yandexCount):
            return JudgeSystem.CODEFORCES
        elif atcoderCount > max(codeforcesCount, yandexCount):
            return JudgeSystem.ATCODER
        elif yandexCount > max(codeforcesCount, atcoderCount):
            return JudgeSystem.YANDEX_CONTEST
        else:
            return None

def colored(text: str, red: int, green: int, blue: int) -> str:
    return f'\033[38;2;{red};{green};{blue}m{text}\033[0m'

def dumpError(message: str) -> None:
    print(colored(message, 255, 70, 0))

def getHtml(url: str) -> Optional[str]:
    result = requests.get(url)
    return None if result.status_code != 200 else result.text

def loadSettings() -> dict[str: Any]:
    settingsPath = os.path.join(os.path.dirname(__file__), 'settings.json')
    with open(settingsPath, 'r') as settingsFile:
        jsonData = json.loads(settingsFile.read())
    
    return jsonData
