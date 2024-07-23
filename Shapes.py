from PyQt6 import QtGui, QtWidgets


class OvalWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor('blue')))
        painter.drawEllipse(self.rect())


class RectangleWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor('green')))
        painter.drawRect(self.rect())
