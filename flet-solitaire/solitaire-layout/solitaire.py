CARD_OFFSET = 20
SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import flet as ft
from slot import Slot
from card import Card
import random

class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value

class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.start_top = 0
        self.start_left = 0
        self.controls = []
        self.slots = []
        self.card_offset = CARD_OFFSET
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()

    def create_slots(self):
        # stock 
        self.slots.append(Slot(top=0, left=0))
        
        # waste
        self.slots.append(Slot(top=0, left=100))
        
        # foundation
        slot_left = 300
        for slot in range(4):
            self.slots.append(
                Slot(
                    top=0,
                    left=slot_left,
                )
            )
            slot_left += 100
        
        #tableau
        slot_left = 0
        for slot in range(7):
            self.slots.append(
                Slot(
                    top=150,
                    left=slot_left,

                )
            )
            slot_left += 100


        self.controls.extend(self.slots)
        self.update()

    def create_card_deck(self):
        suites = [
            Suite("Hearts", "RED"),
            Suite("Diamonds", "RED"),
            Suite("Clubs", "BLACK"),
            Suite("Spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                file_name = f"{rank.name}_{suite.name}.svg"
                #print(file_name)
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank, top=0, left=0))
        
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        print(len(self.cards))
        self.update()
        

    def move_on_top(self, draggable_pile):
        """Brings draggable card pile to the top of the stack"""

        for card in draggable_pile:
            self.controls.remove(card)
            self.controls.append(card)
        self.update()
    
    def bounce_back(self, draggable_pile):
        """Returns draggable pile to its original position"""
        for card in draggable_pile:
            card.top = self.start_top + draggable_pile.index(card) * self.card_offset
            card.left = self.start_left
        self.update()