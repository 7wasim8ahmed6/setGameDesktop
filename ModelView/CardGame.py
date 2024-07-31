from typing import List, Optional

from Model.GamePlay import GamePlay
from common.Card import Card
from common.Observable import Observable


class CardGame(Observable):
    def __init__(self):
        super().__init__()
        self.__theGame = GamePlay()
        self.hint_card: Optional[Card] = None

    def get_draw_cards(self) -> List[Card]:
        return self.__theGame.get_drawn_cards()

    def isCardSelected(self, card: Card):
        return self.__theGame.is_card_chosen(card)

    def isCardMatched(self, card: Card):
        return self.__theGame.is_card_matched(card)

    def isHint(self, card: Card):
        if self.hint_card is None:
            return False
        return card.id == self.hint_card.id

    def create_hint(self):
        self.hint_card = self.__theGame.provide_hint()
        if self.hint_card is not None:
            self.notify_observers()


    def choose(self, card):
        self.__theGame.choose(card)
        self.notify_observers()

    def draw_cards(self):
        self.__theGame.draw_cards()
        self.notify_observers()

    def get_elapsed_time(self):
        return self.__theGame.getTimeTaken()

    def getCurrentPoints(self):
        return self.__theGame.getPoints()

    def startNewGame(self):
        self.__theGame = GamePlay()
        self.notify_observers()

    def getPointsInfo(self):
        return self.__theGame.getScoreInfo()
