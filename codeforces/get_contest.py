import os
import re
import sys
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from library.utils          import colored, getHtml
from codeforces.get_problem import parseProblemFromHtml
from library.contest        import Contest

def parseContestFromHtml(html: str, link: str=None) -> Contest:
    soup = BeautifulSoup(html, 'html.parser')
    titleNode = soup.find('div', {'class': 'caption'})
    title = None if titleNode is None else titleNode.text

    problems = []
    for problem in soup.find_all('div', 'problemindexholder'):
        problems.append(parseProblemFromHtml(str(problem)))

    return Contest(title=title, link=link, problems=problems)
