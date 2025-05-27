from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QFileDialog, QHeaderView, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtCore import QTimer
import csv
from data_fetcher import DataFetcher
from database import DatabaseManager
from alert import trigger_alert

class OddsDropMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pinnacle Odds Drop Monitor")
        self.setGeometry(100, 100, 1000, 600)
        self.db = DatabaseManager()
        self.setup_ui()
        self.data_fetcher = DataFetcher(self)
        self.start_auto_refresh()

    def setup_ui(self):
        layout = QVBoxLayout()
        controls = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh Now")
        self.refresh_btn.clicked.connect(self.fetch_data)
        self.threshold_input = QDoubleSpinBox()
        self.threshold_input.setRange(0, 100)
        self.threshold_input.setValue(10.0)
        self.threshold_input.setSuffix(" %")
        controls.addWidget(QLabel("Min % Drop:"))
        controls.addWidget(self.threshold_input)
        controls.addWidget(self.refresh_btn)
        self.export_btn = QPushButton("Export to CSV")
        self.export_btn.clicked.connect(self.export_to_csv)
        controls.addWidget(self.export_btn)
        layout.addLayout(controls)
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["League", "Outcome", "Market", "Old", "New", "% Drop", "Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def start_auto_refresh(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_data)
        self.timer.start(30000)

    def fetch_data(self):
        self.data_fetcher.fetch_data()

    def update_table(self, rows):
        self.table.setRowCount(0)
        for row_data in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "odds_drops.csv", "CSV Files (*.csv)")
        if path:
            with open(path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Match", "Outcome", "Market", "Old", "New", "% Drop", "Time"])
                for row in range(self.table.rowCount()):
                    writer.writerow([
                        self.table.item(row, col).text() for col in range(self.table.columnCount())
                    ])