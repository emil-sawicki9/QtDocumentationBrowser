import threading
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QVariant, Qt, QByteArray, QSettings

from documentation_model.table_item import TableItem
import warnings


class DocumentationModel(QAbstractItemModel):
    # Roles
    NameRole = Qt.UserRole + 1
    DescriptionRole = Qt.UserRole + 2
    UrlRole = Qt.UserRole + 3
    UseCountRole = Qt.UserRole + 4
    IsPinnedRole = Qt.UserRole + 5
    PinnedIndexRole = Qt.UserRole + 6
    LastUsedRole = Qt.UserRole + 7
    # Data
    column_list = [NameRole, DescriptionRole]
    data_list = []

    # Private
    _settings = QSettings("LidoSoft", "QtDocumentationViewer")
    _lock = threading.Lock()

    def __init__(self, parent=None):
        super(DocumentationModel, self).__init__(parent)

    def rowCount(self, parent=QModelIndex()):
        return len(self.data_list)

    def columnCount(self, parent):
        return 2

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, parent)

    def parent(self, child):
        return QModelIndex()

    def roleNames(self):
        return {
            self.NameRole: b'name',
            self.DescriptionRole: b'description',
            self.UrlRole: b'url',
            self.IsPinnedRole: b'isPinned'
        }

    def data(self, index, role):
        if role == Qt.DisplayRole:
            role = self.column_list[index.column()]
        if not self._is_valid_index(index) or role <= Qt.UserRole:
            return QVariant()

        item = self.data_list[index.row()]
        if role == self.NameRole:
            return item.name
        elif role == self.DescriptionRole:
            return item.description
        elif role == self.UrlRole:
            return item.url
        elif role == self.LastUsedRole:
            return item.last_used
        elif role == self.IsPinnedRole:
            return item.pinned_index >= 0
        elif role == self.PinnedIndexRole:
            return item.pinned_index
        elif role == self.UseCountRole:
            return item.use_count
        return QVariant()

    def pin_item(self, url, pin):
        # Pin item to frontpage
        found_item = self._find_item_with_url(url)
        if found_item is None:
            return

        item = found_item['item']
        if pin:
            item.pinned_index = self._find_last_pinned_index() + 1
        else:
            item.pinned_index = -1

        self._update_pinned_list()

        index = found_item['index']
        model_index = self.createIndex(index, 0)
        self.dataChanged.emit(model_index, model_index, [self.IsPinnedRole, self.PinnedIndexRole])

    def update_item_used(self, url):
        # Updating latest and most used
        found_item = self._find_item_with_url(url)
        if found_item is None:
            return

        item = found_item['item']
        item.last_used = time.time()
        item.use_count += 1

        index = found_item['index']
        model_index = self.createIndex(index, 0)
        self.dataChanged.emit(model_index, model_index, [self.LastUsedRole, self.UseCountRole])

    def append_item(self, name, url, item_type, pinned_index):
        item = TableItem()
        item.name = name
        item.url = url
        item.description = item_type
        item.pinned_index = pinned_index
        # Check if item already exists
        for d in self.data_list:
            if d == item:
                warnings.warn("Item already exists in model: " + name)
                return

        self.beginInsertColumns(QModelIndex(), self.rowCount(), self.rowCount())
        self.data_list.append(item)
        self.endInsertRows()

    def populate_model(self, data, base_url, item_type):
        self._lock.acquire()
        try:
            pinned_list = self._settings.value("pinned_url", [], str)
            for qt_class in data:
                url = base_url + data[qt_class]
                pinned_index = self._get_index_of_item(pinned_list, url)
                self.append_item(qt_class, url, item_type, pinned_index)
        finally:
            self._lock.release()

    def _update_pinned_list(self):
        pinned_item_list = []
        for item in self.data_list:
            if item.pinned_index >= 0:
                pinned_item_list.append(item)

        sort_lambda = lambda i: i.pinned_index
        pinned_item_list.sort(key=sort_lambda)
        pinned_url_list = []
        for item in pinned_item_list:
            pinned_url_list.append(item.url)
        self._settings.setValue("pinned_url", pinned_url_list)
        self._settings.sync()

    def move_pin_item(self, url, move_up):
        # Pin item to frontpage
        found_item = self._find_item_with_url(url)
        if found_item is None:
            return

        item = found_item['item']
        item_on_same_place = None
        item_on_same_place_index = 0
        if move_up:
            new_pinned_index = item.pinned_index - 1
        else:
            new_pinned_index = item.pinned_index + 1
        for item2 in self.data_list:
            if item2.pinned_index == new_pinned_index:
                item_on_same_place = item2
                break
            item_on_same_place_index += 1

        if item_on_same_place is None:
            return

        item_on_same_place.pinned_index = item.pinned_index
        item.pinned_index = new_pinned_index

        self._update_pinned_list()

        index = found_item['index']
        model_index = self.createIndex(index, 0)
        model_index2 = self.createIndex(item_on_same_place_index, 0)
        self.dataChanged.emit(model_index, model_index, [self.IsPinnedRole, self.PinnedIndexRole])
        self.dataChanged.emit(model_index2, model_index2, [self.IsPinnedRole, self.PinnedIndexRole])

    def _is_valid_index(self, index):
        return index.isValid() and index.row() < len(self.data_list)

    def _find_item_with_url(self, url):
        index = 0
        for item in self.data_list:
            if item.url == url:
                return {'item': item, "index": index}
            index += 1
        else:
            return None

    def _get_index_of_item(self, array, item):
        index = 0
        for x in array:
            if x == item:
                return index
            index += 1
        return -1

    def _find_last_pinned_index(self):
        max_pinned_index = 0
        for item in self.data_list:
            max_pinned_index = max(item.pinned_index, max_pinned_index)
        return max_pinned_index
