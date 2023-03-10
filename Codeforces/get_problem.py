import requests
import re
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from Library.helpers import set_language
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


def get_problem(url):
    response = requests.get(set_language(url, 'locale', 'en'))
    if response.status_code != 200:
        return None

    return parse_problem_from_html(response.text, link=url)


def main():
    url = input('Input the link to the problem: ')
    problem = get_problem(url)
    if problem is None:
        print('Failed to load tests.')
        sys.exit(0)

    print(problem)


if __name__ == '__main__':
    main()
