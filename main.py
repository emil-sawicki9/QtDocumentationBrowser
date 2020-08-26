import requests
import sys

from PyQt5.QtWidgets import QApplication

from documentationviewer.mainwindow import MainWindow
from qtdocumentation.constant import QT_BASE_URL
from qtdocumentation.htmlparser import QtTypesListParser

app = QApplication(sys.argv)
window = MainWindow()

response_qt_classes = requests.get(QT_BASE_URL + "classes.html")
response_qml_types = requests.get(QT_BASE_URL + "qmltypes.html")

parser = QtTypesListParser()
qt_classes_dictionary = parser.parse_qt_classes(response_qt_classes.text)
qml_types_dictionary = parser.parse_qml_types(response_qml_types.text)

window.model.populate_model(qt_classes_dictionary, QT_BASE_URL, "Qt class")
# window.model.populate_model(qml_types_dictionary, QT_BASE_URL, "QML type")

window.show()

sys.exit(app.exec_())
