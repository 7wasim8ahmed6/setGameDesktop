from itertools import product
from random import shuffle

from Model.Card import *


class GamePlay:
    def __init__(self):
        self.__cards: list[Card] = GamePlay.__createAllCards()
        shuffle(self.__cards)
        self.__draw_cards: list[Card] = self.__cards[-12:]  # Take the last 12 cards
        self.__cards = self.__cards[:-12]  # Remove the last 12 cards from __cards
        self.__matched: list[Card] = []
        self.__selected: list[Card] = []

    @staticmethod
    def __createAllCards() -> [Card]:
        shapes = list(Shape)
        numbers = list(Numbers)
        fillings = list(Filling)
        colors = list(Color)

        return [
            Card(shape=shape, number=number, filling=filling, color=color, id=idx)
            for idx, (shape, number, filling, color) in enumerate(product(shapes, numbers, fillings, colors), start=1)
        ]

    def get_drawn_cards(self) -> [Card]:
        return self.__draw_cards

    def get_selected_cards(self) -> [Card]:
        return self.__selected

    def get_matched_cards(self) -> [Card]:
        return self.__matched