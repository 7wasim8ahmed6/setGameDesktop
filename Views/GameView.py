
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QVBoxLayout, QScrollArea, \
    QSpacerItem, QSizePolicy, QHBoxLayout

from Views.CardView import CardView


class GameWindow(QMainWindow):
    def __init__(self, numberOfWidgets=12, minWidth=180, aspectRatio=2 / 3):
        super(GameWindow, self).__init__()
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
                Card = CardView()
                Card.setMinimumWidth(self.minWidthOfWidgets)
                Card.setMinimumHeight(int(self.minWidthOfWidgets // self.aspectRat))
                self.gridLayout.addWidget(Card, row, col)
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
        super(GameWindow, self).resizeEvent(event)
        self.rearrangeButtons()

    def rearrangeButtons(self):
        # Remove all existing widgets from the layout
        while self.gridLayout.count():
            child = self.gridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add the buttons again
        self.addButtons()
