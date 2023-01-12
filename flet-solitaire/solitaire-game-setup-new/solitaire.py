#CARD_OFFSET = 20
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
        #self.start_top = 0
        #self.start_left = 0
        self.controls = []
        self.slots = []
        #self.card_offset = CARD_OFFSET
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT

    # def did_mount(self):
    #     self.create_slots()
    #     self.create_card_deck()

    # def create_slots(self):
    #     self.slots.append(Slot(top=0, left=200))
    #     self.slots.append(Slot(top=0, left=300))
    #     self.controls.extend(self.slots)
    #     self.update()

    # def create_card_deck(self):
    #     card1 = Card(self, color="GREEN", top=0, left=0)
    #     card2 = Card(self, color="YELLOW", top=0, left=100)
    #     cards = [card1, card2]
    #     self.controls.extend(cards)
    #     self.update()

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
        # card1 = Card(self, color="GREEN")
        # card2 = Card(self, color="YELLOW")
        # self.cards = [card1, card2]
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
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))

    def create_slots(self):
        # self.slots.append(Slot(top=0, left=0))
        # self.slots.append(Slot(top=0, left=200))
        # self.slots.append(Slot(top=0, left=300))
        # self.controls.extend(self.slots)
        # self.update()
        self.stock = Slot(top=0, left=0, border=ft.border.all(1))

        self.waste = Slot(top=0, left=100, border=None)

        self.foundations = []
        x = 300
        for i in range(4):
            self.foundations.append(Slot(top=0, left=x, border=ft.border.all(1, "outline")))
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(Slot(top=150, left=x, border=None))
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.update()

    def deal_cards(self):
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        #for card in self.cards:
            #card.place(self.stock)
        self.cards[0].place(self.stock)
        self.update()

    # def move_on_top(self, draggable_pile):
    #     """Brings draggable card pile to the top of the stack"""

    #     for card in draggable_pile:
    #         self.controls.remove(card)
    #         self.controls.append(card)
    #     self.update()
    
    # def bounce_back(self, draggable_pile):
    #     """Returns draggable pile to its original position"""
    #     for card in draggable_pile:
    #         card.top = self.start_top + draggable_pile.index(card) * self.card_offset
    #         card.left = self.start_left
 
    #     self.update()