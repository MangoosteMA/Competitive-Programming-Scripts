from bs4 import BeautifulSoup

from cpscripts.lib.problem import Problem

def parseProblemFromHtml(html: str, link: str=None) -> Problem:
    soup = BeautifulSoup(html, 'html.parser')

    sampleNode = soup.find(attrs={'class': 'problem-statement'})
    index = None
    title = None
    if sampleNode is not None:
        titleNode = sampleNode.find(attrs={'class': 'title'})
        if titleNode is not None:
            index = titleNode.text[0]
            if len(titleNode.text) >= 4:
                title = titleNode.text[3:]

    samplesNodes = soup.find_all(attrs={'class': 'sample-tests'})
    inputs = []
    outputs = []

    for sampleNode in samplesNodes:
        testHolders = sampleNode.find_all('pre')
        if len(testHolders) == 2:
            inputs.append(testHolders[0].text)
            outputs.append(testHolders[1].text)

    return Problem(title=title, index=index, link=link, inputs=inputs, outputs=outputs)
