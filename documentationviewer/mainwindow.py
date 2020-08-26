from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableView, QWidget, QHeaderView, QLineEdit
from documentationviewer.table_model import TableModel
from documentationviewer.table_proxy_model import TableProxyModel
import webbrowser
import warnings


class MainWindow(QMainWindow):
    model = TableModel()
    proxy_model = TableProxyModel()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Documentation viewer"))
        self.setMinimumSize(600, 400)
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Filter edit
        filter_field = QLineEdit()
        layout.addWidget(filter_field)

        # Proxy model
        self.proxy_model.setSourceModel(self.model)
        filter_field.textChanged.connect(self.proxy_model.filter_by_text)

        # Setting table view
        table = QTableView()
        table.verticalHeader().hide()
        table.horizontalHeader().show()
        table.setModel(self.proxy_model)
        for i in range(table.horizontalHeader().count()):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        layout.addWidget(table)
        table.clicked.connect(self.cell_clicked)

    def cell_clicked(self, index):
        url = self.proxy_model.get_url(index)
        if url:
            webbrowser.open(url)
        else:
            warnings.warn("Url is empty")
