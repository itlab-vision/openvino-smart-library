class Role:
    def __init__(self, role_id, description):
        self.role_id = role_id
        self.description = description
        
    def _print(self):
        print(self.role_id)
        print(self.description)