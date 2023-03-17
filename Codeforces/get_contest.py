import re
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Library.helpers import set_language, get_html_code
from Codeforces.get_problem import parse_problem_from_html
from Library.default_classes import Contest


def parse_contest_from_html(html_code, link=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    title_node = soup.find('div', {'class': 'caption'})
    contest_title = None if title_node is None else title_node.text

    problems = []
    for problem in soup.find_all('div', 'problemindexholder'):
        problems.append(parse_problem_from_html(str(problem)))

    return Contest(title=contest_title, link=link, problems=problems)


def get_contest(url, use_selenium=False):
    html_code = get_html_code(set_language(url, 'locale', 'en'), use_selenium=use_selenium)
    if html_code is None:
        return None

    return parse_contest_from_html(html_code, link=url)


def get_all_problems_link(link):
    r = re.compile('https://codeforces.com/contest/[0-9]+')
    mat = r.match(link)
    assert mat is not None
    return link[mat.span()[0] : mat.span()[1]] + '/problems'


def get_contest_from_args(args):
    contest = get_contest(get_all_problems_link(args.url), use_selenium=args.selenium)
    return contest


def main():
    url = input('Input the link to the problems: ')
    contest = get_contest(url, use_selenium=False)
    if contest is None:
        print('Failed to load problems.')
        sys.exit(0)

    print(contest)


if __name__ == '__main__':
    main()
