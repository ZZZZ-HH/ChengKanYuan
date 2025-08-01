from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QScrollArea, QFormLayout, QLineEdit, QDoubleSpinBox,
                             QComboBox, QDateEdit, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QDate

class BasicParamWindow(QWidget):
    go_back = pyqtSignal()
    next_step = pyqtSignal(dict) # 传递参数字典的信号

    def __init__(self, backend_manager):
        super().__init__()
        self.backend = backend_manager
        self.back_button = None
        self.next_button = None
        self.input_fields = {} # 存储所有输入字段
        self.model_label = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        top_container = QHBoxLayout()
        top_container.setContentsMargins(0, 0, 0, 0)

        title_container = QHBoxLayout()
        title_container.addStretch(2)
        self.title = QLabel("电站基本参数", self)
        self.title.setStyleSheet("font-size: 42px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_container.addWidget(self.title)
        title_container.addStretch(1)

        self.model_label = QLabel("机型：未选择", self)
        self.model_label.setStyleSheet("font-size: 32px; color: #3498db; font-weight: bold; padding: 10px;")
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        top_container.addLayout(title_container, 1)
        top_container.addWidget(self.model_label, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        main_layout.addLayout(top_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setVerticalSpacing(20)

        # 输入框
        input_style = """
            font-size: 30px;
            min-height: 60px;
            height: 60px;
        """

        # 单位
        unit_style = """
            font-size: 30px;
            min-height: 60px;
            padding-top: 10px;
        """

        # 1.电站名称
        param1_layout = QHBoxLayout()
        param1_input = QLineEdit()
        param1_input.setStyleSheet(input_style)
        param1_layout.addWidget(param1_input)
        param1_layout.addStretch()
        form_layout.addRow(QLabel("电站名称："), param1_layout)
        self.input_fields["电站名称"] = param1_input

        # 2.设计阶段
        param2_layout = QHBoxLayout()
        param2_input = QComboBox()
        param2_input.setStyleSheet(input_style)
        param2_input.addItems(["阶段1", "阶段2", "阶段3"])
        param2_layout.addWidget(param2_input)
        param2_layout.addStretch()
        form_layout.addRow(QLabel("设计阶段："), param2_layout)
        self.input_fields["设计阶段"] = param2_input

        # 3.日期
        date_layout = QHBoxLayout()
        date_input = QDateEdit()
        date_input.setStyleSheet("""
            QDateEdit {
                font-size: 30px;
                min-height: 60px;
                height: 60px;
            }
            QCalendarWidget QWidget {
                font-size: 16px;
                alternate-background-color: #f0f0f0;
            }
            QCalendarWidget QToolButton {
                height: 30px;
                width: 80px;
                font-size: 16px;
                icon-size: 20px, 20px;
            }
            QCalendarWidget QMenu {
                font-size: 16px;
            }
            QCalendarWidget QSpinBox {
                width: 80px;
                font-size: 16px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #3498db;
                selection-color: white;
                font-size: 16px;
            }
        """)
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        date_input.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(date_input)
        date_layout.addStretch()
        form_layout.addRow(QLabel("日期:"), date_layout)
        self.input_fields["日期"] = date_input

        # 4.装机容量
        param4_layout = QHBoxLayout()
        param4_input = QLineEdit()
        param4_input.setStyleSheet(input_style)
        param4_layout.addWidget(param4_input)
        unit_label4 = QLabel("MW")
        unit_label4.setStyleSheet(unit_style)
        param4_layout.addWidget(unit_label4)
        param4_layout.addStretch()
        form_layout.addRow(QLabel("装机容量："), param4_layout)
        self.input_fields["装机容量"] = param4_input

        # 5.装机台数
        param5_layout = QHBoxLayout()
        param5_input = QLineEdit()
        param5_input.setStyleSheet(input_style)
        param5_layout.addWidget(param5_input)
        unit_label5 = QLabel("台")
        unit_label5.setStyleSheet(unit_style)
        param5_layout.addWidget(unit_label5)
        param5_layout.addStretch()
        form_layout.addRow(QLabel("装机台数："), param5_layout)
        self.input_fields["装机台数"] = param5_input

        # 6.发电机效率
        param6_layout = QHBoxLayout()
        param6_input = QLineEdit()
        param6_input.setStyleSheet(input_style)
        param6_layout.addWidget(param6_input)
        unit_label6 = QLabel("%")
        unit_label6.setStyleSheet(unit_style)
        param6_layout.addWidget(unit_label6)
        param6_layout.addStretch()
        form_layout.addRow(QLabel("发电机效率："), param6_layout)
        self.input_fields["发电机效率"] = param6_input

        # 7.水轮机安装海拔高程
        param7_layout = QHBoxLayout()
        param7_input = QLineEdit()
        param7_input.setStyleSheet(input_style)
        param7_layout.addWidget(param7_input)
        unit_label7 = QLabel("m")
        unit_label7.setStyleSheet(unit_style)
        param7_layout.addWidget(unit_label7)
        param7_layout.addStretch()
        form_layout.addRow(QLabel("水轮机安装海拔高程："), param7_layout)
        self.input_fields["水轮机安装海拔高程"] = param7_input

        # 8.额定转速
        param8_layout = QHBoxLayout()
        param8_input = QLineEdit()
        param8_input.setStyleSheet(input_style)
        param8_layout.addWidget(param8_input)
        unit_label8 = QLabel("r/min")
        unit_label8.setStyleSheet(unit_style)
        param8_layout.addWidget(unit_label8)
        param8_layout.addStretch()
        form_layout.addRow(QLabel("额定转速："), param8_layout)
        self.input_fields["额定转速"] = param8_input

        # 9.最大水头
        param9_layout = QHBoxLayout()
        param9_input = QLineEdit()
        param9_input.setStyleSheet(input_style)
        param9_layout.addWidget(param9_input)
        unit_label9 = QLabel("m")
        unit_label9.setStyleSheet(unit_style)
        param9_layout.addWidget(unit_label9)
        param9_layout.addStretch()
        form_layout.addRow(QLabel("最大水头："), param9_layout)
        self.input_fields["最大水头"] = param9_input

        # 10.最小水头
        param10_layout = QHBoxLayout()
        param10_input = QLineEdit()
        param10_input.setStyleSheet(input_style)
        param10_layout.addWidget(param10_input)
        unit_label10 = QLabel("m")
        unit_label10.setStyleSheet(unit_style)
        param10_layout.addWidget(unit_label10)
        param10_layout.addStretch()
        form_layout.addRow(QLabel("最小水头："), param10_layout)
        self.input_fields["最小水头"] = param10_input

        # 11.额定水头
        param11_layout = QHBoxLayout()
        param11_input = QLineEdit()
        param11_input.setStyleSheet(input_style)
        param11_layout.addWidget(param11_input)
        unit_label11 = QLabel("m")
        unit_label11.setStyleSheet(unit_style)
        param11_layout.addWidget(unit_label11)
        param11_layout.addStretch()
        form_layout.addRow(QLabel("额定水头："), param11_layout)
        self.input_fields["额定水头"] = param11_input

        # 12.水轮机型号
        param12_layout = QHBoxLayout()
        param12_input = QLineEdit()
        param12_input.setStyleSheet(input_style)
        param12_layout.addWidget(param12_input)
        param12_layout.addStretch()
        form_layout.addRow(QLabel("水轮机型号："), param12_layout)
        self.input_fields["水轮机型号"] = param12_input

        # 13.水轮机转轮直径
        param13_layout = QHBoxLayout()
        param13_input = QLineEdit()
        param13_input.setStyleSheet(input_style)
        param13_layout.addWidget(param13_input)
        unit_label13 = QLabel("m")
        unit_label13.setStyleSheet(unit_style)
        param13_layout.addWidget(unit_label13)
        param13_layout.addStretch()
        form_layout.addRow(QLabel("水轮机转轮直径D<sub>1</sub>："), param13_layout)
        self.input_fields["水轮机转轮直径"] = param13_input

        # 14.水轮机额定比转速
        param14_layout = QHBoxLayout()
        param14_input = QLineEdit()
        param14_input.setStyleSheet(input_style)
        param14_layout.addWidget(param14_input)
        unit_label14 = QLabel("m·kW")
        unit_label14.setStyleSheet(unit_style)
        param14_layout.addWidget(unit_label14)
        param14_layout.addStretch()
        form_layout.addRow(QLabel("水轮机额定比转速n<sub>s</sub>："), param14_layout)
        self.input_fields["水轮机额定比转速"] = param14_input

        # 15.发电机型号
        param15_layout = QHBoxLayout()
        param15_input = QLineEdit()
        param15_input.setStyleSheet(input_style)
        param15_layout.addWidget(param15_input)
        param15_layout.addStretch()
        form_layout.addRow(QLabel("发电机型号："), param15_layout)
        self.input_fields["发电机型号"] = param15_input

        # 16.发电机额定cos phi
        param16_layout = QHBoxLayout()
        param16_input = QLineEdit()
        param16_input.setStyleSheet(input_style)
        param16_layout.addWidget(param16_input)
        unit_label16 = QLabel("（滞后）")
        unit_label16.setStyleSheet(unit_style)
        param16_layout.addWidget(unit_label16)
        param16_layout.addStretch()
        form_layout.addRow(QLabel("发电机额定cos𝜙："), param16_layout)
        self.input_fields["发电机额定cos"] = param16_input

        # TODO 17.重力加速度g

        # TODO 18.海拔高程对空压机生产率修正系数

        for i in range(form_layout.rowCount()):
            label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
            field_item = form_layout.itemAt(i, QFormLayout.FieldRole)

            if label_item and label_item.widget():
                label_item.widget().setStyleSheet("font-size: 30px; font-weight: bold;")
                label_item.widget().setFixedHeight(70)

            if field_item and field_item.layout():
                for j in range(field_item.layout().count()):
                    widget = field_item.layout().itemAt(j).widget()
                    if widget:
                        widget.setMinimumHeight(60)
                        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        form_container = QHBoxLayout()
        form_container.addStretch(1)
        form_container.addLayout(form_layout)
        form_container.addStretch(1)

        scroll_layout.addLayout(form_container)
        scroll_layout.addStretch(1)

        scroll_area.setWidget(scroll_content)

        bottom_layout = QHBoxLayout()

        self.back_button = QPushButton("返回", self)
        self.back_button.setFixedSize(150, 60)
        self.back_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #95a5a6;"
            "   color: white;"
            "   font-size: 24px;"
            "   border-radius: 10px;"
            "   min-height: 60px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #7f8c8d;"
            "}"
        )
        self.back_button.clicked.connect(self.go_back.emit)

        self.next_button = QPushButton("下一步", self)
        self.next_button.setFixedSize(150, 60)
        self.next_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #2ecc71;"
            "   color: white;"
            "   font-size: 24px;"
            "   border-radius: 10px;"
            "   min-height: 60px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #27ae60;"
            "}"
        )
        self.next_button.clicked.connect(self.on_next_clicked)

        bottom_layout.addWidget(self.back_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.next_button)

        main_layout.addSpacing(20)
        main_layout.addWidget(scroll_area, 1)
        main_layout.addSpacing(20)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def on_next_clicked(self):
        params = {}

        station_name = self.input_fields["电站名称"].text().strip()
        params["电站名称"] = station_name if station_name else ""

        design_stage = self.input_fields["设计阶段"].currentText()
        params["设计阶段"] = design_stage if design_stage else ""

        date_value = self.input_fields["日期"].date()
        params["日期"] = date_value.toString("yyyy-MM-dd") if date_value.isValid() else ""

        numeric_fields = [
            "装机容量", "装机台数", "发电机效率", "水轮机安装海拔高程", "额定转速", "最大水头", "最小水头",
            "额定水头", "水轮机转轮直径", "水轮机额定比转速", "发电机额定cos"
        ]

        for field in numeric_fields:
            text_value = self.input_fields[field].text().strip()

            if text_value == "":
                params[field] = 0.0
            else:
                try:
                    params[field] = float(text_value)
                except ValueError:
                    params[field] = 0.0

        turbine_model = self.input_fields["水轮机型号"].text().strip()
        params["水轮机型号"] = turbine_model if turbine_model else ""

        generator_model = self.input_fields["发电机型号"].text().strip()
        params["发电机型号"] = generator_model if generator_model else ""

        self.backend.set_basic_params(params)
        self.next_step.emit(params)

    def set_model_name(self, model_name):
        self.model_label.setText(f"机组类型：{model_name}")

    def show_back_button(self, visible):
        if self.back_button:
            self.back_button.setVisible(visible)