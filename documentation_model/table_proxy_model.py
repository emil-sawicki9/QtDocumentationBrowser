from PyQt5.QtCore import QSortFilterProxyModel, pyqtSlot
import re

from documentation_model.table_model import TableModel


class TableProxyModel(QSortFilterProxyModel):
    _filtered_text = ""

    def __init__(self):
        super().__init__()
        self.setDynamicSortFilter(True)

    def filterAcceptsRow(self, source_row, source_parent):
        if not self._filtered_text:
            return True

        mapped_index = self.sourceModel().index(source_row, 0)
        name = self.sourceModel().data(mapped_index, TableModel.NameRole)
        return re.search(self._filtered_text, name, re.IGNORECASE) is not None

    @pyqtSlot(str)
    def filter(self, text):
        self._filtered_text = text
        self.invalidateFilter()

    def get_url(self, index):
        mapped_index = self.mapToSource(index)
        return self.sourceModel().get_url(mapped_index)
