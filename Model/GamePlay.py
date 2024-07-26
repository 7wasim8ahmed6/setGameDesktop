from itertools import product
from random import shuffle

from Model.Card import *


class GamePlay:
    def __init__(self):
        self.__cards = GamePlay.__createAllCards()
        shuffle(self.__cards)
        self.__draw_cards = self.__cards[-12:]  # Take the last 12 cards
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

    def draw_cards(self):
        if self.__cards:
            self.__draw_cards = self.__cards[-3:]  # Take the last 3 cards
            self.__cards = self.__cards[:-3]  # Remove the last 3 cards from __cards

    def choose(self, card: Card):
        pass

    def makeMatch(self, card_a: Card, card_b: Card, card_c: Card) -> bool:
        # Check if all three cards are different
        if card_a.id == card_b.id or card_b.id == card_c.id or card_c.id == card_a.id:
            return False

        # Check if all attributes are either all the same or all different
        attributes = ['shape', 'color', 'filling', 'number']
        for attr in attributes:
            values = {getattr(card_a, attr), getattr(card_b, attr), getattr(card_c, attr)}
            if len(values) == 2:  # If there are exactly two different values, it's not a match
                return False

        return True
