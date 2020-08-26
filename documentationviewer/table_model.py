from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QVariant, Qt

from .tableitem import TableItem
import warnings


class TableModel(QAbstractItemModel):
    # Roles
    NameRole = Qt.UserRole + 1
    DescriptionRole = Qt.UserRole + 2
    column_list = [NameRole, DescriptionRole]
    # Data
    data_list = []
    # Private
    _column_name = 0
    _column_type = 1
    _header_data = ["Name", "Type"]

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)

    def rowCount(self, parent = QModelIndex()):
        return len(self.data_list)

    def columnCount(self, parent):
        return 2

    def index(self, row, column, parent = QModelIndex()):
        return self.createIndex(row, column, parent)

    def parent(self, child):
        return QModelIndex()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_data[section]
        else:
            return QVariant()

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
        return QVariant()

    def append_item(self, name, url, item_type):
        item = TableItem()
        item.name = name
        item.url = url
        item.description = item_type
        # Check if item already exists
        for d in self.data_list:
            if d == item:
                warnings.warn("Item already exists in model: " + name)
                return

        self.beginInsertColumns(QModelIndex(), self.rowCount(), self.rowCount())
        self.data_list.append(item)
        self.endInsertRows()

    def populate_model(self, data, base_url, item_type):
        for qt_class in data:
            url = data[qt_class]
            self.append_item(qt_class, base_url + url, item_type)

    def _is_valid_index(self, index):
        return index.isValid() and index.row() < len(self.data_list)

    def get_url(self, index):
        if not self._is_valid_index(index):
            return ""

        item = self.data_list[index.row()]
        return item.url
