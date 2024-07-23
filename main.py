# Example usage
from PyQt6 import QtWidgets

from Card import Card
from Shapes import OvalWidget, RectangleWidget

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # Create some example widgets to put in the card
    oval1 = OvalWidget()
    oval2 = OvalWidget()
    rectangle1 = RectangleWidget()
    rectangle2 = RectangleWidget()
    rectangle3 = RectangleWidget()

    # Set fixed sizes for the shapes
    oval1.setFixedSize(100, 100)
    oval2.setFixedSize(100, 100)
    rectangle1.setFixedSize(100, 50)
    rectangle2.setFixedSize(100, 50)
    rectangle3.setFixedSize(100, 50)

    # Create the card widget with the example contents and an aspect ratio of 1.5
    card = Card(2/3, oval1, oval2, rectangle1, rectangle2, rectangle3)

    # Set up the main application window
    window = QtWidgets.QMainWindow()
    central_widget = QtWidgets.QWidget()
    central_layout = QtWidgets.QVBoxLayout()
    central_layout.addWidget(card)
    central_widget.setLayout(central_layout)
    window.setCentralWidget(central_widget)

    # Show the window
    window.show()
    sys.exit(app.exec())