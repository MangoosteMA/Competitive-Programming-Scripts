import re
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Library.helpers import set_language, get_html_code
from Library.default_classes import Problem


def parse_problem_from_html(html_code, link=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    problem_node = soup.find('div', {'class' : 'problemindexholder'})

    problem_index = problem_node['problemindex']
    problem_title = problem_node.find('div', {'class': 'problem-statement'}).find('div', {'class': 'header'}).find('div', {'class': 'title'}).text
    problem_title = ''.join(problem_title.split('.')[1:]).strip()
    inputs = []
    outputs = []

    for node in problem_node.find('div', {'class': 'sample-test'}).children:
        pre_node = node.find('pre', recursive=False)
        text = ''
        for child in pre_node.children:
            if child.name == 'br':
                text += '\n'
            text += child.text
            if child.name == 'div':
                text += '\n'
        text = text.strip('\n') + '\n'
        if node['class'] == ['input']:
            inputs.append(text)
        elif node['class'] == ['output']:
            outputs.append(text)

    tags = []
    difficulty = None
    for node in soup.find_all('span', {'class': 'tag-box'}):
        if node['title'] == 'Difficulty':
            difficulty = int(re.sub('[^0-9]', '', node.text))
        else:
            tags.append(str(node.text).strip())

    return Problem(title=problem_title, index=problem_index, link=link, tags=tags, difficulty=difficulty, inputs=inputs, outputs=outputs)


def get_problem(url, use_selenium=False):
    html_code = get_html_code(set_language(url, 'locale', 'en'), use_selenium=use_selenium)
    if html_code is None:
        return None

    return parse_problem_from_html(html_code, link=url)


def main():
    url = input('Input the link to the problem: ')
    problem = get_problem(url, use_selenium=False)
    if problem is None:
        print('Failed to load tests.')
        sys.exit(0)

    print(problem)


if __name__ == '__main__':
    main()
