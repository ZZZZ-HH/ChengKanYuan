from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QFormLayout, QPushButton,
                             QHBoxLayout, QScrollArea, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDoubleValidator, QDesktopServices

class TechWaterSupplySystemPage(QWidget):
    def __init__(self, backend_manager):
        super().__init__()
        self.backend = backend_manager
        self.model_label = None
        self.input_fields = {}
        self.init_styles()
        self.initUI()
        self.design_confirmed = False

        self.backend.model_changed.connect(self.update_model_label)
        self.backend.calculation_result_ready.connect(self.update_calculation_results)
        self.update_model_label(self.backend.get_model())

    def init_styles(self):
        """样式表"""
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
        self.common_input_style = "font-size: 20px; min-height: 35px; text-align: center;"
        self.input_style = self.common_input_style
        self.header_style = "font-size: 22px; font-weight: bold;"
        self.button_style = """
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
        """
        self.unit_style = "font-size: 20px; min-height: 35px; padding-top: 5px; min-width: 70px;"

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 顶部标题区域
        top_layout = QHBoxLayout()
        top_layout.addStretch(2)

        title = QLabel("技术供水系统计算")
        title.setStyleSheet("font-size: 36px; font-weight: bold;")
        top_layout.addWidget(title)

        top_layout.addStretch(1)

        self.model_label = QLabel("机组类型：未选择")
        self.model_label.setStyleSheet("font-size: 32px; color: #3498db; font-weight: bold; padding: 10px;")
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self.model_label)

        main_layout.addLayout(top_layout)

        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # 1. 供水方式
        content_layout.addWidget(self.create_water_supply_group())

        # 2. 水轮发电机组供水系统
        param_group = QGroupBox("2. 水轮发电机组供水系统")
        param_group.setStyleSheet(self.group_style)
        param_layout = QVBoxLayout(param_group)
        param_layout.setSpacing(20)

        # 2.1 水轮发电机用水量计算
        row_config_21 = [
            {"label": "空气冷却器Q<sub>kl</sub>", "key": "kl"},
            {"label": "推力轴承油冷却器Q<sub>tl</sub>", "key": "tl"},
            {"label": "上导轴承油冷却器Q<sub>sd</sub>", "key": "sd"},
            {"label": "下导轴承油冷却器Q<sub>xd</sub>", "key": "xd"}
        ]
        param_layout.addWidget(self.create_formula_table("2.1", "2.1 水轮发电机用水量计算", row_config_21))

        # 2.2 水轮机用水量计算
        row_config_22 = [
            {"label": "水导轴承冷却水Q<sub>sd</sub>", "key": "sd"},
            {"label": "主轴密封供水Q<sub>zz</sub>", "key": "zz"}
        ]
        param_layout.addWidget(self.create_formula_table("2.2", "2.2 水轮机用水量计算", row_config_22))

        # 2.3 机组总用水量
        param_layout.addWidget(self.create_total_usage_group())

        # 2.4 水轮发电机组用水量参考
        param_layout.addWidget(self.create_reference_group())

        # 2.5 机组技术供水系统用水量设计值
        param_layout.addWidget(self.create_design_usage_group())

        # 2.6 供水管设计
        param_layout.addWidget(self.create_pipe_design_group())

        content_layout.addWidget(param_group)
        content_layout.addStretch(1)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)

        for key, input_field in self.input_fields.items():
            input_field.textChanged.connect(lambda text, k=key: self.on_param_changed(k, text))

    def create_water_supply_group(self):
        """1. 供水方式"""
        group = QGroupBox("1. 供水方式")
        group.setStyleSheet(self.group_style)
        layout = QFormLayout(group)
        layout.setSpacing(20)

        label = QLabel("供水方式：")
        label.setStyleSheet("font-size: 24px;")
        input_field = QLineEdit()
        input_field.setStyleSheet("font-size: 24px; min-height: 40px; text-align: center;")
        layout.addRow(label, input_field)

        self.input_fields["1.供水方式"] = input_field
        return group

    def create_formula_table(self, section_key, title, rows):
        """公式化创建表格"""
        group = QGroupBox(title)
        group.setStyleSheet(self.subgroup_style)
        grid = QGridLayout(group)
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)

        # 表头
        headers = ["", "A厂", "B厂", "C厂", "设计值"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet(self.header_style)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(label, 0, col)

        # 数据行
        for row, config in enumerate(rows, 1):
            param_label = QLabel(config["label"])
            param_label.setStyleSheet("font-size: 20px;")
            grid.addWidget(param_label, row, 0)

            for col, factory in enumerate(["A", "B", "C"], 1):
                factory_input = QLineEdit()
                factory_input.setStyleSheet(self.input_style)
                factory_input.setValidator(QDoubleValidator(0, 1e9, 2, self))
                grid.addWidget(factory_input, row, col)
                self.input_fields[f"{section_key}.{row}.{factory}厂"] = factory_input

            # 设计值
            value_input = QLineEdit()
            value_input.setStyleSheet(self.input_style)
            value_input.setValidator(QDoubleValidator(0, 1e9, 2, self))
            grid.addWidget(value_input, row, 4)
            self.input_fields[f"{section_key}.{row}.取值"] = value_input

        return group

    def create_total_usage_group(self):
        """总用水量"""
        group = QGroupBox("2.3 机组总用水量")
        group.setStyleSheet(self.subgroup_style)
        grid = QGridLayout(group)
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)

        # 表头
        headers = ["", "计算值", "设计值"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet(self.header_style)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(label, 0, col)

        # 计算值
        calc_layout = QHBoxLayout()
        self.total_calc_input = QLineEdit()
        self.total_calc_input.setReadOnly(True)
        self.total_calc_input.setStyleSheet(self.input_style)
        calc_layout.addWidget(self.total_calc_input)
        unit_label_calc = QLabel("m³/h")
        unit_label_calc.setStyleSheet(self.unit_style)
        calc_layout.addWidget(unit_label_calc)
        grid.addLayout(calc_layout, 1, 1)
        self.input_fields["2.3.计算值"] = self.total_calc_input

        # 设计值
        value_layout = QHBoxLayout()
        self.total_value_input = QLineEdit()
        self.total_value_input.setReadOnly(True)
        self.total_value_input.setStyleSheet(self.input_style)
        value_layout.addWidget(self.total_value_input)
        unit_label_value = QLabel("m³/h")
        unit_label_value.setStyleSheet(self.unit_style)
        value_layout.addWidget(unit_label_value)
        grid.addLayout(value_layout, 1, 2)
        self.input_fields["2.3.设计值"] = self.total_value_input

        return group

    def create_reference_group(self):
        """用水量参考"""
        group = QGroupBox("2.4 水轮发电机组用水量参考")
        group.setStyleSheet(self.subgroup_style)
        layout = QVBoxLayout(group)

        button = QPushButton("查看已建电站技术用水量参考文档")
        button.setStyleSheet(self.button_style)
        button.setFixedHeight(50)
        # TODO: 修改实际文档路径
        button.clicked.connect(lambda: self.open_pdf_document(r"C:\Users\13438\Desktop\辅助计算\方案构思策划.pdf"))
        layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)

        return group

    def create_design_usage_group(self):
        group = QGroupBox("2.5 机组技术供水系统用水量设计值")
        group.setStyleSheet(self.subgroup_style)
        layout = QVBoxLayout(group)
        layout.setSpacing(15)

        parameters = [
            ("空气冷却器Q<sub>kl</sub>", "m³/h", False, "2.1.1.取值"),
            ("推力轴承油冷却器Q<sub>tl</sub>", "m³/h", False, "2.1.2.取值"),
            ("上导轴承油冷却器Q<sub>sd</sub>", "m³/h", False, "2.1.3.取值"),
            ("下导轴承油冷却器Q<sub>xd</sub>", "m³/h", False, "2.1.4.取值"),
            ("水导轴承冷却水Q<sub>sd</sub>", "m³/h", False, "2.2.1.取值"),
            ("主轴密封供水Q<sub>zz</sub>", "m³/h", False, "2.2.2.取值"),
            ("机组总用水量", "m³/h", True, None)
        ]

        self.design_value_inputs = []

        for i, (param_name, unit, is_total, source_key) in enumerate(parameters):
            row_layout = self.create_input_row(param_name, unit, is_total, i+1, source_key)
            layout.addLayout(row_layout)
            if not is_total:
                self.design_value_inputs.append(row_layout.itemAt(2).widget())

        confirm_layout = QHBoxLayout()
        confirm_layout.addStretch(1)

        self.confirm_label = QLabel("确认以上设计值无误")
        self.confirm_label.setStyleSheet("font-size: 24px; color: #e74c3c; font-weight: bold;")
        confirm_layout.addWidget(self.confirm_label)

        self.confirm_button = QPushButton("确认")
        self.confirm_button.setStyleSheet(self.button_style)
        self.confirm_button.setFixedSize(200, 60)
        self.confirm_button.clicked.connect(self.confirm_design_values)
        confirm_layout.addWidget(self.confirm_button)

        confirm_layout.addStretch(1)
        layout.addLayout(confirm_layout)

        return group

    def create_input_row(self, param_name, unit, is_total, index, source_key):
        row_layout = QHBoxLayout()
        stretch = 1 if not is_total else 2
        row_layout.addStretch(stretch)

        prefix = f"({index})" if not is_total else ""
        label = QLabel(f"{prefix}{param_name}：")
        label_style = "font-size: 24px; min-width: 150px; font-weight: bold;" if is_total else "font-size: 20px; min-width: 200px;"
        label.setStyleSheet(label_style)
        row_layout.addWidget(label)

        if is_total:
            self.total_design_usage_input = QLineEdit()
            self.total_design_usage_input.setReadOnly(True)
            self.total_design_usage_input.setStyleSheet(self.common_input_style + "min-width: 250px;")
            row_layout.addWidget(self.total_design_usage_input)

            self.source_key_total = source_key
        else:
            input_field = QLineEdit()
            input_field.setReadOnly(True)
            input_field.setStyleSheet(self.common_input_style + "min-width: 250px;")
            row_layout.addWidget(input_field)

            input_field.source_key = source_key

        unit_label = QLabel(unit)
        unit_label.setStyleSheet(self.unit_style)
        row_layout.addWidget(unit_label)

        row_layout.addStretch(1)
        return row_layout

    def create_pipe_design_group(self):
        """供水管设计"""
        group = QGroupBox("2.6 供水管设计")
        group.setStyleSheet(self.subgroup_style)
        group.setVisible(False)
        self.pipe_design_group = group

        layout = QVBoxLayout(group)
        layout.setSpacing(15)

        # 流速设置
        vj_group = QGroupBox()
        vj_layout = QHBoxLayout(vj_group)

        vj_label = QLabel("流速V<sub>j</sub>取：")
        vj_label.setStyleSheet("font-size: 20px; min-width: 150px;")
        vj_layout.addWidget(vj_label)

        self.flow_speed_min = QLineEdit()
        self.flow_speed_min.setStyleSheet(self.common_input_style + "min-width: 100px;")
        self.flow_speed_min.setText("1.0")
        vj_layout.addWidget(self.flow_speed_min)

        vj_layout.addWidget(QLabel("~"))

        self.flow_speed_max = QLineEdit()
        self.flow_speed_max.setStyleSheet(self.common_input_style + "min-width: 100px;")
        self.flow_speed_max.setText("3.0")
        vj_layout.addWidget(self.flow_speed_max)

        unit_label = QLabel("m/s")
        unit_label.setStyleSheet(self.unit_style)
        vj_layout.addWidget(unit_label)
        vj_layout.addStretch(1)

        layout.addWidget(vj_group)
        self.input_fields["2.6.流速Vj.最小值"] = self.flow_speed_min
        self.input_fields["2.6.流速Vj.最大值"] = self.flow_speed_max

        subsections = [
            {"title": "2.6.1 总管", "button_text": "材料\n选择",
             "param_names": ["计算管径d", "设计管型", "管内流速V"]},
            {"title": "2.6.2 上导轴承油冷却器供水管", "button_text": "材料\n选择",
             "param_names": ["计算管径d", "设计管型", "管内流速V"]},
            {"title": "2.6.3 推力轴承油冷却器供水管", "button_text": "材料\n选择",
             "param_names": ["计算管径d", "设计管型", "管内流速V"]},
            {"title": "2.6.4 下导轴承油冷却器供水管", "button_text": "材料\n选择",
             "param_names": ["计算管径d", "设计管型", "管内流速V"]},
            {"title": "2.6.5 空气冷却器供水管", "button_text": "材料\n选择",
             "param_names": ["计算管径d", "设计管型", "管内流速V"]},
            {"title": "2.6.6 水导轴承冷却水供水管", "button_text": "材料\n选择",
             "param_names": ["计算管径d", "设计管型", "管内流速V"]},
            {"title": "2.6.7 主轴密封供水供水管", "button_text": "材料\n选择",
             "param_names": ["计算管径d", "设计管型", "管内流速V"]}
        ]

        for config in subsections:
            # TODO: 修改实际文档路径
            layout.addWidget(self.create_pipe_subsection(
                config["title"], config["button_text"], r"C:\.pdf", config["param_names"]
            ))

        return group

    def create_pipe_subsection(self, title, button_text, pdf_path, param_names):
        group = QGroupBox(title)
        group.setStyleSheet(self.subgroup_style)
        layout = QHBoxLayout(group)

        params_layout = QVBoxLayout()
        for i, name in enumerate(param_names):
            row_layout = QHBoxLayout()

            label_text = f"{name}："
            if i == 1:  # 设计管型
                label_text = f"{name}：Φ"

            label = QLabel(label_text)
            label.setStyleSheet("font-size: 20px; min-width: 150px;")
            row_layout.addWidget(label)

            if i < 2:  # 前两个参数是范围
                max_input = QLineEdit()
                max_input.setStyleSheet(self.input_style + "min-width: 80px;")
                row_layout.addWidget(max_input)

                separator = "~" if i == 0 else "×"
                row_layout.addWidget(QLabel(separator))

                min_input = QLineEdit()
                min_input.setStyleSheet(self.input_style + "min-width: 80px;")
                row_layout.addWidget(min_input)

                if i == 0:
                    unit_label = QLabel("m")
                    unit_label.setStyleSheet(self.unit_style)
                    row_layout.addWidget(unit_label)

                self.input_fields[f"{title}.{name}.最大值"] = max_input
                self.input_fields[f"{title}.{name}.最小值"] = min_input
            else:  # 第三个参数是单值
                value_input = QLineEdit()
                value_input.setStyleSheet(self.input_style + "min-width: 180px;")
                row_layout.addWidget(value_input)
                unit_label = QLabel("m/s")
                unit_label.setStyleSheet(self.unit_style)
                row_layout.addWidget(unit_label)
                self.input_fields[f"{title}.{name}"] = value_input

            row_layout.addStretch(1)
            params_layout.addLayout(row_layout)

        layout.addLayout(params_layout)

        # PDF按钮
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton(button_text)
        button.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold;
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            min-width: 150px;
            min-height: 60px;
            text-align: center;
        """)
        button.setFixedSize(150, 80)
        button.clicked.connect(lambda: self.open_pdf_document(pdf_path))

        button_layout.addWidget(button)
        layout.addLayout(button_layout)

        return group

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

        # 2.5 设计用水量
        total_design_usage = 0.0
        for input_field in self.design_value_inputs:
            source_value = self.input_fields.get(input_field.source_key, None)
            if source_value:
                value = source_value.text()
                input_field.setText(value)

                total_design_usage += float(value) if value else 0.0

        # 更新总用水量
        self.total_design_usage_input.setText(f"{total_design_usage:.2f}")

        # 更新管道设计结果
        pipe_keys = [
            "2.6.1 总管",
            "2.6.2 上导轴承油冷却器供水管",
            "2.6.3 推力轴承油冷却器供水管",
            "2.6.4 下导轴承油冷却器供水管",
            "2.6.5 空气冷却器供水管",
            "2.6.6 水导轴承冷却水供水管",
            "2.6.7 主轴密封供水供水管"
        ]

        for pipe_key in pipe_keys:
            max_key = f"{pipe_key}.计算管径d.最大值"
            min_key = f"{pipe_key}.计算管径d.最小值"

            if max_key in results:
                max_value = results[max_key]
                max_field = self.input_fields.get(max_key)
                if max_field:
                    max_field.setText(f"{max_value:.3f}")

            if min_key in results:
                min_value = results[min_key]
                min_field = self.input_fields.get(min_key)
                if min_field:
                    min_field.setText(f"{min_value:.3f}")

    def on_param_changed(self, key, value):
        self.backend.set_tech_water_param(key, value)

    def confirm_design_values(self):
        all_filled = True
        for input_field in self.design_value_inputs:
            if not input_field.text().strip():
                all_filled = False
                break

        if not self.total_design_usage_input.text().strip():
            all_filled = False

        if all_filled:
            self.design_confirmed = True
            self.pipe_design_group.setVisible(True) # 显示2.6部分
            self.confirm_label.setText("设计值已确认")
            self.confirm_label.setStyleSheet("font-size: 24px; color: #27ae60; font-weight: bold;")
            self.confirm_button.setEnabled(False)
        else:
            self.confirm_label.setText("请先填写所有设计值")