import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from constants import TEXT_1, TEXT_2, WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT, MARGINS, SPACING, LABEL_MIN_HEIGHT
from styles import MAIN_WINDOW_STYLE, LABEL_STYLE, BUTTON_STYLE
from widgets import BackgroundWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_is_changed = False
        self._setup_window()
        self._create_layout()
        self._create_label()
        self._create_buttons()

    def _setup_window(self):
        self.setWindowTitle("Приложение на PyQT")
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        self.central_widget = BackgroundWidget()
        self.setCentralWidget(self.central_widget)

    def _create_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(MARGINS, MARGINS, MARGINS, MARGINS)
        main_layout.setSpacing(SPACING)
        self.central_widget.setLayout(main_layout)
        self.main_layout = main_layout

    def _create_label(self):
        self.label = QLabel(TEXT_1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(LABEL_STYLE)
        self.label.setMinimumHeight(LABEL_MIN_HEIGHT)
        self.main_layout.addWidget(self.label)

    def _create_buttons(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(SPACING)
        self.main_layout.addLayout(buttons_layout)

        self.button1 = QPushButton("Сменить текст")
        self.button1.clicked.connect(self.change_label_text)
        self.button1.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(self.button1)

        self.button2 = QPushButton("Загрузить изображение")
        self.button2.clicked.connect(self.load_transparent_image)
        self.button2.setStyleSheet(BUTTON_STYLE)
        buttons_layout.addWidget(self.button2)

    def change_label_text(self):
        if self.text_is_changed:
            self.label.setText(TEXT_1)
        else:
            self.label.setText(TEXT_2)
        self.text_is_changed = not self.text_is_changed

    def load_transparent_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Загрузите изображение",
            "",
            "PNG Files (*.png);;All Files (*)"
        )

        if not file_path:
            return

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить изображение.")
            return

        self.central_widget.set_background_pixmap(pixmap)

        img_width = pixmap.width()
        img_height = pixmap.height()
        screen = self.screen().availableGeometry()

        if img_width > screen.width() or img_height > screen.height():
            self.showMaximized()
        else:
            self.resize(img_width, img_height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())