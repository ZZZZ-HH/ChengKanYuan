from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QFormLayout, QPushButton,
                             QHBoxLayout, QScrollArea, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDoubleValidator, QDesktopServices

class TechWaterSupplySystemPage(QWidget):
    def __init__(self, backend_manager):
        super().__init__()
        self.backend = backend_manager
        self.model_label = None
        self.input_fields = {} # 存储所有输入字段
        self.group_style = """
            QGroupBox {
                font-size: 28px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 20px;
                padding-top: 30px;
            }
        """
        self.subgroup_style = """
            QGroupBox {
                font-size: 24px;
                font-weight: bold;
                border: 1px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 25px;
            }
        """
        self.initUI()

        self.backend.model_changed.connect(self.update_model_label)
        self.backend.calculation_result_ready.connect(self.update_calculation_results)

        self.update_model_label(self.backend.get_model())

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

        """
        1. 供水方式
        """
        water_supply_group = QGroupBox("1. 供水方式")
        water_supply_group.setStyleSheet(self.group_style)
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

        """
        2. 水轮发电机组供水系统
        """
        param_group = QGroupBox("2. 水轮发电机组供水系统")
        param_group.setStyleSheet(self.group_style)
        param_layout = QVBoxLayout()
        param_layout.setSpacing(20)

        """
        2.1 水轮发电机用水量计算
        """
        section21_group = QGroupBox("2.1 水轮发电机用水量计算")
        section21_group.setStyleSheet(self.subgroup_style)
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

        """
        2.2 水轮机用水量计算
        """
        section22_group = QGroupBox("2.2 水轮机用水量计算")
        section22_group.setStyleSheet(self.subgroup_style)
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

        """
        2.3 机组总用水量
        """
        section23_group = QGroupBox("2.3 机组总用水量")
        section23_group.setStyleSheet(self.subgroup_style)
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

        """
        2.4 水轮发电机组用水量参考
        """
        section24_group = QGroupBox("2.4 水轮发电机组用水量参考")
        section24_group.setStyleSheet(self.subgroup_style)
        section24_layout = QVBoxLayout()

        self.pdf_button = QPushButton("查看已建电站技术用水量参考文档")
        self.pdf_button.setStyleSheet("""
            QPushButton {
                font-size: 22px;
                font-weight: bold;
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.pdf_button.setFixedHeight(50)
        self.pdf_button.clicked.connect(lambda: self.open_pdf_document(r"C:\Users\13438\Desktop\辅助计算\方案构思策划.pdf")) # TODO 修改实际文档路径

        section24_layout.addWidget(self.pdf_button, 0, Qt.AlignmentFlag.AlignCenter)
        section24_layout.addStretch(1)
        section24_group.setLayout(section24_layout)
        param_layout.addWidget(section24_group)

        """
        2.5 机组技术供水系统用水量设计值
        """
        section25_group = QGroupBox("2.5 机组技术供水系统用水量设计值")
        section25_group.setStyleSheet(self.subgroup_style)
        section25_layout = QVBoxLayout()
        section25_layout.setSpacing(15)

        parameters = [
            ("空气冷却器Q<sub>kl</sub>", "m³/h"),
            ("推力轴承油冷却器Q<sub>tl</sub>", "m³/h"),
            ("上导轴承油冷却器Q<sub>sd</sub>", "m³/h"),
            ("下导轴承油冷却器Q<sub>xd</sub>", "m³/h"),
            ("水导轴承冷却水Q<sub>sd</sub>", "m³/h"),
            ("主轴密封供水Q<sub>zz</sub>", "m³/h"),
            ("机组总用水量", "m³/h")
        ]

        for i, (param_name, unit) in enumerate(parameters):
            row_layout = QHBoxLayout()

            if i == 6:
                row_layout.addStretch(2)
                label = QLabel(f"{param_name}：")
                label.setStyleSheet("font-size: 24px; min-width: 150px; font-weight: bold;")
            else:
                row_layout.addStretch(1)
                label = QLabel(f"({i+1}){param_name}：")
                label.setStyleSheet("font-size: 20px; min-width: 200px;")

            row_layout.addWidget(label)

            if i == 6:
                self.total_design_usage_input = QLineEdit()
                self.total_design_usage_input.setReadOnly(True)
                self.total_design_usage_input.setStyleSheet("font-size: 20px; min-height: 35px; min-width: 250px;")
                row_layout.addWidget(self.total_design_usage_input)
            else:
                input_field = QLineEdit()
                input_field.setStyleSheet("font-size: 20px; min-height: 35px; min-width: 250px;")
                row_layout.addWidget(input_field)

            unit_label = QLabel(unit)
            unit_label.setStyleSheet("font-size: 20px; min-height: 35px; padding-top: 5px; min-width: 70px;")
            row_layout.addWidget(unit_label)

            row_layout.addStretch(1)

            section25_layout.addLayout(row_layout)

            self.input_fields[f"2.5.{i+1}"] = input_field

        section25_group.setLayout(section25_layout)
        param_layout.addWidget(section25_group)

        """
        2.6 供水管设计
        """
        section26_group = QGroupBox("2.6 供水管设计")
        section26_group.setStyleSheet(self.subgroup_style)
        section26_layout = QVBoxLayout()
        section26_layout.setSpacing(15)

        param_vj_group = QGroupBox()
        param_vj_layout = QHBoxLayout()

        param_vj_label = QLabel("流速V<sub>j</sub>取：")
        param_vj_label.setStyleSheet("font-size: 22px; min-width: 200px;")
        param_vj_layout.addWidget(param_vj_label)

        self.flow_speed_min = QLineEdit()
        self.flow_speed_min.setStyleSheet("font-size: 20px; min-height: 35px; min-width: 100px;")
        param_vj_layout.addWidget(self.flow_speed_min)

        tilde_label = QLabel("~")
        tilde_label.setStyleSheet("font-size: 20px; padding: 0 10px;")
        param_vj_layout.addWidget(tilde_label)

        self.flow_speed_max = QLineEdit()
        self.flow_speed_max.setStyleSheet("font-size: 20px; min-height: 35px; min-width: 100px;")
        param_vj_layout.addWidget(self.flow_speed_max)

        unit_label = QLabel("m/s")
        unit_label.setStyleSheet("font-size: 20px; padding-left: 10px;")
        param_vj_layout.addWidget(unit_label)

        param_vj_layout.addStretch(1)
        param_vj_group.setLayout(param_vj_layout)
        section26_layout.addWidget(param_vj_group)

        self.input_fields["2.6.流速Vj.最小值"] = self.flow_speed_min
        self.input_fields["2.6.流速Vj.最大值"] = self.flow_speed_max

        """
        2.6.1 - 2.6.4
        """
        subsection_titles = [
            ("2.6.1 总管", "材料\n选择"),
            ("2.6.2 上导轴承油冷却器供水管", "材料\n选择"),
            ("2.6.3 推力轴承油冷却器供水管", "材料\n选择"),
            ("2.6.4 下导轴承油冷却器供水管", "材料\n选择")
        ]

        # TODO 修改实际文档路径
        pdf_paths = [
            r"C:\.pdf",
            r"C:\.pdf",
            r"C:\.pdf",
            r"C:\.pdf"
        ]

        param_names = [
            ["计算管径d", "设计管型", "管内流速V"],
            ["计算管径d", "设计管型", "管内流速V"],
            ["计算管径d", "设计管型", "管内流速V"],
            ["计算管径d", "设计管型", "管内流速V"]
        ]

        for i, (title, button_text) in enumerate(subsection_titles):
            subsection_group = QGroupBox(title)
            subsection_group.setStyleSheet(self.subgroup_style)

            subsection_layout = QHBoxLayout()

            params_layout = QVBoxLayout()
            params_layout.setSpacing(15)

            for j in range(3):
                row_layout = QHBoxLayout()

                if j == 1:
                    param_label = QLabel(param_names[i][j] + "：𝜙")
                else:
                    param_label = QLabel(param_names[i][j] + "：")
                param_label.setStyleSheet("font-size: 20px; min-width: 150px;")
                row_layout.addWidget(param_label)

                if j < 2:
                    min_input = QLineEdit()
                    min_input.setStyleSheet("font-size: 20px; min-height: 35px; min-width: 80px;")
                    row_layout.addWidget(min_input)

                    if j == 0:
                        tilde_label = QLabel("~")
                    else:
                        tilde_label = QLabel("×")
                    tilde_label.setStyleSheet("font-size: 20px; padding: 0 5px;")
                    row_layout.addWidget(tilde_label)

                    max_input = QLineEdit()
                    max_input.setStyleSheet("font-size: 20px; min-height: 35px; min-width: 80px;")
                    row_layout.addWidget(max_input)

                    if j == 0:
                        unit_label = QLabel("m")
                        unit_label.setStyleSheet("font-size: 20px; padding-left: 5px;")
                        row_layout.addWidget(unit_label)

                    self.input_fields[f"{title}.{param_names[i][j]}.最小值"] = min_input
                    self.input_fields[f"{title}.{param_names[i][j]}.最大值"] = max_input
                else:
                    value_input = QLineEdit()
                    value_input.setStyleSheet("font-size: 20px; min-height: 35px; min-width: 180px;")
                    row_layout.addWidget(value_input)

                    unit_label = QLabel("m/s")
                    unit_label.setStyleSheet("font-size: 20px; padding-left: 5px;")
                    row_layout.addWidget(unit_label)

                    self.input_fields[f"{title}.{param_names[i][j]}"] = value_input

                row_layout.addStretch(1)
                params_layout.addLayout(row_layout)

            subsection_layout.addLayout(params_layout)

            button_layout = QVBoxLayout()
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            pdf_button = QPushButton(button_text)
            pdf_button.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    font-weight: bold;
                    background-color: #3498db;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 5px;
                    min-width: 150px;
                    min-height: 60px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            pdf_button.setFixedSize(150, 80)

            pdf_button.setText(button_text)
            pdf_button.clicked.connect(lambda checked, path=pdf_paths[i]: self.open_pdf_document(path))

            button_layout.addWidget(pdf_button)
            subsection_layout.addLayout(button_layout)

            subsection_group.setLayout(subsection_layout)
            section26_layout.addWidget(subsection_group)

        section26_group.setLayout(section26_layout)
        param_layout.addWidget(section26_group)



        param_group.setLayout(param_layout)
        content_layout.addWidget(param_group)

        content_layout.addStretch(1)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)

        self.setLayout(main_layout)

        for key, input_field in self.input_fields.items():
            input_field.textChanged.connect(lambda text, k=key: self.on_param_changed(k, text))

    def set_model_name(self, model_name):
        if self.model_label:
            self.model_label.setText(f"机组类型：{model_name}")

    def open_pdf_document(self, path):
        url = QUrl.fromLocalFile(path)
        QDesktopServices.openUrl(url)

    def update_model_label(self, model_name):
        if self.model_label:
            self.model_label.setText(f"机组类型：{model_name}")

    def update_calculation_results(self, results):
        # 2.3 总用水量
        self.total_calc_input.setText(f"{results.get('2.3.计算值', 0):.2f}")
        self.total_value_input.setText(f"{results.get('2.3.设计值', 0):.2f}")

        # TODO 2.5只是确认设计值，有问题返回2.1和2.2修改，没问题往下
        # 2.5 设计用水量
        design_values = results.get("2.5.设计值", [])
        for i in range(1, 7):
            if i-1 < len(design_values):
                self.input_fields[f"2.5.{i}"].setText(f"{design_values[i-1]:.2f}")
        self.total_design_usage_input.setText(f"{results.get('2.5.总计', 0):.2f}")

    def on_param_changed(self, key, value):
        self.backend.set_tech_water_param(key, value)