import requests
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


url_qml_types = "https://doc.qt.io/qt-5/qmltypes.html"
url_qt_classes = "https://doc.qt.io/qt-5/classes.html"

response = requests.get(url_qml_types)

parser = MyHTMLParser()
parser.feed(response.text)
