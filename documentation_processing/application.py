import requests
from PyQt5.QtCore import QUrl, pyqtSlot, QTimer
from PyQt5.QtGui import QGuiApplication, QDesktopServices
from PyQt5.QtQml import QQmlApplicationEngine

import qml_qrc
from documentation_model.documentation_model import DocumentationModel
from documentation_model.documentation_proxy_model import DocumentationFilterModel

from documentation_processing.constant import QT_BASE_URL
from documentation_processing.qtitemhtmlparser import QtItemHtmlParser
from documentation_processing.qtitemlisthtmlparser import QtItemListHtmlParser


class Application(QGuiApplication):
    documentation_model = DocumentationModel()
    proxy_model = DocumentationFilterModel()
    pinned_model = DocumentationFilterModel()
    latest_model = DocumentationFilterModel()
    most_used_model = DocumentationFilterModel()
    qml_engine = None

    def __init__(self, argv):
        super().__init__(argv)

        # Setting up proxy models
        self.proxy_model.setSourceModel(self.documentation_model)
        self.pinned_model.setSourceModel(self.documentation_model)
        self.pinned_model.show_only_pinned = True
        self.latest_model.setSourceModel(self.documentation_model)
        self.latest_model.show_only_latest = True
        self.most_used_model.setSourceModel(self.documentation_model)
        self.most_used_model.show_only_most_used = True

        # Populating model
        # TODO Use thread to populate documentation model
        populate_lambda = lambda: self._populate_qt_models()
        QTimer.singleShot(1000, populate_lambda)
        # Initializing QML
        self.init_ui()

    def init_ui(self):
        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine.rootContext().setContextProperty("documentationModel", self.proxy_model)
        self.qml_engine.rootContext().setContextProperty("pinnedModel", self.pinned_model)
        self.qml_engine.rootContext().setContextProperty("latestModel", self.latest_model)
        self.qml_engine.rootContext().setContextProperty("mostUsedModel", self.most_used_model)
        self.qml_engine.rootContext().setContextProperty("app", self)
        self.qml_engine.load(QUrl("qrc:/qml/main.qml"))
        # Debug: only for faster testing of parsing specific docs.
        # self.open_new_tab("https://doc.qt.io/qt-5/q3dbars.html")

    @pyqtSlot(str)
    def open_new_tab(self, url):
        parser = QtItemHtmlParser()
        data = parser.parse_qt_item(url)

    @pyqtSlot(str)
    def open_in_external_browser(self, url):
        self.documentation_model.update_item_used(url)
        self.latest_model.sort(0)
        self.most_used_model.sort(0)
        QDesktopServices.openUrl(QUrl(url))

    @pyqtSlot(str, bool)
    def pin_item(self, url, pin):
        self.documentation_model.pin_item(url, pin)
        self.pinned_model.sort(0)

    def _populate_qt_models(self):
        response_qt_classes = requests.get(QT_BASE_URL + "classes.html")
        response_qml_types = requests.get(QT_BASE_URL + "qmltypes.html")

        parser = QtItemListHtmlParser()
        qt_classes_dictionary = parser.parse_qt_classes(response_qt_classes.text)
        qml_types_dictionary = parser.parse_qml_types(response_qml_types.text)

        self.documentation_model.populate_model(qt_classes_dictionary, QT_BASE_URL, "Qt class")
        self.documentation_model.populate_model(qml_types_dictionary, QT_BASE_URL, "QML type")
