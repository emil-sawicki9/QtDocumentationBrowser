

class TableItem:
    name = ""
    url = ""
    description = ""

    def __init__(self):
        pass

    def __eq__(self, other):
        return self.name == other.name and self.link == other.link and self.description == other.description
