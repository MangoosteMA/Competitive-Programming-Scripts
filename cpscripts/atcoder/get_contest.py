from bs4 import BeautifulSoup

from cpscripts.lib.contest         import Contest
from cpscripts.utils               import colored, getHtml
from cpscripts.atcoder.get_problem import getProblemIndexAndTitle, parseProblemFromHtml

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
