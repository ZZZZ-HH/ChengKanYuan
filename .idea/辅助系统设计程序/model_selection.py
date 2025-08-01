from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class ModelSelectionWindow(QWidget):
    model_selected = pyqtSignal(str)

    def __init__(self, backend_manager):
        super().__init__()
        self.backend = backend_manager
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        title = QLabel("请选择机组类型", self)
        title.setStyleSheet("font-size: 42px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        grid = QGridLayout()
        models = ["混流式水轮机", "轴流式水轮机", "贯流式水轮机", "冲击式水轮机", "水泵水轮机"]

        for i, model in enumerate(models):
            btn = QPushButton(model, self)
            btn.setFixedSize(300, 120)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 28px;
                    background-color: #ecf0f1;
                    border: 2px solid #bdc3c7;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: #d6dbdf;
                }
            """)
            btn.clicked.connect(lambda checked, m=model: self.on_model_selected(m))
            grid.addWidget(btn, i // 3, i % 3)

        main_layout.addSpacing(80)
        main_layout.addWidget(title)
        main_layout.addSpacing(80)
        main_layout.addLayout(grid)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def on_model_selected(self, model_name):
        self.model_selected.emit(model_name)
        self.backend.set_model(model_name)