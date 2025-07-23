from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

class AuthWindow(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("系统认证", self)
        self.label.setStyleSheet("font-size: 36px; font-weight: bold;")

        self.prompt = QLabel("请输入访问密码:", self)
        self.prompt.setStyleSheet("font-size: 24px;")

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(400, 60)
        self.password_input.setStyleSheet("font-size: 24px;")

        self.login_button = QPushButton("登录", self)
        self.login_button.setFixedSize(200, 70)
        self.login_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                background-color: #3498db;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.login_button.clicked.connect(self.check_password)

        layout.addStretch(1)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.prompt, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)

        self.setLayout(layout)

    def check_password(self):
        if self.password_input.text() == "": # 密码
            self.login_success.emit()
        else:
            QMessageBox.warning(self, "认证失败", "密码不正确，请重试！")
            self.password_input.clear()