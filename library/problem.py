class Problem:
    def __init__(self, title: str=None, index: str=None, link: str=None, tags: str=None,\
                 difficulty: int=None, inputs: list[str]=None, outputs: list[str]=None):
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
