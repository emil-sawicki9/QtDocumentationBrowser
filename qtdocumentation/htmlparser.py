from html.parser import HTMLParser
from abc import ABC


class QtTypesListParser(HTMLParser, ABC):
    parsing_qt_classes = False
    parsing_qml_types = False
    found_dd = False
    current_link = ""
    links = {}

    def parse_qt_classes(self, data):
        self.clear()
        self.parsing_qt_classes = True
        self.feed(data)
        return self.links

    def parse_qml_types(self, data):
        self.clear()
        self.parsing_qml_types = True
        self.feed(data)
        return self.links

    def clear(self):
        self.parsing_qt_classes = False
        self.parsing_qml_types = False
        self.found_dd = False
        self.current_link = ""
        self.links = {}

    def handle_starttag(self, tag, attrs):
        if tag == "dd":
            self.found_dd = True
            return
        elif tag == "a" and self.found_dd and len(attrs) > 0:
            href = attrs[0]
            if href[0] == "href":
                self.current_link = attrs[0][1]
        self.found_dd = False

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.current_link and len(data) > 1:
            if self.parsing_qt_classes and not data.startswith('Q'):
                return
            self.links[data] = self.current_link
        self.current_link = ""