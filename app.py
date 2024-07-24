import sys

from PyQt6.QtWidgets import QApplication

from Views.GameView import GameWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = GameWindow()
    window.show()

    app.exec()
