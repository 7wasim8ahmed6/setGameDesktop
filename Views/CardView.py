from enum import Enum
from typing import Optional

from PyQt6.QtCore import QRect, QSize, Qt, QPointF, pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen, QPainterPath
from PyQt6.QtWidgets import QWidget, QStyleOption, QStyle


class CardView(QWidget):
    onTapGesture = pyqtSignal(QObject)
    class Shape(Enum):
        OVAL = 1
        DIAMOND = 2
        SQUIGGLE = 3

    class Filling(Enum):
        OPEN = 1
        SHADED = 2
        STRIPED = 3

    class Numbers(Enum):
        ONE = 1
        TWO = 2
        THREE = 3

    class Color(Enum):
        RED = 1
        PURPLE = 2
        GREEN = 3

    def __init__(self, parent: Optional[QWidget] = None, shape=Shape.OVAL, filling=Filling.OPEN, number=Numbers.ONE,
                 color=Color.GREEN):
        super().__init__(parent)
        self.shape = shape
        self.filling = filling
        self.numbers = number
        self.color = color
        self.PAD = 8
        self.SEGMENT_PAD = 6
        self.ImageOrientation = 15
        self.setStyleSheet("""
                                CardView {
                                    background-color: mintcream;
                                    border: 2px solid black;
                                    border-radius: 15px;
                                }
                            """)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.onTapGesture.emit(self)  # Emit the custom signal
        super().mousePressEvent(event)

    def __getDoubleRects(self, cardRect: QRect) -> [QRect]:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect.translate(0, segWidth // 2)
        rect2 = QRect(rect)
        rect2.translate(0, segWidth)
        return [rect, rect2]

    def __getSingleRect(self, cardRect: QRect) -> QRect:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect.translate(0, segWidth)
        return rect

    def __getRects(self, cardRect: QRect) -> [QRect]:
        if self.numbers == CardView.Numbers.ONE:
            rectList = []
            rectList.append(self.__getSingleRect(cardRect))
            return rectList
        elif self.numbers == CardView.Numbers.TWO:
            return self.__getDoubleRects(cardRect)
        else:
            return self.__getTripleRects(cardRect)

    def __fetchColor(self) -> QColor:
        if self.color == CardView.Color.RED:
            return QColor("#ff0000")
        elif self.color == CardView.Color.GREEN:
            return QColor("#008000")
        else:
            return QColor("#800080")

    def __fetchPen(self) -> QPen:
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.__fetchColor())
        return pen

    def __fetchBrush(self) -> QBrush:
        brush = QBrush(self.__fetchColor())
        if self.filling == CardView.Filling.OPEN:
            brush.setStyle(Qt.BrushStyle.NoBrush)
        elif self.filling == CardView.Filling.SHADED:
            brush.setStyle(Qt.BrushStyle.SolidPattern)
        else:
            brush.setStyle(Qt.BrushStyle.BDiagPattern)
        return brush
    def select(self):
        self.setStyleSheet("""
                                CardView {
                                    background-color: lightsteelblue;
                                    border: 2px solid black;
                                    border-radius: 15px;
                                }
                            """)

    def match(self):
        self.setStyleSheet("""
                                CardView {
                                    background-color: yellowgreen;
                                    border: 2px solid black;
                                    border-radius: 15px;
                                }
                            """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        opt = QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)

        # Draw the white background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(self.PAD, self.PAD, -self.PAD, -self.PAD)
        # painter.fillRect(rect, QBrush(QColor('White')))

        # Draw the non-filled rectangles
        painter.setPen(self.__fetchPen())
        painter.setBrush(self.__fetchBrush())
        # Draw each shape with rotation
        for seg_rect in self.__getRects(rect):
            painter.save()
            painter.translate(seg_rect.center())
            painter.rotate(self.ImageOrientation)
            painter.translate(-seg_rect.center())

            if self.shape == CardView.Shape.OVAL:
                painter.drawEllipse(seg_rect)
            elif self.shape == CardView.Shape.DIAMOND:
                path = QPainterPath()
                points = [
                    QPointF(seg_rect.center().x(), seg_rect.top()),
                    QPointF(seg_rect.right(), seg_rect.center().y()),
                    QPointF(seg_rect.center().x(), seg_rect.bottom()),
                    QPointF(seg_rect.left(), seg_rect.center().y())
                ]
                path.moveTo(points[0])
                for point in points[1:]:
                    path.lineTo(point)
                path.closeSubpath()
                painter.drawPath(path)
            elif self.shape == CardView.Shape.SQUIGGLE:
                path = QPainterPath()
                start_x = seg_rect.left()
                start_y = seg_rect.center().y()
                end_x = seg_rect.right()
                end_y = seg_rect.center().y()
                control1_x = seg_rect.left() + seg_rect.width() / 4
                control1_y = seg_rect.top() - seg_rect.height() / 4
                control2_x = seg_rect.left() + 3 * seg_rect.width() / 4
                control2_y = seg_rect.bottom() + seg_rect.height() / 4
                control3_x = seg_rect.left() + seg_rect.width() / 4
                control3_y = seg_rect.bottom() + seg_rect.height() / 4
                control4_x = seg_rect.left() + 3 * seg_rect.width() / 4
                control4_y = seg_rect.top() - seg_rect.height() / 4

                path.moveTo(start_x, start_y)
                path.cubicTo(control1_x, control1_y, control2_x, control2_y, end_x, end_y)
                path.cubicTo(control4_x, control4_y, control3_x, control3_y, start_x, start_y)
                painter.drawPath(path)

            painter.restore()
