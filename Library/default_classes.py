class Problem:
    def __init__(self, title=None, index=None, link=None, tags=None, difficulty=None, inputs=None, outputs=None):
        self.title = title
        self.index = index
        self.link = link
        self.difficulty = difficulty
        self.tags = tags
        self.inputs = None if inputs is None else [x.strip('\n') + '\n' for x in inputs]
        self.outputs = None if outputs is None else [x.strip('\n') + '\n' for x in outputs]

    def __str__(self):
        result = f'Title: {self.title}\n'
        result += f'Index: {self.index}\n'
        result += f'Link: {self.link}\n'
        result += f'Tags: {self.tags}\n'
        result += f'Difficulty: {self.difficulty}'
        if self.inputs is None:
            result += '\nTests: None'
        else:
            result += '\n'
            result += f'Tests count: {len(self.inputs)}\n'
            result += f'Inputs: {self.inputs}\n'
            result += f'Outputs: {self.outputs}'
        return result


class Contest:
    def __init__(self, title=None, link=None, problems=None):
        self.title = title
        self.link = link
        self.problems = problems

    def __str__(self):
        result = f'Title: {self.title}\n'
        result += f'Link: {self.link}'
        if self.problems is None:
            result += '\nProblems: None'
        else:
            result += '\n'
            result += f'Problems count: {len(self.problems)}'
            for problem in self.problems:
                result += '\n\n' + str(problem)
        return result
