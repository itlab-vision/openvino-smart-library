class Model:
    def __init__(self, model_id, file_path, name_model):
        self.model_id = model_id
        self.file_path = file_path
        self.name_model = name_model
        
    def _print(self):
        print(self.model_id)
        print(self.file_path)
        print(self.name_model)