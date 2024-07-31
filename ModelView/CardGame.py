from typing import List

from Model.GamePlay import GamePlay
from Views.CardView import CardView
from common.Card import Card
from common.Observable import Observable


class CardGame(Observable):
    def __init__(self):
        super().__init__()
        self.__theGame = GamePlay()

    def get_draw_cards(self) -> List[Card]:
        return self.__theGame.get_drawn_cards()

    def isCardSelected(self, card: Card):
        return self.__theGame.is_card_chosen(card)

    def isCardMatched(self, card: Card):
        return self.__theGame.is_card_matched(card)

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