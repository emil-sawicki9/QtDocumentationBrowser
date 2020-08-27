import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from documentation_model.table_model import TableModel
from documentation_model.table_proxy_model import TableProxyModel
import webbrowser
import warnings

from documentation_processing.constant import QT_BASE_URL
from documentation_processing.qthtmlparser import QtHtmlParser


class Application(QGuiApplication):
    model = TableModel()
    proxy_model = TableProxyModel()
    qml_engine = None

    def __init__(self, argv):
        super().__init__(argv)
        self.proxy_model.setSourceModel(self.model)
        self.qml_engine = QQmlApplicationEngine()
        self._populate_qt_models()
        self.init_ui()

    def init_ui(self):
        self.qml_engine.rootContext().setContextProperty("documentationModel", self.proxy_model)
        self.qml_engine.load(QUrl("qml/main.qml"))

    def _populate_qt_models(self):
        response_qt_classes = requests.get(QT_BASE_URL + "classes.html")
        response_qml_types = requests.get(QT_BASE_URL + "qmltypes.html")

        parser = QtHtmlParser()
        qt_classes_dictionary = parser.parse_qt_classes(response_qt_classes.text)
        qml_types_dictionary = parser.parse_qml_types(response_qml_types.text)

        self.model.populate_model(qt_classes_dictionary, QT_BASE_URL, "Qt class")
        self.model.populate_model(qml_types_dictionary, QT_BASE_URL, "QML type")
