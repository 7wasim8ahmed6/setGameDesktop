from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class Card(QtWidgets.QWidget):
    def __init__(self, aspect_ratio: float, *contents):
        super().__init__()

        # Store the aspect ratio
        self.aspect_ratio = aspect_ratio
        self.contents = contents

        # Set up the main layout for the card
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add each content widget to the layout
        for content in contents:
            self.layout.addWidget(content)

        # Set the layout for the widget
        self.setLayout(self.layout)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        # Calculate the new size based on the aspect ratio
        width = event.size().width()
        height = int(width / self.aspect_ratio)
        # self.setFixedSize(width, height)

        # Calculate the spacing to evenly distribute the items
        num_contents = len(self.contents)
        if num_contents > 1:
            total_content_height = sum(content.sizeHint().height() for content in self.contents)
            remaining_space = height - total_content_height
            spacing = remaining_space // (num_contents + 1)
            self.layout.setSpacing(spacing)
        else:
            self.layout.setSpacing(0)

        super().resizeEvent(event)
