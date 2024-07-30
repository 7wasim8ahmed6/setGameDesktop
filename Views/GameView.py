from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QVBoxLayout, QScrollArea, \
    QSpacerItem, QSizePolicy, QHBoxLayout, QLabel, QMessageBox

from ModelView import CardGame
from Views.CardView import CardView
from common.Observer import Observer


class GameWindow(QMainWindow, Observer):
    def __init__(self, the_card_game: CardGame, min_width=200, aspect_ratio=2 / 3):
        QMainWindow.__init__(self, parent=None)  # Initialize QMainWindow with GameWindow as parent
        Observer.__init__(self)  # Initialize Observer without any arguments
        self.setMinimumSize(1300, 1000)
        self.cardGame = the_card_game
        self.minWidthOfWidgets = min_width
        self.aspectRat = aspect_ratio
        self.cardGame.add_observer(self)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        vertical_layout = QVBoxLayout(self.central_widget)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(1)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.reinsert_card_views()
        widget = QWidget()
        widget.setLayout(self.gridLayout)
        scroll_area.setWidget(widget)
        vertical_layout.addLayout(self.createTopView())
        vertical_layout.addWidget(scroll_area)
        vertical_layout.addLayout(self.createBottomView())
        self.setWindowTitle("Sets")
        self.createMenu()
        # self.showFullScreen()

    def update(self, observable, *args, **kwargs):
        self.rearrangeButtons()
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
        pushButton.clicked.connect(self.on_hint_clicked)
        horLayout.addWidget(pushButton)
        pushButton = QPushButton("Draw Cards")
        pushButton.clicked.connect(self.on_draw_cards_clicked)
        horLayout.addWidget(pushButton)
        return horLayout

    def on_draw_cards_clicked(self):
        print("on_draw_cards_clicked pressed")
        self.cardGame.draw_cards()


    def on_hint_clicked(self):
        print("on_hint_clicked pressed")

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

    def onCustomSignalEmitted(self, card_view: CardView):
        self.cardGame.choose(card_view.card)


    def reinsert_card_views(self):
        card_views = []
        for card in self.cardGame.get_draw_cards():
            is_selected = self.cardGame.isCardSelected(card)
            is_matched = self.cardGame.isCardMatched(card)
            theCardView = CardView(card, self.minWidthOfWidgets,
                                   int(self.minWidthOfWidgets // self.aspectRat), None,  is_selected, is_matched)
            theCardView.onTapGesture.connect(self.onCustomSignalEmitted)
            card_views.append(theCardView)

        maxCol = self.computeColoumnSize()
        row = 0
        widgetsPlaced = 0
        while widgetsPlaced < len(card_views):
            for col in range(maxCol):
                self.gridLayout.addWidget(card_views[widgetsPlaced], row, col)
                widgetsPlaced += 1
                if widgetsPlaced >= len(card_views):
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
        self.reinsert_card_views()
