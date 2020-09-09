class Model:
    def __init__(self, user_id, vec):
        self.user_id = user_id
        self.vec = vec

    def _print(self):
        print(self.user_id)
        print(self.vec)