from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QFormLayout
from PyQt5.QtCore import Qt

class TechWaterSupplySystemPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("技术供水系统计算", self)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        label1 = QLabel("供水方式：", self)
        label1.setStyleSheet("font-size: 24px;")
        self.input1 = QLineEdit(self)
        self.input1.setStyleSheet("font-size: 24px; min-height: 40px;")
        form_layout.addRow(label1, self.input1)

        layout.addLayout(form_layout)
        layout.addStretch(1)
        self.setLayout(layout)