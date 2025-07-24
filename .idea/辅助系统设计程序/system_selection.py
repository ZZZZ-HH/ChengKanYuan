from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal

from System_Calculations.tech_water_supply_system_page import TechWaterSupplySystemPage

class SystemSelectionWindow(QWidget):
    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.system_pages = {}
        self.selected_model = ""
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        content_layout = QHBoxLayout()

        # 左侧系统列表
        self.sidebar = QVBoxLayout()
        self.sidebar.setSpacing(10)

        systems = [
            "技术供水系统", "检修排水系统", "渗漏排水系统", "透平油系统", "绝缘油系统", "低压气系统", "中压气系统"
        ]

        self.system_buttons = []
        for i, system in enumerate(systems):
            btn = QPushButton(system, self)
            btn.setFixedSize(180, 60)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    background-color: #ecf0f1;
                    border: 1px solid #bdc3c7;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #d6dbdf;
                }
                QPushButton:checked {
                    background-color: #3498db;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i, sys=system: self.switch_system(idx, sys))
            self.system_buttons.append(btn)
            self.sidebar.addWidget(btn)

        if self.system_buttons:
            self.system_buttons[0].setChecked(True)

        self.sidebar.addStretch(1)
        content_layout.addLayout(self.sidebar)

        # 系统计算区
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("""
            QStackedWidget {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #bdc3c7;
            }
        """)

        # 创建各个系统的页面
        for system in systems:
            if system == "技术供水系统":
                page = TechWaterSupplySystemPage()
                page.set_model_name(self.selected_model)
                self.content_area.addWidget(page)
                self.system_pages[system] = page
            else:
                pass

        content_layout.addWidget(self.content_area, 1)

        main_layout.addLayout(content_layout, 1)

        bottom_layout = QHBoxLayout()

        self.back_btn = QPushButton("返回", self)
        self.back_btn.setFixedSize(150, 60)
        self.back_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #95a5a6;"
            "   color: white;"
            "   font-size: 24px;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #7f8c8d;"
            "}"
        )
        self.back_btn.clicked.connect(self.go_back.emit)

        bottom_layout.addWidget(self.back_btn)
        bottom_layout.addStretch(1)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def set_model_name(self, model_name):
        self.selected_model = model_name
        for page in self.system_pages.values():
            page.set_model_name(model_name)

    def switch_system(self, index):
        for i, btn in enumerate(self.system_buttons):
            btn.setChecked(i == index)

        self.content_area.setCurrentIndex(index)