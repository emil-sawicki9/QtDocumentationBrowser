from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableView, QWidget, QHeaderView
from documentationviewer.table_model import TableModel


class MainWindow(QMainWindow):
    model = TableModel()

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

        # Setting table view
        table = QTableView()
        table.verticalHeader().hide()
        table.horizontalHeader().show()
        table.setModel(self.model)
        for i in range(table.horizontalHeader().count()):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        layout.addWidget(table)
