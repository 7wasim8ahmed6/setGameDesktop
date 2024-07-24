import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QVBoxLayout, QScrollArea, \
    QSpacerItem, QSizePolicy, QHBoxLayout


class MainWindow(QMainWindow):

    def __init__(self, numberOfWidgets=12, minWidth=180, aspectRatio=2/3):
        super(MainWindow, self).__init__()
        self.setMinimumSize(800, 600)
        # self.showFullScreen()
        self.numOfWidgets = numberOfWidgets
        self.minWidthOfWidgets = minWidth
        self.aspectRat = aspectRatio

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        verticalLayout = QVBoxLayout(self.central_widget)
        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        maxCol = self.computeColoumnSize()
        row = 0
        widgetsPlaced = 0
        while widgetsPlaced < numberOfWidgets:
            for col in range(maxCol):
                button = QPushButton("Hello")
                button.setMinimumWidth(self.minWidthOfWidgets)
                button.setMinimumHeight(int(self.minWidthOfWidgets//aspectRatio))
                # button.setStyleSheet("margin: 0px; padding: 0px;")
                gridLayout.addWidget(button, row, col)
                widgetsPlaced += 1
                if widgetsPlaced >= numberOfWidgets:
                    break
            row += 1

        # gridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum,  QSizePolicy.Policy.Expanding))
            # Add horizontal spacer to push buttons to the left
        # gridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, maxCol)
            # Add vertical spacer to push buttons to the top
        gridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), row + 1, 0)

        widget = QWidget()
        widget.setLayout(gridLayout)
        self.scroll_area.setWidget(widget)
        verticalLayout.addWidget(self.scroll_area)
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

    def computeColoumnSize(self):
        width = self.rect().width()
        numCol = width//self.minWidthOfWidgets
        return numCol if numCol > 0 else 1

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow(12)
    window.show()

    app.exec()
