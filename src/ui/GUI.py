from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *

from src.ui.BaseUi import BaseUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reversi")
        self.setFixedSize(QSize(1200, 700))
        self.setStyleSheet("background-color: darkgrey")

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QGridLayout()
        self.central.setLayout(self.layout)

        self.title_label = self.generate_title_label("Welcome to reversi!", 25, True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._build_menu_layout()

        self.layout.addWidget(self.title_label, 0, 0)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 9)
        self.layout.setColumnStretch(0, 8)
        self.layout.setColumnStretch(8, 9)

    def _build_menu_layout(self):
        self.menu_layout = QVBoxLayout()
        self.layout.addLayout(self.menu_layout, 1, 0)

        self.option_title_label = self.generate_title_label("  Please choose a game mode", 20)
        self.option_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.option_title_label.setFixedHeight(100)

        self.bot_button = QPushButton("Play against a bot")
        self.bot_button.setFixedHeight(100)
        self.bot_button.setFont(QFont("Arial", 20))
        self.bot_button.setStyleSheet("border-radius: 5px; "
                                      "border: 1px solid")
        self.bot_button.clicked.connect(self.bot_button_click)

        self.human_button = QPushButton("Play against a local player")
        self.human_button.setFixedHeight(100)
        self.human_button.setFont(QFont("Arial", 20))
        self.human_button.setStyleSheet(self.human_button.styleSheet() +
                                        "border-radius: 5px; "
                                        "border: 1px solid")
        self.human_button.clicked.connect(self.human_button_click)

        self.menu_layout.addStretch()
        self.menu_layout.addWidget(self.option_title_label)
        self.menu_layout.addWidget(self.bot_button)
        self.menu_layout.addWidget(self.human_button)
        self.menu_layout.addStretch()

    def human_button_click(self):
        print("Human")

    def bot_button_click(self):
        print("bot")

    def generate_test_label(self, text: str, color: str):
        """
        Make a test label with the given text and color.
        :param text: The text of the test label.
        :param color: The color of the test label. Must be a correct CSS color.
        :return: None
        """
        lbl = QLabel(text)
        lbl.setStyleSheet(f"background-color: {color}")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return lbl

    def generate_title_label(self, text: str = None, font_size: int = None, bold: bool = False):
        lbl = QLabel(text)

        if font_size is None:
            font_size = 20

        font = QFont("Arial", font_size)
        font.setBold(bold)
        lbl.setFont(font)

        lbl.setStyleSheet("background-color: gainsboro; "
                          "border-radius: 5")
        return lbl

class GUI(BaseUI):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        app = QApplication([])

        window = MainWindow()
        window.show()

        app.exec()