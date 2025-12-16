from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QPixmap
from PyQt5.QtCore import Qt
from constants import COLOR_DARK, COLOR_LIGHT, BACKGROUND_OPACITY


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_pixmap = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    def set_background_pixmap(self, pixmap: QPixmap):
        self.background_pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.background_pixmap:
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            painter.setOpacity(BACKGROUND_OPACITY)
            painter.drawPixmap(0, 0, scaled_pixmap)
        else:
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(COLOR_DARK))
            gradient.setColorAt(1, QColor(COLOR_LIGHT))
            painter.fillRect(self.rect(), gradient)

        painter.end()

