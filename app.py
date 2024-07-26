import sys

from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication
from resources import resources_rc
# pyside6-rcc resources.qrc -o resources_rc.py for compiling resource file

from Views.GameView import GameWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    qrc_path = ":/stylesheets/light_theme.qss"
    resource_file = QFile(qrc_path)
    if resource_file.open(QFile.ReadOnly | QFile.Text):
        stylesheet = resource_file.readAll().data().decode()
        app.setStyleSheet(stylesheet)
    else:
        print(f"Failed to load resource from {qrc_path}")

    window = GameWindow()
    window.show()

    app.exec()
