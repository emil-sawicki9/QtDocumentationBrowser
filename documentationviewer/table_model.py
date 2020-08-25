from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QVariant, Qt

from .tableitem import TableItem
import warnings


class TableModel(QAbstractItemModel):
    data_list = []
    _column_name = 0
    _column_type = 1
    _header_data = ["Name", "Type"]

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        # self.setHeaderData(0, Qt.Horizontal, "Name", Qt.DisplayRole)
        # self.setHeaderData(1, Qt.Horizontal, "Type")

    def rowCount(self, parent = QModelIndex()):
        return len(self.data_list)

    def columnCount(self, parent):
        return 2

    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)

    def parent(self, child):
        return QModelIndex()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_data[section]
        else:
            return QVariant()

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self.data_list) or role != Qt.DisplayRole:
            return QVariant()

        item = self.data_list[index.row()]
        if index.column() == self._column_name:
            return item.name
        elif index.column() == self._column_type:
            return item.description
        return QVariant()

    def append_item(self, name, link, item_type):
        item = TableItem()
        item.name = name
        item.link = link
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
            link = data[qt_class]
            self.append_item(qt_class, base_url + link, item_type)
