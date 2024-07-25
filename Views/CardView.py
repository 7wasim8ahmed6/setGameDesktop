from typing import Optional

from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtWidgets import QWidget


class CardView(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.PAD = 5
        self.SEGMENT_PAD = 4

    def __getSegmentRect(self, cardRect: QRect) -> (QRect, int):
        segmentHt = cardRect.height() // 3
        return QRect(cardRect.topLeft(), QSize(cardRect.width(), segmentHt)).adjusted(self.SEGMENT_PAD,
                                                                                      self.SEGMENT_PAD,
                                                                                      -self.SEGMENT_PAD,
                                                                                      -self.SEGMENT_PAD), segmentHt

    def __getTripleRects(self, cardRect: QRect) -> [QRect]:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect2 = QRect(rect)
        rect2.translate(0, segWidth)
        rect3 = QRect(rect2)
        rect3.translate(0, segWidth)
        return [rect, rect2, rect3]

    def __getDoubleRects(self, cardRect: QRect) -> [QRect]:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect.translate(0, segWidth//2)
        rect2 = QRect(rect)
        rect2.translate(0, segWidth)
        return [rect, rect2]

    def __getSingleRect(self, cardRect: QRect) -> QRect:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect.translate(0, segWidth)
        return rect

    def _getRects(self, cardRect: QRect, number: int) -> [QRect]:
        if number > 3 or number < 1:
            return []
        if number == 1:
            rectList = []
            rectList.append(self.__getSingleRect(cardRect))
            return rectList
        if number == 2:
            return self.__getDoubleRects(cardRect)
        if number == 3:
            return self.__getTripleRects(cardRect)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Draw the white background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(self.PAD, self.PAD, -self.PAD, -self.PAD)
        painter.fillRect(rect, QBrush(QColor('White')))

        # Draw the non-filled rectangles
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor("Red"))
        painter.setPen(pen)
        # brush = QBrush(QColor("Red"), Qt.BrushStyle.HorPattern)
        # painter.setBrush(brush)
        painter.drawRects(self._getRects(rect, 3))
