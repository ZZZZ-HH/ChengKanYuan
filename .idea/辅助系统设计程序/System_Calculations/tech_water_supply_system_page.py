from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QFormLayout,
                             QHBoxLayout, QScrollArea, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

class TechWaterSupplySystemPage(QWidget):
    def __init__(self):
        super().__init__()
        self.model_label = None
        self.input_fields = {} # 存储所有输入字段
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
        self.input_fields["1.供水方式"] = self.input1
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
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            section21_layout.addWidget(header_label, 0, col)

        for row in range(1, 5):
            match row:
                case 1:
                    param_label = QLabel(f"空气冷却器Q<sub>kl</sub>")
                case 2:
                    param_label = QLabel(f"推力轴承油冷却器Q<sub>tl</sub>")
                case 3:
                    param_label = QLabel(f"上导轴承油冷却器Q<sub>sd</sub>")
                case 4:
                    param_label = QLabel(f"下导轴承油冷却器Q<sub>xd</sub>")
            param_label.setStyleSheet("font-size: 20px;")
            section21_layout.addWidget(param_label, row, 0)

            formula_input = QLineEdit()
            formula_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
                font-family: 'Times New Roman';
            """)
            section21_layout.addWidget(formula_input, row, 1)
            self.input_fields[f"2.1.{row}.公式"] = formula_input

            calc_input = QLineEdit()
            calc_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
            """)
            section21_layout.addWidget(calc_input, row, 2)
            self.input_fields[f"2.1.{row}.计算值"] = calc_input

            value_input = QLineEdit()
            value_input.setStyleSheet("font-size: 20px; min-height: 35px;")
            section21_layout.addWidget(value_input, row, 3)
            self.input_fields[f"2.1.{row}.取值"] = value_input

            calc_input.setValidator(QDoubleValidator(0, 1e9, 2, self))
            value_input.setValidator(QDoubleValidator(0, 1e9, 2, self))

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
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            section22_layout.addWidget(header_label, 0, col)

        self.section22_inputs = []
        for row in range(1, 3):
            match row:
                case 1:
                    param_label = QLabel(f"水导轴承冷却水Q<sub>sd</sub>")
                case 2:
                    param_label = QLabel(f"主轴密封供水Q<sub>zz</sub>")
            param_label.setStyleSheet("font-size: 20px;")
            section22_layout.addWidget(param_label, row, 0)

            formula_input = QLineEdit()
            formula_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
                font-family: 'Times New Roman';
            """)
            section22_layout.addWidget(formula_input, row, 1)
            self.input_fields[f"2.2.{row}.公式"] = formula_input

            calc_input = QLineEdit()
            calc_input.setStyleSheet("""
                font-size: 20px; 
                min-height: 35px;
            """)
            section22_layout.addWidget(calc_input, row, 2)
            self.input_fields[f"2.2.{row}.计算值"] = calc_input

            value_input = QLineEdit()
            value_input.setStyleSheet("font-size: 20px; min-height: 35px;")
            section22_layout.addWidget(value_input, row, 3)
            self.input_fields[f"2.2.{row}.取值"] = value_input

            calc_input.setValidator(QDoubleValidator(0, 1e9, 2, self))
            value_input.setValidator(QDoubleValidator(0, 1e9, 2, self))

        section22_group.setLayout(section22_layout)
        param_layout.addWidget(section22_group)

        section23_group = QGroupBox("2.3 机组总用水量")
        section23_group.setStyleSheet("""
            QGroupBox {
                font-size: 24px;
                font-weight: bold;
                border: 1px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 25px;
            }
        """)
        section23_layout = QGridLayout()
        section23_layout.setHorizontalSpacing(15)
        section23_layout.setVerticalSpacing(15)

        # 表头
        headers23 = ["", "计算值", "设计值"]
        for col, header in enumerate(headers23):
            header_label = QLabel(header)
            header_label.setStyleSheet("font-size: 22px; font-weight: bold;")
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            section23_layout.addWidget(header_label, 0, col)

        calc_layout = QHBoxLayout()
        self.total_calc_input = QLineEdit()
        self.total_calc_input.setReadOnly(True)
        self.total_calc_input.setStyleSheet("""
            font-size: 20px; 
            min-height: 35px;
        """)
        calc_layout.addWidget(self.total_calc_input)
        calc_unit = QLabel("m³/h")
        calc_unit.setStyleSheet("font-size: 20px; min-height: 35px; padding-top: 5px;")
        calc_layout.addWidget(calc_unit)
        section23_layout.addLayout(calc_layout, 1, 1)
        self.input_fields["2.3.计算值"] = self.total_calc_input

        value_layout = QHBoxLayout()
        self.total_value_input = QLineEdit()
        self.total_value_input.setReadOnly(True)
        self.total_value_input.setStyleSheet("""
            font-size: 20px; 
            min-height: 35px;
        """)
        value_layout.addWidget(self.total_value_input)
        value_unit = QLabel("m³/h")
        value_unit.setStyleSheet("font-size: 20px; min-height: 35px; padding-top: 5px;")
        value_layout.addWidget(value_unit)
        section23_layout.addLayout(value_layout, 1, 2)
        self.input_fields["2.3.设计值"] = self.total_value_input

        section23_group.setLayout(section23_layout)
        param_layout.addWidget(section23_group)

        param_group.setLayout(param_layout)
        content_layout.addWidget(param_group)

        content_layout.addStretch(1)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)

        self.setLayout(main_layout)

        self.connect_signals()

    def set_model_name(self, model_name):
        if self.model_label:
            self.model_label.setText(f"机组类型：{model_name}")

    def connect_signals(self):
        # 2.1的4个计算值和4个取值
        for i in range(1, 5):
            self.input_fields[f"2.1.{i}.计算值"].textChanged.connect(self.update_total_water_usage)
            self.input_fields[f"2.1.{i}.取值"].textChanged.connect(self.update_total_water_usage)

        # 2.2的2个计算值和2个取值
        for i in range(1, 3):
            self.input_fields[f"2.2.{i}.计算值"].textChanged.connect(self.update_total_water_usage)
            self.input_fields[f"2.2.{i}.取值"].textChanged.connect(self.update_total_water_usage)

    def update_total_water_usage(self):
        total_calc = 0.0
        total_value = 0.0

        # 2.1
        for i in range(1, 5):
            calc = float(self.input_fields[f"2.1.{i}.计算值"].text() or 0)
            total_calc += calc

            value = float(self.input_fields[f"2.1.{i}.取值"].text() or 0)
            total_value += value

        # 2.2
        for i in range(1, 3):
            calc = float(self.input_fields[f"2.2.{i}.计算值"].text() or 0)
            total_calc += calc

            value = float(self.input_fields[f"2.2.{i}.取值"].text() or 0)
            total_value += value

        self.total_calc_input.setText(f"{total_calc:.2f}")
        self.total_value_input.setText(f"{total_value:.2f}")