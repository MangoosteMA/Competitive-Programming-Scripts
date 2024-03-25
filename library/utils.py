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

def set_language(link, lang_flag, lang='en'):
    pos = link.find(lang_flag)
    if pos == -1:
        return link + '?' + lang_flag + '=' + lang
    pos += len(lang_flag) + 1
    assert link[pos - 1] == '='
    return link[:pos] + lang

def determine_system(link):
    if link.find('codeforces') != -1:
        return 'codeforces'
    elif link.find('atcoder') != -1:
        return 'atcoder'
    else:
        return None

def determine_system_from_html(html_code):
    codeforces_count = html_code.count('codeforces')
    atcoder_count = html_code.count('atcoder')
    if codeforces_count > atcoder_count:
        return 'codeforces'
    elif atcoder_count > codeforces_count:
        return 'atcoder'
    else:
        return None

def colored(text, red, green, blue):
    return f'\033[38;2;{red};{green};{blue}m{text}\033[0m'

def dumpError(message):
    print(colored(message, 255, 70, 0))

def get_html_code(url, use_selenium=False):
    if not use_selenium:
        import requests
        result = requests.get(url)
        return None if result.status_code != 200 else result.text
    else:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print('Creating driver.')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        print('Requesting data.')
        driver.get(url)
        html_code = driver.page_source
        driver.close()
        print('Got html code!')
        return html_code
