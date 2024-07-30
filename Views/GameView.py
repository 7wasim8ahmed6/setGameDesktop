from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QVBoxLayout, QScrollArea, \
    QSpacerItem, QSizePolicy, QHBoxLayout, QLabel, QMessageBox

from ModelView import CardGame
from Views.CardView import CardView


class GameWindow(QMainWindow):
    def __init__(self, theCardGame: CardGame, minWidth=200, aspectRatio=2 / 3):
        super(GameWindow, self).__init__()
        self.setMinimumSize(1300, 1000)
        self.cardGame = theCardGame
        self.minWidthOfWidgets = minWidth
        self.aspectRat = aspectRatio
        self.card_views = []
        self._initCards()

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
        verticalLayout.addLayout(self.createTopView())
        verticalLayout.addWidget(scroll_area)
        verticalLayout.addLayout(self.createBottomView())
        self.setWindowTitle("Sets")
        self.createMenu()
        # self.showFullScreen()

    def createMenu(self):
        # Create the menu bar
        menuBar = self.menuBar()

        # Create the File menu
        fileMenu = menuBar.addMenu("File")
        newGameAction = QAction("New Game", self)
        newGameAction.setIcon(QIcon(':/icons/new'))
        newGameAction.triggered.connect(self.newGame)
        exitAction = QAction("Exit", self)
        exitAction.setIcon(QIcon(':/icons/exit'))
        exitAction.triggered.connect(self.exitGame)
        fileMenu.addAction(newGameAction)
        fileMenu.addAction(exitAction)

        # Create the Help menu
        helpMenu = menuBar.addMenu("Help")
        helpAction = QAction("Help", self)
        helpAction.setIcon(QIcon(':/icons/help'))
        helpAction.triggered.connect(self.showHelp)
        helpMenu.addAction(helpAction)

    def newGame(self):
        # Logic for starting a new game
        print("New Game started")
        # Reset the game state or implement the logic needed for a new game
        # Example: self._initCards()

    def exitGame(self):
        # Logic for exiting the game
        print("Exiting the game")
        self.close()

    def showHelp(self):
        # Show a help message box
        QMessageBox.information(self, "Help",
                                "This is the help information for the game.This is the help information for the game.This is the help information for the game.")

    def createBottomView(self):
        horLayout = QHBoxLayout()
        horLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        pushButton = QPushButton("Hint?")
        horLayout.addWidget(pushButton)
        pushButton = QPushButton("Draw Cards")
        horLayout.addWidget(pushButton)
        return horLayout

    def createTopView(self):
        horLayout = QHBoxLayout()

        # Points label
        lblPoints = QLabel("Score: ")
        self.pointsValue = QLabel("0")  # Placeholder for the points
        horLayout.addWidget(lblPoints)
        horLayout.addWidget(self.pointsValue)

        # Spacer
        horLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Time label
        lblTime = QLabel("Time: ")
        self.timeValue = QLabel("00:00")  # Placeholder for the timer
        horLayout.addWidget(lblTime)
        horLayout.addWidget(self.timeValue)
        return horLayout

    def _initCards(self):
        for card in self.cardGame.get_draw_cards():
            theCardView = CardView(card)
            theCardView.setMinimumWidth(self.minWidthOfWidgets)
            theCardView.setMinimumHeight(int(self.minWidthOfWidgets // self.aspectRat))
            theCardView.onTapGesture.connect(self.onCustomSignalEmitted)
            self.card_views.append(theCardView)

    def onCustomSignalEmitted(self, card: CardView):
        print("Card clicked")


    def addButtons(self):
        maxCol = self.computeColoumnSize()
        row = 0
        widgetsPlaced = 0
        while widgetsPlaced < len(self.card_views):
            for col in range(maxCol):
                self.gridLayout.addWidget(self.card_views[widgetsPlaced], row, col)
                widgetsPlaced += 1
                if widgetsPlaced >= len(self.card_views):
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
                # child.widget().deleteLater()
                self.gridLayout.removeWidget(child.widget())

        # Add the buttons again
        self.addButtons()
