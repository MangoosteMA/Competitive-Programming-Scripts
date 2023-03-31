import re
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Library.helpers import set_language, get_html_code
from Library.default_classes import Problem


def get_problem_index_and_title(name):
    pos = name.find('-')
    return (name[:pos - 1], name[pos + 2:])


def parse_problem_from_html(html_code, link=None):
    soup = BeautifulSoup(html_code, 'html.parser')

    title_node = soup.find('title')
    problem_title = None
    problem_index = None
    if title_node is not None:
        problem_index, problem_title = get_problem_title_and_index(title_node.text)

    regex_input = re.compile(r'Sample Input [0-9]+')
    regex_output = re.compile(r'Sample Output [0-9]+')
    inputs = []
    outputs = []

    for root_node in soup.find_all('div', {'class': 'part'}):
        title = root_node.find('h3').text
        if regex_input.match(title):
            inputs.append(root_node.find('pre').text)
        elif regex_output.match(title):
            outputs.append(root_node.find('pre').text)

    return Problem(title=problem_title, index=problem_index, link=link, inputs=inputs, outputs=outputs)


def get_problem(url, use_selenium=False):
    html_code = get_html_code(set_language(url, 'lang', 'en'), use_selenium=use_selenium)
    if html_code is None:
        return None

    return parse_problem_from_html(html_code, link=url)


def get_problem_from_args(args):
    return get_problem(args.url, use_selenium=args.selenium)


def main():
    url = input('Input the link to the problem: ')
    problem = get_problem(url, use_selenium=False)
    if problem is None:
        print('Failed to load tests.')
        sys.exit(0)

    print(problem)


if __name__ == '__main__':
    main()
