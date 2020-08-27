

class TableItem:
    name = ""
    url = ""
    description = ""

    def __init__(self):
        pass

    def __eq__(self, other):
        return self.name == other.name and self.url == other.url and self.description == other.description
