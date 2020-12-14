

class TableItem:
    name = ""
    url = ""
    description = ""
    pinned_index = 0
    use_count = 0
    last_used = None

    def __init__(self):
        pass

    def __eq__(self, other):
        return self.name == other.name and self.url == other.url and self.description == other.description
