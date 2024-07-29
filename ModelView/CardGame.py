from typing import List

from Model.GamePlay import GamePlay
from Views.CardViewV2 import CardViewV2
from common.Card import Card


class CardGame:
    def __init__(self):
        self.__theGame = GamePlay()

    def get_draw_cards(self) -> List[CardViewV2]:
        card_view_list = []
        for card in self.__theGame.get_drawn_cards():

            card_view_list.append(CardViewV2(card, None, self.__theGame.is_card_chosen(card),
                                             self.__theGame.is_card_matched(card)))

        return card_view_list
    def make_draw_get_cards(self) -> List[CardViewV2]:
        self.__theGame.draw_cards()
        return self.get_draw_cards()


