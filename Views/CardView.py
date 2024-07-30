from typing import Optional, List

from PySide6.QtCore import QRect, QSize, QPointF, QObject, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, Qt, QPainterPath
from PySide6.QtWidgets import QWidget, QStyleOption, QStyle

from common.Card import *


class CardView(QWidget):
    onTapGesture = Signal(QObject)
    PADDING = 8
    SHAPE_PADDING = 6
    ORIENTATION = 15

    COLOR_MAPPING = {
        Color.RED: QColor("#ff0000"),
        Color.GREEN: QColor("#008000"),
        Color.PURPLE: QColor("#800080")
    }

    BRUSH_STYLE_MAPPING = {
        Filling.OPEN: Qt.BrushStyle.NoBrush,
        Filling.SHADED: Qt.BrushStyle.SolidPattern,
        Filling.STRIPED: Qt.BrushStyle.BDiagPattern
    }

    def __init__(self, card: Card, min_width, min_height, parent: Optional[QWidget] = None, isSelected=False, isMatched=False):
        super().__init__(parent)
        self.card = card
        self.is_selected = isSelected
        self.is_matched = isMatched
        self.setObjectName("CardViewV2")
        self.setMinimumSize(min_width, min_height)

    def setBackgroundStyle(self):
        if self.is_selected:
            self.setStyleSheet("""
                                CardViewV2 {
                                    background-color: lightsteelblue;
                                    border: 2px solid black;
                                    border-radius: 15px;
                                }
                            """)

        if self.is_matched:
            self.setStyleSheet("""
                                CardViewV2 {
                                    background-color: yellowgreen;
                                    border: 2px solid black;
                                    border-radius: 15px;
                                }
                            """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # This is to consider style sheet
        opt = QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)

        # Draw the white background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pad_val = self.PADDING
        rect = self.rect().adjusted(pad_val, pad_val, -pad_val, -pad_val)
        # painter.fillRect(rect, QBrush(QColor('White')))
        painter.setPen(self.__fetchPen())
        painter.setBrush(self.__fetchBrush())
        self.setBackgroundStyle()

        for seg_rect in self.__getRects(rect):
            painter.save()
            painter.translate(seg_rect.center())
            painter.rotate(self.ORIENTATION)
            painter.translate(-seg_rect.center())
            self.drawShape(painter, seg_rect)
            painter.restore()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.onTapGesture.emit(self)  # Emit the custom signal
        super().mousePressEvent(event)

    def __fetchPen(self):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.__fetchColor())
        return pen

    def __fetchBrush(self) -> QBrush:
        brush = QBrush(self.__fetchColor())
        brush.setStyle(self.BRUSH_STYLE_MAPPING[self.card.filling])
        return brush

    def __fetchColor(self) -> QColor:
        return self.COLOR_MAPPING[self.card.color]

    def __getSegmentRect(self, cardRect: QRect) -> (QRect, int):
        segmentHt = cardRect.height() // 3
        return QRect(cardRect.topLeft(), QSize(cardRect.width(), segmentHt)).adjusted(self.SHAPE_PADDING,
                                                                                      self.SHAPE_PADDING,
                                                                                      -self.SHAPE_PADDING,
                                                                                      -self.SHAPE_PADDING), segmentHt

    def __getTripleRects(self, cardRect: QRect) -> List[QRect]:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect2 = QRect(rect)
        rect2.translate(0, segWidth)
        rect3 = QRect(rect2)
        rect3.translate(0, segWidth)
        return [rect, rect2, rect3]

    def __getDoubleRects(self, cardRect: QRect) -> List[QRect]:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect.translate(0, segWidth // 2)
        rect2 = QRect(rect)
        rect2.translate(0, segWidth)
        return [rect, rect2]

    def __getSingleRect(self, cardRect: QRect) -> QRect:
        rect, segWidth = self.__getSegmentRect(cardRect)
        rect.translate(0, segWidth)
        return rect

    def __getRects(self, cardRect: QRect) -> List[QRect]:
        if self.card.number == Numbers.ONE:
            rectList = []
            rectList.append(self.__getSingleRect(cardRect))
            return rectList
        elif self.card.number == Numbers.TWO:
            return self.__getDoubleRects(cardRect)
        else:
            return self.__getTripleRects(cardRect)

    def drawShape(self, painter, seg_rect):
        if self.card.shape == Shape.OVAL:
            painter.drawEllipse(seg_rect)
        elif self.card.shape == Shape.DIAMOND:
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
        elif self.card.shape == Shape.SQUIGGLE:
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