import sys
from main import main
from Car import Car
import numpy as np
from PySide6.QtCore import Qt
import plotly.graph_objects as go
from functools import partial
from build_plot import build_plot, add_plot_trace

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
    QLabel,
    QComboBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class PlotTab(QWidget):
    def __init__(self, title, data_tab):
        super().__init__()
        self.data_tab = data_tab
        self.graph_counter = 0
        self.colors = ['red', 'blue']

        self.chosen_colors = {}

        self.row_layout_list = []

        # integrating web engine
        self.browser = QWebEngineView()
        self.fig = None


        # add widgets
        self.generate_button = QPushButton("Build Plot")
        self.clear_button = QPushButton("Clear Plot")

        
        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.browser)

        self.setLayout(self.layout)

        self.generate_button.clicked.connect(self.generate_plot)
        self.clear_button.clicked.connect(self.clear_plot)

    def generate_plot(self):
        # TODO: need to pass colors through to main to get them into build_plot

        # new layout for this row
        row_layout = QHBoxLayout()


        # add a color (TODO: and show) widget for every active graph
        current_graph_num = self.graph_counter
        graph_label = QLabel("Graph {}".format(current_graph_num))
        lines1_dropdown = QComboBox()
        lines1_dropdown.addItems(self.colors)
        lines1_dropdown.setCurrentIndex(0)
        
        lines2_dropdown = QComboBox()
        lines2_dropdown.addItems(self.colors)
        lines2_dropdown.setCurrentIndex(1)

        row_layout.addWidget(graph_label)
        row_layout.addWidget(lines1_dropdown)
        row_layout.addWidget(lines2_dropdown)

        lines1_dropdown.currentTextChanged.connect(partial(self.color_change, source_grpah=current_graph_num, subgraph=1))

        lines2_dropdown.currentTextChanged.connect(partial(self.color_change, source_graph=current_graph_num, subgraph=2))

        self.layout.addLayout(row_layout)

        self.row_layout_list.append(row_layout)


        self.graph_df = main(self.data_tab.vehicle_params, self.data_tab.vehicle_params['velocity'])
        if self.graph_counter == 0:
            self.fig = build_plot(self.graph_df, self.data_tab.vehicle_params['velocity'])
            html = self.fig.to_html(include_plotlyjs="cdn", full_html=False)
            self.browser.setHtml(html)
            self.graph_counter += 1
        else:
            # TODO: add traces to the fig that already exists
            updated_fig = add_plot_trace(self.fig, self.graph_df, self.data_tab.vehicle_params['velocity'])
            self.fig = updated_fig
            html = self.fig.to_html(include_plotlyjs="cdn", full_html=False)
            self.browser.setHtml(html)
            self.graph_counter += 1
             

    def clear_plot(self):
        empty_fig = go.Figure()
        self.browser.setHtml(empty_fig.to_html(include_plotlyjs="cdn"))
        self.graph_counter = 0

        for row_layout in self.row_layout_list:
            while row_layout.count():
                item = row_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        
    def color_change(self, source_graph, subgraph):
        # TODO: yikes
        pass

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

        new_row_layout = QHBoxLayout()

        velocityLabel = QLabel("velocity")
        velocityEdit = QLineEdit()
        window_width = self.window().width()
        velocityEdit.setMaximumWidth(250)
        velocityEdit.setAlignment(Qt.AlignRight)

        new_row_layout.addWidget(velocityLabel)
        new_row_layout.addWidget(velocityEdit)
        self.form_layout.addLayout(new_row_layout)
        self.inputs['velocity'] = velocityEdit
        velocityEdit.textChanged.connect(lambda text, k = 'velocity': self.update_car_param('velocity', text))

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
