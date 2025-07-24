from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QFormLayout,
                             QHBoxLayout, QScrollArea, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt

class TechWaterSupplySystemPage(QWidget):
    def __init__(self):
        super().__init__()
        self.model_label = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        top_layout = QHBoxLayout()

        top_layout.addStretch(2)

        title = QLabel("技术供水系统计算", self)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")
        top_layout.addWidget(title)

        top_layout.addStretch(1)

        self.model_label = QLabel("机组类型：未选择", self)
        self.model_label.setStyleSheet("font-size: 32px; color: #3498db; font-weight: bold; padding: 10px;")
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self.model_label)

        main_layout.addLayout(top_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        water_supply_group = QGroupBox("1. 供水方式")
        water_supply_group.setStyleSheet("""
            QGroupBox {
                font-size: 28px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 20px;
                padding-top: 30px;
            }
        """)
        water_supply_layout = QFormLayout()
        water_supply_layout.setSpacing(20)

        label1 = QLabel("供水方式：", self)
        label1.setStyleSheet("font-size: 24px;")
        self.input1 = QLineEdit(self)
        self.input1.setStyleSheet("font-size: 24px; min-height: 40px;")
        water_supply_layout.addRow(label1, self.input1)

        water_supply_group.setLayout(water_supply_layout)
        content_layout.addWidget(water_supply_group)

        param_group = QGroupBox("2. 水轮发电机组供水系统")
        param_group.setStyleSheet("""
            QGroupBox {
                font-size: 28px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 20px;
                padding-top: 30px;
            }
        """)
        param_layout = QVBoxLayout()
        param_layout.setSpacing(20)

        section21_group = QGroupBox("2.1 水轮发电机用水量计算")
        section21_group.setStyleSheet("""
            QGroupBox {
                font-size: 24px;
                font-weight: bold;
                border: 1px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 25px;
            }
        """)
        section21_layout = QGridLayout()
        section21_layout.setHorizontalSpacing(15)
        section21_layout.setVerticalSpacing(15)

        # 表头
        headers = ["", "公式", "计算值", "取值"]
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setStyleSheet("font-size: 22px; font-weight: bold;")
            section21_layout.addWidget(header_label, 0, col)

        self.section21_inputs = []
        for row in range(1, 5):
            param_label = QLabel(f"参数{row}") # TODO 改成对应项目名
            param_label.setStyleSheet("font-size: 20px;")
            section21_layout.addWidget(param_label, row, 0)

            formula_input = QLineEdit()
            formula_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
                font-family: 'Times New Roman';
                background-color: #f9f9f9;
            """)
            section21_layout.addWidget(formula_input, row, 1)
            self.section21_inputs.append(formula_input)

            calc_input = QLineEdit()
            calc_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
                background-color: #f9f9f9;
            """)
            section21_layout.addWidget(calc_input, row, 2)
            self.section21_inputs.append(calc_input)

            value_input = QLineEdit()
            value_input.setStyleSheet("font-size: 20px; min-height: 35px;")
            section21_layout.addWidget(value_input, row, 3)
            self.section21_inputs.append(value_input)

        section21_group.setLayout(section21_layout)
        param_layout.addWidget(section21_group)

        section22_group = QGroupBox("2.2 水轮机用水量计算")
        section22_group.setStyleSheet("""
            QGroupBox {
                font-size: 24px;
                font-weight: bold;
                border: 1px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 25px;
            }
        """)
        section22_layout = QGridLayout()
        section22_layout.setHorizontalSpacing(15)
        section22_layout.setVerticalSpacing(15)

        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setStyleSheet("font-size: 22px; font-weight: bold;")
            section22_layout.addWidget(header_label, 0, col)

        self.section22_inputs = []
        for row in range(1, 3):
            param_label = QLabel(f"参数{row}") # TODO 改成对应项目名
            param_label.setStyleSheet("font-size: 20px;")
            section22_layout.addWidget(param_label, row, 0)

            formula_input = QLineEdit()
            formula_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
                font-family: 'Times New Roman';
                background-color: #f9f9f9;
            """)
            section22_layout.addWidget(formula_input, row, 1)
            self.section22_inputs.append(formula_input)

            calc_input = QLineEdit()
            calc_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
                background-color: #f9f9f9;
            """)
            section22_layout.addWidget(calc_input, row, 2)
            self.section22_inputs.append(calc_input)

            value_input = QLineEdit()
            value_input.setStyleSheet("font-size: 20px; min-height: 35px;")
            section22_layout.addWidget(value_input, row, 3)
            self.section22_inputs.append(value_input)

        section22_group.setLayout(section22_layout)
        param_layout.addWidget(section22_group)

        param_group.setLayout(param_layout)
        content_layout.addWidget(param_group)

        content_layout.addStretch(1)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)

        self.setLayout(main_layout)

    def set_model_name(self, model_name):
        if self.model_label:
            self.model_label.setText(f"机组类型：{model_name}")