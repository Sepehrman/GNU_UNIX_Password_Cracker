class Request():

    def __init__(self):
        self.users = None
        self.file = None

    def __str__(self):
        return f'(users: {self.users}, file: {self.file})'

    def __repr__(self):
        return f'(users: {self.users}, file: {self.file})'
