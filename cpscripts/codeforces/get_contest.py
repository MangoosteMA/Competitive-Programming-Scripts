from bs4 import BeautifulSoup

from cpscripts.lib.contest            import Contest
from cpscripts.utils                  import colored, getHtml
from cpscripts.codeforces.get_problem import parseProblemFromHtml

def parseContestFromHtml(html: str, link: str=None) -> Contest:
    soup = BeautifulSoup(html, 'html.parser')
    titleNode = soup.find('div', {'class': 'caption'})
    title = None if titleNode is None else titleNode.text

    problems = []
    for problem in soup.find_all('div', 'problemindexholder'):
        problems.append(parseProblemFromHtml(str(problem)))

    return Contest(title=title, link=link, problems=problems)
