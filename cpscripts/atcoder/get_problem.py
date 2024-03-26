import re
from bs4 import BeautifulSoup

from cpscripts.lib.problem import Problem

def getProblemIndexAndTitle(name: str) -> tuple[str, str]:
    pos = name.find('-')
    return (name[:pos - 1], name[pos + 2:])

def parseProblemFromHtml(html: str, link: str=None) -> Problem:
    soup = BeautifulSoup(html, 'html.parser')

    titleNode = soup.find('title')
    title = None
    index = None
    if titleNode is not None:
        index, title = getProblemIndexAndTitle(titleNode.text)

    inputRegex = re.compile(r'Sample Input [0-9]+')
    outputRegex = re.compile(r'Sample Output [0-9]+')
    inputs = []
    outputs = []

    for rootNode in soup.find_all('div', {'class': 'part'}):
        title = rootNode.find('h3').text
        if inputRegex.match(title):
            inputs.append(rootNode.find('pre').text)
        elif outputRegex.match(title):
            outputs.append(rootNode.find('pre').text)

    return Problem(title=title, index=index, link=link, inputs=inputs, outputs=outputs)
