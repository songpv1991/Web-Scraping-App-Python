# File: main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from data_fetcher import DataFetcher
from database import DatabaseManager
from exporter import export_to_csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📉 Pinnacle Odds Drop Monitor")
        self.resize(1000, 600)
        self.db = DatabaseManager()

        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14px;
            }
            QMainWindow {
                background-color: #f5f7fa;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #007acc;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005b9f;
            }
            QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #ccc;
            }
        """)

        title = QLabel("Live Odds Drop Monitor")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "League", "Team", "OutCome", "Old", "New", "Drop", "Time"
        ])
        self.table.setWordWrap(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        self.refresh_btn = QPushButton("🔄 Refresh Now")
        self.refresh_btn.clicked.connect(self.fetch_data_now)

        self.export_btn = QPushButton("📁 Export to CSV")
        self.export_btn.clicked.connect(self.export_data)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.data_fetcher = DataFetcher()
        self.data_fetcher.data_fetched.connect(self.update_table)
        self.data_fetcher.message_alert.connect(self.update_table)
        self.data_fetcher.start()


    def alert(self,data):
        QMessageBox.warning(
            self,
            "📢 Alert","dafasfasfasfasf"
        )


    def fetch_data_now(self):
        self.data_fetcher.fetch_once()

    def update_table(self, data):
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        print(data)
        for col_index, item in enumerate(data):
            cell = QTableWidgetItem(str(item))
            # cell.setBackground(QColor('#dfffe0') if float(row[5].replace('%', '')) >= 15 else QColor('#ffffff'))
            self.table.setItem(row_index, col_index, cell)

        # for row in data:
        #     # self.db.insert_data(row)
           
        #     row_index = self.table.rowCount()
        #     row_list = row.toArray()
        #     for row_data in row_list:
        #         self.table.insertRow(row_index)
        #         print(row_data)
        #         for col_index, item in enumerate(row_data):
        #             cell = QTableWidgetItem(str(item))
        #             # cell.setBackground(QColor('#dfffe0') if float(row[5].replace('%', '')) >= 15 else QColor('#ffffff'))
        #             self.table.setItem(row_index, col_index, cell)
        #     self.table.resizeRowsToContents()
            # drop = float(row[5].replace('%', ''))
            # if drop >= 15:
            #     QMessageBox.warning(
            #         self,
            #         "📢 Alert",
            #         f"Significant drop detected:\nMatch: {row[0]}\nOutcome: {row[1]}\nDrop: {row[5]}"
            #     )

    def export_data(self):
        rows = []
        for i in range(self.table.rowCount()):
            row = []
            for j in range(self.table.columnCount()):
                row.append(self.table.item(i, j).text())
            rows.append(row)
        export_to_csv(rows)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())