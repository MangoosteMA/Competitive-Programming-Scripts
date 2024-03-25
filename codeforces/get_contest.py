import re
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from library.utils          import colored, set_language, getHtml
from codeforces.get_problem import parse_problem_from_html
from library.contest        import Contest

def parse_contest_from_html(html_code, link=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    title_node = soup.find('div', {'class': 'caption'})
    contest_title = None if title_node is None else title_node.text

    problems = []
    for problem in soup.find_all('div', 'problemindexholder'):
        problems.append(parse_problem_from_html(str(problem)))

    return Contest(title=contest_title, link=link, problems=problems)

def get_contest(url, use_selenium=False):
    html_code = getHtml(set_language(url, 'locale', 'en'), use_selenium=use_selenium)
    if html_code is None:
        return None

    return parse_contest_from_html(html_code, link=url)

def get_all_problems_link(link):
    r = re.compile('https://codeforces.com/contest/[0-9]+')
    link = re.sub('contests', 'contest', link)
    mat = r.match(link)
    assert mat is not None
    return link[mat.span()[0] : mat.span()[1]] + '/problems'

def get_contest_from_args(args):
    if args.html_code is not None:
        contest = parse_contest_from_html(args.html_code, link=args.url)
    else:
        link = get_all_problems_link(args.url)
        print(f'Link to the contest: {link}')
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
