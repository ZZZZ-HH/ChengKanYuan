import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from auth_window import AuthWindow
from welcome_window import WelcomeWindow
from model_selection import ModelSelectionWindow
from basic_parameter import BasicParamWindow
from system_selection import SystemSelectionWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("水机油气水辅助系统设计程序")

        self.basic_param = {}
        self.selected_model = ""

        # 堆叠窗口管理器
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.auth_window = AuthWindow()
        self.welcome_window = WelcomeWindow()
        self.model_selection = ModelSelectionWindow()
        self.basic_parameter = BasicParamWindow()
        self.system_selection = SystemSelectionWindow()

        self.stacked_widget.addWidget(self.auth_window) # window 0
        self.stacked_widget.addWidget(self.welcome_window) # window 1
        self.stacked_widget.addWidget(self.model_selection) # window 2
        self.stacked_widget.addWidget(self.basic_parameter) # window 3
        self.stacked_widget.addWidget(self.system_selection) # window 4

        self.auth_window.login_success.connect(lambda: self.switch_window(1))
        self.welcome_window.start_clicked.connect(lambda: self.switch_window(2))
        self.basic_parameter.go_back.connect(lambda: self.switch_window(2))
        self.system_selection.go_back.connect(lambda: self.switch_window(3))

        self.model_selection.model_selected.connect(self.on_model_selected)
        self.basic_parameter.next_step.connect(self.handle_basic_params)

        self.switch_window(0)

    def switch_window(self, index):
        # 更新返回按钮状态（从BasicParamWindow开始显示返回按钮）
        if index >= 3:
            self.basic_parameter.show_back_button(True)
        else:
            self.basic_parameter.show_back_button(False)

        self.stacked_widget.setCurrentIndex(index)

    def on_model_selected(self, model_name):
        self.selected_model = model_name
        self.basic_parameter.set_model_name(model_name)
        self.switch_window(3)
        print("机组类型：", self.selected_model)

    def handle_basic_params(self, params):
        self.basic_param = params
        self.switch_window(4)
        print("接收到的参数：", self.basic_param)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowState(Qt.WindowMaximized)
    window.show()
    sys.exit(app.exec_())