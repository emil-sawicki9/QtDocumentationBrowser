from PyQt5.QtCore import QSortFilterProxyModel, pyqtSlot
import re

from documentation_model.documentation_model import DocumentationModel


class DocumentationFilterModel(QSortFilterProxyModel):
    _filtered_text = ""
    _filtered_type = 0

    show_only_latest = False
    show_only_pinned = False
    show_only_most_used = False

    def __init__(self):
        super().__init__()
        self.setDynamicSortFilter(True)

    def lessThan(self, left, right):
        if self.show_only_latest:
            left_count = self.sourceModel().data(left, DocumentationModel.LastUsedRole)
            right_count = self.sourceModel().data(right, DocumentationModel.LastUsedRole)
            return left_count > right_count
        if self.show_only_most_used:
            left_count = self.sourceModel().data(left, DocumentationModel.UseCountRole)
            right_count = self.sourceModel().data(right, DocumentationModel.UseCountRole)
            return left_count > right_count
        if self.show_only_pinned:
            left_count = self.sourceModel().data(left, DocumentationModel.PinnedIndexRole)
            right_count = self.sourceModel().data(right, DocumentationModel.PinnedIndexRole)
            return left_count > right_count
        return True

    def filterAcceptsRow(self, source_row, source_parent):
        if self.show_only_latest:
            mapped_index = self.sourceModel().index(source_row, 0)
            return self.sourceModel().data(mapped_index, DocumentationModel.LastUsedRole) is not None
        if self.show_only_most_used:
            mapped_index = self.sourceModel().index(source_row, 0)
            return self.sourceModel().data(mapped_index, DocumentationModel.UseCountRole) > 0
        if self.show_only_pinned:
            mapped_index = self.sourceModel().index(source_row, 0)
            return self.sourceModel().data(mapped_index, DocumentationModel.IsPinnedRole)

        if not self._filtered_text and self._filtered_type == 0:
            return True
        result = True
        mapped_index = self.sourceModel().index(source_row, 0)
        if len(self._filtered_text) > 0:
            name = self.sourceModel().data(mapped_index, DocumentationModel.NameRole)
            result &= re.search(self._filtered_text, name, re.IGNORECASE) is not None
        if self._filtered_type > 0:
            types = {1: "Qt class", 2: "QML type"}
            description = self.sourceModel().data(mapped_index, DocumentationModel.DescriptionRole)
            result &= types[self._filtered_type] == description
        return result

    @pyqtSlot(str)
    def filter(self, text):
        self._filtered_text = text
        self.invalidateFilter()

    @pyqtSlot(int)
    def filter_by_type(self, item_type):
        self._filtered_type = item_type
        self.invalidateFilter()

    def get_url(self, index):
        mapped_index = self.mapToSource(index)
        return self.sourceModel().get_url(mapped_index)
