import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QFileDialog, QGroupBox, QGridLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

import Process_Excel_Points as pep
import Basic_Tool as bt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("底图画线工具")
        self.setGeometry(300, 300, 1600, 900)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        file_group = QGroupBox("文件选择")
        file_layout = QGridLayout()

        self.excel_path = ""
        self.pdf_path = ""

        self.excel_label = QLabel("未选择Excel文件")
        excel_btn = QPushButton("选择Excel文件")
        excel_btn.clicked.connect(self.select_excel)
        file_layout.addWidget(QLabel("Excel文件:"), 0, 0)
        file_layout.addWidget(self.excel_label, 0, 1)
        file_layout.addWidget(excel_btn, 0, 2)

        self.pdf_label = QLabel("未选择PDF文件")
        pdf_btn = QPushButton("选择PDF文件")
        pdf_btn.clicked.connect(self.select_pdf)
        file_layout.addWidget(QLabel("PDF文件:"), 1, 0)
        file_layout.addWidget(self.pdf_label, 1, 1)
        file_layout.addWidget(pdf_btn, 1, 2)

        file_group.setLayout(file_layout)

        coord_group = QGroupBox("坐标范围设置")
        coord_layout = QGridLayout()

        self.x_min_edit = QLineEdit()
        self.x_max_edit = QLineEdit()
        self.y_min_edit = QLineEdit()
        self.y_max_edit = QLineEdit()

        coord_layout.addWidget(QLabel("横坐标最小值:"), 0, 0)
        coord_layout.addWidget(self.x_min_edit, 0, 1)
        coord_layout.addWidget(QLabel("横坐标最大值:"), 0, 2)
        coord_layout.addWidget(self.x_max_edit, 0, 3)

        coord_layout.addWidget(QLabel("纵坐标最小值:"), 1, 0)
        coord_layout.addWidget(self.y_min_edit, 1, 1)
        coord_layout.addWidget(QLabel("纵坐标最大值:"), 1, 2)
        coord_layout.addWidget(self.y_max_edit, 1, 3)

        coord_group.setLayout(coord_layout)

        execute_btn = QPushButton("运行画线工具")
        execute_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 40px;")
        execute_btn.clicked.connect(self.execute_mapping)

        self.status_label = QLabel("准备就绪，等待输入中")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-weight: bold;")

        # 结果图
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 400)
        self.image_label.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        main_layout.addWidget(file_group)
        main_layout.addWidget(coord_group)
        main_layout.addWidget(execute_btn)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.image_label)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def select_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel文件 (*.xlsx *.xls)"
        )
        if file_path:
            self.excel_path = file_path
            self.excel_label.setText(os.path.basename(file_path))

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择PDF文件", "", "PDF文件 (*.pdf)"
        )
        if file_path:
            self.pdf_path = file_path
            self.pdf_label.setText(os.path.basename(file_path))

    def execute_mapping(self):
        if not self.excel_path or not self.pdf_path:
            self.status_label.setText("错误: 请先选择Excel和PDF文件!")
            return

        try:
            x_min = float(self.x_min_edit.text())
            x_max = float(self.x_max_edit.text())
            y_min = float(self.y_min_edit.text())
            y_max = float(self.y_max_edit.text())
        except ValueError:
            self.status_label.setText("错误: 坐标范围必须为有效数字!")
            return

        if x_min >= x_max or y_min >= y_max:
            self.status_label.setText("错误: 坐标范围无效 (最小值应小于最大值)!")
            return

        # TODO: 是否允许自定义单元格位置？
        custom_points = [
            'A2', 'B2',  # 1
            'A3', 'B3',  # 2
            'A4', 'B4',  # 3
            'A5', 'B5',  # 4
            'A6', 'B6',  # 5
            'A7', 'B7'   # 6
        ]

        try:
            points = pep.read_custom_points(self.excel_path, custom_points)

            output_dir = os.path.dirname(self.pdf_path)
            output_path = os.path.join(output_dir, "底图画线结果.png")

            self.status_label.setText("处理中...")
            QApplication.processEvents()

            result_image = bt.map_coordinates_to_image(
                pdf_path=self.pdf_path,
                points=points,
                x_range=(x_min, x_max),
                y_range=(y_min, y_max),
                output_path=output_path
            )

            self.status_label.setText(f"处理完成! 结果已保存至: 底图画线结果.png")

            # 显示结果图
            pixmap = QPixmap(output_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
            # TODO: 调整显示图的位置和大小

        except Exception as e:
            self.status_label.setText(f"处理出错: {str(e)}")
            #self.status_label.setText(f"处理出错，请重试！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())