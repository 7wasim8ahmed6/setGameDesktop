from itertools import product
from random import shuffle
from typing import Tuple, List, Optional

from common.Card import *
from Model.Score import Score


class GamePlay:
    def __init__(self):
        self.__cards = GamePlay.__createAllCards()
        shuffle(self.__cards)
        self.__draw_cards: List[Card] = self.__cards[-12:]  # Take the last 12 cards
        self.__cards: List[Card] = self.__cards[:-12]  # Remove the last 12 cards from __cards
        self.__matched: List[Card] = []
        self.__selected: List[Card] = []
        self.__game_completed = False
        self.__score = Score()
        self.__score.start_timer()

    @staticmethod
    def __createAllCards() -> List[Card]:
        shapes = list(Shape)
        numbers = list(Numbers)
        fillings = list(Filling)
        colors = list(Color)

        return [
            Card(shape=shape, number=number, filling=filling, color=color, id=idx)
            for idx, (shape, number, filling, color) in enumerate(product(shapes, numbers, fillings, colors), start=1)
        ]

    def get_drawn_cards(self) -> List[Card]:
        return self.__draw_cards

    def draw_cards(self):
        if len(self.__cards) >= 3:
            isSetAvailable, _ = self.has_set_available()
            if isSetAvailable:
                self.__score.deduct()
                if len(self.__selected) == 3:
                    self.__choice_full_replace_drawn_cards()
                else:
                    self.__draw_cards = self.__cards[-3:]  # Take the last 3 cards
                    self.__cards = self.__cards[:-3]  # Remove the last 3 cards from __cards

    def choose(self, card: Card):
        select_index = self.__find_in_drawn(card)
        if not select_index:
            print("selected card not in drawn cards")
            return

        if self.__is_card_matched(card):
            print("Matched card selected")
            return

        self.__choice_full_replace_drawn_cards()
        self.__add_or_remove_choice(card)
        if self.__make_match():
            self.__score.add_corrected_points()
            print(f"{self.__selected[0]},{self.__selected[1]} and {self.__selected[2]} make match")
            if len(self.__draw_cards) == 3:
                self.__game_completed = True
        else:
            self.__score.deduct()
            print(f"{self.__selected[0]},{self.__selected[1]} and {self.__selected[2]} make  no match")

    def is_game_completed(self):
        return self.__game_completed

    def __make_match(self, card_a: Card, card_b: Card, card_c: Card) -> bool:
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

    def __make_match(self) -> bool:
        if len(self.__selected) != 3:
            return False

        if self.__make_match(self.__selected[0], self.__selected[1], self.__selected[2]):
            self.__matched.append(self.__selected[0])
            self.__matched.append(self.__selected[1])
            self.__matched.append(self.__selected[2])
            return True

        return False

    def __is_card_matched(self, card: Card) -> bool:
        for _, match_card in enumerate(self.__matched):
            if match_card.id == card.id:
                return True

        return False

    def __find_in_drawn(self, card) -> Optional[int]:
        for index, drawn_card in enumerate(self.__draw_cards):
            if drawn_card.id == card.id:
                return index
        return None

    def __choice_full_replace_drawn_cards(self):
        if len(self.__selected) != 3:
            return

        if self.__is_card_matched(self.__selected[0]):
            for card in self.__selected:
                index_in_drawn = self.__find_in_drawn(card)
                if index_in_drawn is not None:
                    if self.__cards:
                        new_card = self.__cards.pop()
                        self.__draw_cards[index_in_drawn] = new_card
                    else:
                        self.__draw_cards.pop(index_in_drawn)

            self.__selected.clear()
            self.__matched.clear()

    def has_set_available(self) -> Tuple[bool, List[Card]]:
        size = len(self.__draw_cards)

        if size < 3:
            return False, []

        for i in range(size):
            for j in range(i + 1, size):
                for k in range(j + 1, size):
                    card1 = self.__draw_cards[i]
                    card2 = self.__draw_cards[j]
                    card3 = self.__draw_cards[k]

                    # Skip cards that are already in __matched
                    if any(matched_card.id in [card1.id, card2.id, card3.id] for matched_card in self.__matched):
                        continue

                    if self.__make_match(card1, card2, card3):
                        return True, [card1, card2, card3]

        return False, []

    def provide_hint(self) -> Optional[Card]:
        set_available, hint_cards = self.has_set_available()
        if set_available and hint_cards:
            self.__score.deduct()
            return hint_cards[0]  # Return the first card in the found set
        return None

    # def _is_matched_card_selected(self, selected_index: int) -> bool:
    #     return any(matched_card.id == self.__draw_cards[selected_index].id for matched_card in self.__matched)

    def __add_or_remove_choice(self, card: Card):
        index = next((i for i, c in enumerate(self.__selected) if c.id == card.id), None)
        if index is not None:
            self.__selected.pop(index)
        else:
            self.__selected.append(card)
