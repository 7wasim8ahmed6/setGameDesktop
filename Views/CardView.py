from typing import Optional

from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtWidgets import QWidget


class CardView(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Draw the white background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(5, 5, -5, -5)
        painter.fillRect(rect, QBrush(QColor('White')))

        # Draw the non-filled rectangles
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)

        segmentHt = rect.height() // 3

        brush = QBrush(QColor("Red"))
        # First rectangle
        newRect = QRect(rect.topLeft(), QSize(rect.width(), segmentHt)).adjusted(3, 3, -3, -3)
        pen.setColor(QColor("Red"))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(newRect)

        painter.setBrush(Qt.BrushStyle.HorPattern)
        # Second rectangle
        newRect2 = QRect(newRect)
        newRect2.translate(0, segmentHt/2)
        pen.setColor(QColor("Blue"))
        painter.setPen(pen)
        painter.drawRect(newRect2)

        # Third rectangle
        newRect3 = QRect(newRect2)
        newRect3.translate(0, segmentHt)
        pen.setColor(QColor("Green"))
        painter.setPen(pen)
        painter.drawRect(newRect3)

    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     painter = QPainter(self)
    #     rect = self.rect().adjusted(5, 5, -5, -5)
    #     brush = QBrush()
    #     brush.setColor(QColor('White'))
    #     brush.setStyle(Qt.BrushStyle.SolidPattern)
    #     painter.setBrush(brush)
    #     painter.drawRoundedRect(rect, 10.0, 10.0)
    #     segmentHt = rect.height() // 3
    #     newRect = QRect(rect.topLeft(), QSize(rect.width(), segmentHt)).adjusted(3, 3, -3, -3)
    #     newRect2 = QRect(newRect)
    #     newRect2.translate(0, segmentHt)
    #     newRect3 = QRect(newRect2)
    #     newRect3.translate(0, segmentHt)
    #     pen = QPen()
    #     pen.setWidth(2)
    #     pen.setColor(QColor("#EB5160"))
    #     painter.setPen(pen)
    #     painter.drawRect(newRect)
    #     painter.drawRect(newRect2)
    #     painter.drawRect(newRect3)
    #     pen.setColor(QColor("#94EB52"))
    #     painter.setPen(pen)
    #     newRect4 = QRect(newRect)
    #     newRect4.translate(0, segmentHt//2)
    #     painter.drawRect(newRect4)
    #     newRect5 = QRect(newRect4)
    #     newRect5.translate(0, segmentHt)
    #     painter.drawRect(newRect5)
    #     pen.setColor(QColor("#3434FF"))
    #     painter.setPen(pen)
    #     newRect6 = QRect(newRect2)
    #     painter.drawRect(newRect6)