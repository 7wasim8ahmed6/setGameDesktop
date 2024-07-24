import sys
from typing import Optional

from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QVBoxLayout, QScrollArea, \
    QSpacerItem, QSizePolicy, QHBoxLayout


class Card(QWidget):
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


class MainWindow(QMainWindow):

    def __init__(self, numberOfWidgets=6, minWidth=200, aspectRatio=2 / 3):
        super(MainWindow, self).__init__()
        self.setMinimumSize(800, 600)
        self.numOfWidgets = numberOfWidgets
        self.minWidthOfWidgets = minWidth
        self.aspectRat = aspectRatio

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        verticalLayout = QVBoxLayout(self.central_widget)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.addButtons()
        widget = QWidget()
        widget.setLayout(self.gridLayout)
        scroll_area.setWidget(widget)
        verticalLayout.addWidget(scroll_area)
        horLayout = QHBoxLayout()
        horLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        pushButton = QPushButton("Hint?")
        pushButton.setStyleSheet("padding: 15px;")
        horLayout.addWidget(pushButton)
        pushButton = QPushButton("Draw Cards")
        pushButton.setStyleSheet("padding: 15px;")
        horLayout.addWidget(pushButton)
        verticalLayout.addLayout(horLayout)
        self.setWindowTitle("My App")
        # self.showFullScreen()

    def addButtons(self):
        maxCol = self.computeColoumnSize()
        row = 0
        widgetsPlaced = 0
        while widgetsPlaced < self.numOfWidgets:
            for col in range(maxCol):
                button = Card()
                button.setMinimumWidth(self.minWidthOfWidgets)
                button.setMinimumHeight(int(self.minWidthOfWidgets // self.aspectRat))
                self.gridLayout.addWidget(button, row, col)
                widgetsPlaced += 1
                if widgetsPlaced >= self.numOfWidgets:
                    break
            row += 1
        if widgetsPlaced < maxCol:
            # print("Added a horizontal spacer")
            self.gridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0,
                                    widgetsPlaced)
        self.gridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), row + 1, 0)

    def computeColoumnSize(self):
        width = self.rect().width()
        numCol = width // self.minWidthOfWidgets
        return numCol if numCol > 0 else 1

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        self.rearrangeButtons()

    def rearrangeButtons(self):
        # Remove all existing widgets from the layout
        while self.gridLayout.count():
            child = self.gridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add the buttons again
        self.addButtons()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow(6)
    window.show()

    app.exec()
