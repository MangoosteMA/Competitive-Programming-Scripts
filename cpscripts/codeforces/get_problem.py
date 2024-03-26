import re
from bs4 import BeautifulSoup

from cpscripts.lib.problem import Problem

def parseProblemFromHtml(html: str, link: str=None) -> Problem:
    soup = BeautifulSoup(html, 'html.parser')
    problemNode = soup.find('div', {'class' : 'problemindexholder'})

    index = problemNode['problemindex']
    title = problemNode.find('div', {'class': 'problem-statement'}).find('div', {'class': 'header'}).find('div', {'class': 'title'}).text
    title = ''.join(title.split('.')[1:]).strip()
    inputs = []
    outputs = []

    for node in problemNode.find('div', {'class': 'sample-test'}).children:
        preNode = node.find('pre', recursive=False)
        text = ''
        for child in preNode.children:
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

    return Problem(title=title, index=index, link=link, tags=tags, difficulty=difficulty, inputs=inputs, outputs=outputs)
