import re
import requests
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Library.helpers import colored
from Library.helpers import set_language, get_html_code
from Atcoder.get_problem import get_problem_index_and_title, parse_problem_from_html
from Library.default_classes import Contest


def parse_contest_from_html(html_code, link=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    title_node = soup.find('title')
    contest_title = None if title_node is None else title_node.text

    problems = []
    for problem in soup.find_all('span', 'lang-en'):
        problems.append(parse_problem_from_html(str(problem)))

    for index, title in enumerate(soup.find_all('span', {'class': 'h2'})):
        problems[index].index, problems[index].title = get_problem_index_and_title(title.text)

    return Contest(title=contest_title, link=link, problems=problems)


def get_contest(url, use_selenium=False):
    html_code = get_html_code(set_language(url, 'lang', 'en'), use_selenium=use_selenium)
    if html_code is None:
        return None

    return parse_contest_from_html(html_code, link=url)


def get_all_problems_link(link):
    r = re.compile('https://atcoder.jp/contests/[^/]+')
    mat = r.match(link)
    assert mat is not None
    return link[mat.span()[0] : mat.span()[1]] + '/tasks_print'


def get_contest_from_args(args):
    link = get_all_problems_link(args.url)
    print(f'Link to the problems: {link}')
    while True:
        contest = get_contest(link, use_selenium=args.selenium)
        if contest.problems is None:
            print(colored('Failed to load the contest. Trying to load again.', 255, 0, 0))
            continue
        if len(contest.problems) == 0:
            print(colored('None problems parsed. Trying to load again.', 255, 0, 0))
            continue
        break
            
    print(colored('Contest is loaded!\n', 0, 255, 0))
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
