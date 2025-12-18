import sys
from main import main
from Car import Car
import numpy as np
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QFileDialog,
    QLabel
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class PlotTab(QWidget):
    def __init__(self, title, data_tab):
        super().__init__()
        self.data_tab = data_tab

        # integrating web engine
        self.browser = QWebEngineView()

        # add widgets
        self.generate_button = QPushButton("Build Plot")
        
        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.generate_button)
        layout.addWidget(self.browser)

        self.setLayout(layout)

        self.generate_button.clicked.connect(self.generate_plot)

    def generate_plot(self):
        html = main(self.data_tab.vehicle_params)

        self.browser.setHtml(html)

class dataTab(QWidget):
    def __init__(self, title):
        super().__init__()

        self.vehicle = None
        self.vehicle_params = None
        self.inputs = {}
        
        self.add_data_button = QPushButton("Add data")
        self.add_data_button.clicked.connect(self.open_file)

        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.add_data_button)
        self.setLayout(self.form_layout)


    def open_file(self):
        global vehicle
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Data File",
            "",
            "Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        # build a car
        self.vehicle = Car(file_path)
        self.vehicle.load_data()
        self.vehicle_params = self.vehicle.car_params

        self.populate_form()

    def clear_layout(self, layout):
        print("in clear layout")
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
                
    def populate_form(self):
        # clear old widgets
        self.clear_layout(self.form_layout)
        self.inputs.clear()

        for key, value in self.vehicle_params.items():
            row_layout = QHBoxLayout()

            label = QLabel(key)
            edit = QLineEdit(str(value))
            window_width = self.window().width()
            edit.setMaximumWidth(int(window_width*0.25))
            edit.setAlignment(Qt.AlignRight)

            row_layout.addWidget(label)
            row_layout.addWidget(edit)
            self.form_layout.addLayout(row_layout)


            self.inputs[key] = edit
            
            edit.textChanged.connect(lambda text, k=key: self.update_car_param(k, text))

    def update_car_param(self, key, value):
        try:
            self.vehicle_params[key] = float(value)
        except ValueError:
            self.vehicle_params[key] = value

    def get_updated_params(self):
        return {
                key: float(edit.text())
                for key, edit in self.inputs.items()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yaw Moment Diagram Simulator")
        self.resize(1000, 700)

        self.tabs = QTabWidget()

        # create tabs
        self.dataTab = dataTab("Data Import")
        self.plotTab = PlotTab("Plot", self.dataTab)
        self.tabs.addTab(self.dataTab, "Data Import")
        self.tabs.addTab(self.plotTab, "Plot")

        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
