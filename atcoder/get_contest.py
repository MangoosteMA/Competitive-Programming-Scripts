import os
import re
import sys
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from library.utils       import colored, getHtml
from atcoder.get_problem import getProblemIndexAndTitle, parseProblemFromHtml
from library.contest     import Contest

def parseContestFromHtml(html: str, link: str=None) -> Contest:
    soup = BeautifulSoup(html, 'html.parser')
    titleNode = soup.find('title')
    title = None if titleNode is None else titleNode.text

    problems = []
    for problem in soup.find_all('span', 'lang-en'):
        problems.append(parseProblemFromHtml(str(problem)))

    for index, title in enumerate(soup.find_all('span', {'class': 'h2'})):
        problems[index].index, problems[index].title = getProblemIndexAndTitle(title.text)

    return Contest(title=title, link=link, problems=problems)
