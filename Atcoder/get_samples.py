import requests
from bs4 import BeautifulSoup
import re

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from Library.helpers import set_language

url = input('input the link to the problem: ')
response = requests.get(set_language(url, 'lang', 'en')).text
soup = BeautifulSoup(response, 'html.parser')

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

print(len(inputs))
for i in range(len(inputs)):
    print(f'Test #{i + 1}')
    print('Input:')
    print(inputs[i].strip('\n'))
    print('\nOutput:')
    print(outputs[i].strip('\n'))
    print()
