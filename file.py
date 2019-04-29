from pathlib import Path

class File:
    def __init__(self, path, name):
        self.name = name
        self.path = Path(path, name)
        
    def __str__(self):
        return str(self.path)
    
    def __repr__(self):
        "File(name: {}, path: {})".format(self.name, self.path)