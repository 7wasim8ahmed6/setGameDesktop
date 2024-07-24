from typing import Optional

from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtWidgets import QWidget


class CardView(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        rect = self.rect().adjusted(5, 5, -5, -5)
        brush = QBrush()
        brush.setColor(QColor('White'))
        # brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)
        painter.drawRoundedRect(rect, 10.0, 10.0)