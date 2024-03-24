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
