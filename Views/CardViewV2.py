from typing import Optional

from PySide6.QtWidgets import QWidget

from common.Card import *


class CardViewV2(QWidget):
    def __init__(self, card: Card, parent: Optional[QWidget] = None, isSelected=False, isMatched=False):
        super().__init__(parent)
        self.card = card
        self.is_selected = isSelected
        self.is_matched = isMatched
