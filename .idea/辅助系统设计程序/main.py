import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from auth_window import AuthWindow
from welcome_window import WelcomeWindow
from model_selection import ModelSelectionWindow
from basic_parameter import BasicParamWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("水机油气水辅助系统设计程序")
        #self.setGeometry(100, 100, 800, 600)

        # 堆叠窗口管理器
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.auth_window = AuthWindow()
        self.welcome_window = WelcomeWindow()
        self.model_selection = ModelSelectionWindow()
        self.basic_parameter = BasicParamWindow()

        self.stacked_widget.addWidget(self.auth_window) # window 0
        self.stacked_widget.addWidget(self.welcome_window) # window 1
        self.stacked_widget.addWidget(self.model_selection) # window 2
        self.stacked_widget.addWidget(self.basic_parameter) # window 3

        self.auth_window.login_success.connect(lambda: self.switch_window(1))
        self.welcome_window.start_clicked.connect(lambda: self.switch_window(2))
        self.model_selection.model_selected.connect(lambda: self.switch_window(3))
        self.basic_parameter.go_back.connect(lambda: self.switch_window(2))

        self.switch_window(0)

    def switch_window(self, index):
        # 更新返回按钮状态（从BasicParamWindow开始显示返回按钮）
        if index >= 3:
            self.basic_parameter.show_back_button(True)
        else:
            self.basic_parameter.show_back_button(False)

        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowState(Qt.WindowMaximized)
    window.show()
    sys.exit(app.exec_())