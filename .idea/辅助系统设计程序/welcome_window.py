from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class WelcomeWindow(QWidget):
    start_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title = QLabel("水力机械油气水辅助系统设计程序", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 48px; font-weight: bold; color: #2c3e50;")

        self.company = QLabel("中国电建成都院\n勘测设计分公司·机电部", self)
        self.company.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.company.setStyleSheet("font-size: 36px; color: #7f8c8d;")

        self.start_button = QPushButton("开始使用", self)
        self.start_button.setFixedSize(300, 80)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 28px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.start_button.clicked.connect(self.start_clicked.emit)

        layout.addStretch(1)
        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addWidget(self.company)
        layout.addStretch(2)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)

        self.setLayout(layout)