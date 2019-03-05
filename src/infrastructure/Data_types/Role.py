class Role:
    def __init__(self, role_id = -1, description = -1):
        self.role_id = role_id
        self.description = description
        
    def _print(self):
        print(self.role_id)
        print(self.description)