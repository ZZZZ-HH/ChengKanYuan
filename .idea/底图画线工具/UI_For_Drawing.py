import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QScrollArea, QMessageBox,
                             QLabel, QLineEdit, QFileDialog, QGroupBox, QGridLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import shutil

import Process_Excel_Points as pep
import Basic_Tool as bt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("底图画线工具")
        #self.setGeometry(100, 100, 1600, 900)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        file_group = QGroupBox("文件选择")
        file_layout = QGridLayout()

        self.excel_path = ""
        self.pdf_path = ""
        self.current_output_path = ""

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

        point_group = QGroupBox("标注指定点")
        point_layout = QGridLayout()

        self.point_x_edit = QLineEdit()
        self.point_y_edit = QLineEdit()

        point_layout.addWidget(QLabel("X坐标:"), 0, 0)
        point_layout.addWidget(self.point_x_edit, 0, 1)
        point_layout.addWidget(QLabel("Y坐标:"), 0, 2)
        point_layout.addWidget(self.point_y_edit, 0, 3)

        point_group.setLayout(point_layout)

        execute_btn = QPushButton("运行画线工具")
        execute_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 40px;")
        execute_btn.clicked.connect(self.execute_mapping)

        mark_point_btn = QPushButton("标注点")
        mark_point_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; height: 40px;")
        mark_point_btn.clicked.connect(self.mark_point)

        self.statusBar().showMessage("准备就绪，等待输入中")

        # 结果图
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 400)
        self.image_label.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.image_label.setText("结果将显示在这里")
        self.scroll_area.setWidget(self.image_label)

        self.save_btn = QPushButton("另存为")
        self.save_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; height: 40px;")
        self.save_btn.setEnabled(False) # 初始禁用
        self.save_btn.clicked.connect(self.save_image_as)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(execute_btn)
        btn_layout.addWidget(mark_point_btn)
        btn_layout.addWidget(self.save_btn)

        main_layout.addWidget(file_group)
        main_layout.addWidget(coord_group)
        main_layout.addWidget(point_group)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.scroll_area, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def select_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel文件 (*.xlsx *.xls)"
        )
        if file_path:
            self.excel_path = file_path
            self.excel_label.setText(os.path.basename(file_path))
            self.statusBar().showMessage(f"已选择Excel文件: {os.path.basename(file_path)}")

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择PDF文件", "", "PDF文件 (*.pdf)"
        )
        if file_path:
            self.pdf_path = file_path
            self.pdf_label.setText(os.path.basename(file_path))
            self.statusBar().showMessage(f"已选择PDF文件: {os.path.basename(file_path)}")

    def mark_point(self):
        if not self.pdf_path:
            QMessageBox.critical(self, "错误", "请先选择PDF文件!")
            return

        try:
            x = float(self.point_x_edit.text())
            y = float(self.point_y_edit.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "坐标必须为有效数字!")
            return

        try:
            try:
                x_min = float(self.x_min_edit.text())
                x_max = float(self.x_max_edit.text())
                y_min = float(self.y_min_edit.text())
                y_max = float(self.y_max_edit.text())
            except ValueError:
                QMessageBox.critical(self, "错误", "坐标范围必须为有效数字!")
                return

            output_dir = os.path.dirname(self.pdf_path)
            output_path = os.path.join(output_dir, "点标注结果.png")
            self.current_output_path = output_path

            self.statusBar().showMessage("处理中...")
            QApplication.processEvents()

            result_image = bt.mark_point_on_image(
                pdf_path=self.pdf_path,
                point=(x, y),
                x_range=(x_min, x_max),
                y_range=(y_min, y_max),
                output_path=output_path
            )

            self.statusBar().showMessage(f"点标注完成! 结果已保存至: {os.path.normpath(output_path)}")

            pixmap = QPixmap(output_path)
            scroll_area_size = self.scroll_area.size()
            scaled_pixmap = pixmap.scaled(
                scroll_area_size.width(),
                scroll_area_size.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.resize(scaled_pixmap.size())

            self.save_btn.setEnabled(True)

        except Exception as e:
            self.statusBar().showMessage(f"点标注出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"点标注过程中出错: {str(e)}")

    def execute_mapping(self):
        if not self.excel_path or not self.pdf_path:
            QMessageBox.critical(self, "错误", "请先选择Excel和PDF文件!")
            return

        try:
            x_min = float(self.x_min_edit.text())
            x_max = float(self.x_max_edit.text())
            y_min = float(self.y_min_edit.text())
            y_max = float(self.y_max_edit.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "坐标范围必须为有效数字!")
            return

        if x_min >= x_max or y_min >= y_max:
            QMessageBox.critical(self, "错误", "坐标范围无效（最小值应小于最大值）!")
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

            self.current_output_path = output_path

            self.statusBar().showMessage("处理中...")
            QApplication.processEvents()

            result_image = bt.map_coordinates_to_image(
                pdf_path=self.pdf_path,
                points=points,
                x_range=(x_min, x_max),
                y_range=(y_min, y_max),
                output_path=output_path
            )

            self.statusBar().showMessage(f"处理完成! 结果已保存至: {os.path.normpath(output_path)}")

            # 显示结果图
            pixmap = QPixmap(output_path)
            scroll_area_size = self.scroll_area.size()
            scaled_pixmap = pixmap.scaled(
                scroll_area_size.width(),
                scroll_area_size.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.resize(scaled_pixmap.size())

            self.save_btn.setEnabled(True)

        except Exception as e:
            self.statusBar().showMessage(f"处理出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"处理过程中出错: {str(e)}")

    def save_image_as(self):
        if not self.current_output_path:
            QMessageBox.warning(self, "警告", "没有可保存的图像！")
            return

        source_path = os.path.normpath(self.current_output_path)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存图像", self.current_output_path,
            "PNG图像 (*.png);;JPEG图像 (*.jpg);;所有文件 (*)"
        )

        if file_path:
            try:
                target_path = os.path.normpath(file_path)
                shutil.copy(source_path, target_path)
                self.statusBar().showMessage(f"图像已另存至: {os.path.normpath(target_path)}")
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"无法保存图像: {str(e)}")
                print(f"无法保存图像: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowState(Qt.WindowMaximized)
    window.show()
    sys.exit(app.exec_())