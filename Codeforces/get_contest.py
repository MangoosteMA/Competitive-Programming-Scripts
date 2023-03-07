import requests
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Library.helpers import set_language
from Codeforces.get_problem import parse_problem_from_html
from Library.default_classes import Contest


def parse_contest_from_html(html_code, link=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    contest_title = soup.find('div', {'class': 'caption'}).text
    problems = []
    for problem in soup.find_all('div', 'problemindexholder'):
        problems.append(parse_problem_from_html(str(problem)))

    return Contest(title=contest_title, link=link, problems=problems)


def get_contest(url):
    response = requests.get(set_language(url, 'locale', 'en'))
    if response.status_code != 200:
        return None

    return parse_contest_from_html(response.text, link=url)


def main():
    url = input('Input the link to the problems: ')
    contest = get_contest(url)
    if contest is None:
        print('Failed to load problems.')
        sys.exit(0)

    print(contest)


if __name__ == '__main__':
    main()
