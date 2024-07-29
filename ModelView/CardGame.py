from typing import List

from Model.GamePlay import GamePlay
from Views.CardViewV2 import CardViewV2
from common.Card import Card


class CardGame:
    def __init__(self):
        self.__theGame = GamePlay()

    def get_draw_cards(self) -> List[Card]:
        return self.__theGame.get_drawn_cards()

    def isCardSelected(self, card: Card):
        return self.__theGame.is_card_chosen(card)

    def isCardMatched(self, card: Card):
        return self.__theGame.is_card_matched(card)