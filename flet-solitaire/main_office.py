import logging
import random

import flet as ft

# This prototype is move slot and card creating and dealing to a class

# logging.basicConfig(level=logging.DEBUG)


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
        self.width = 1000
        self.height = 500
        self.current_top = 0
        self.current_left = 0
        self.card_offset = 20
        self.waste_size = 3
        self.deck_passes_allowed = 3
        self.deck_passes_remaining = 3
        self.controls = []

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()
        self.deal_cards()

    def create_slots(self):
        # self.slots = []

        self.stock = slot(
            solitaire=self, slot_type="stock", top=0, left=0, border=ft.border.all(1)
        )

        self.waste = slot(
            solitaire=self, slot_type="waste", top=0, left=100, border=None
        )

        self.foundation = []
        x = 300
        for i in range(4):
            self.foundation.append(
                slot(
                    solitaire=self,
                    slot_type="foundation",
                    top=0,
                    left=x,
                    border=ft.border.all(1),
                )
            )
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(
                slot(
                    solitaire=self,
                    slot_type="tableau",
                    top=150,
                    left=x,
                    border=ft.border.all(1),
                )
            )
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundation)
        self.controls.extend(self.tableau)
        self.update()

    def create_card_deck(self):
        suites = [
            Suite("Hearts", "RED"),
            Suite("Diamonds", "RED"),
            Suite("Clubs", "BLACK"),
            Suite("Spades", "BLACK"),
        ]
        # colors = ["BLUE", "YELLOW", "GREEN", "RED"]
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
        # self.stock = self.cards
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        self.update()

    def deal_cards(self):
        # Tableau
        card_index = 0
        first_slot = 0
        while card_index <= 27:
            for slot_index in range(first_slot, len(self.tableau)):
                self.cards[card_index].place(self.tableau[slot_index])
                card_index += 1
            first_slot += 1

        # Reveal top cards in slot piles:
        for number in range(len(self.tableau)):
            self.tableau[number].pile[-1].turn_face_up()

        # Stock pile
        for i in range(28, len(self.cards)):
            self.cards[i].place(self.stock)
            print(f"Stock card {self.cards[i].rank.name}")

    def move_on_top(self, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            self.controls.remove(card)
            self.controls.append(card)
        self.update()
    
    
    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.slot.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1

    def display_waste(self):
        for card in self.waste.pile:
            card.visible = False
        visible_cards_number = min(self.waste_size, len(self.waste.pile))
        for i in range(visible_cards_number):
            self.waste.pile[
                len(self.waste.pile) - i - 1
            ].left = self.waste.left + self.card_offset * (visible_cards_number - i - 1)
            self.waste.pile[len(self.waste.pile) - i - 1].visible = True
            print(
                f"waste card number {len(self.waste.pile)-i-1}, offset = {self.card_offset * (visible_cards_number - i - 1)}"
            )
        self.update()

    def restart_stock(self):
        self.waste.pile.reverse()
        print(len(self.waste.pile))
        print(self.waste.pile[0].rank.name)
        # for card in self.waste.pile:
        #     print(f"card {self.waste.pile.index(card)} name {card.rank.name}")
        #     card.turn_face_down()
        #     card.place(self.stock)
        while len(self.waste.pile) > 0:
            print(f"First card {self.waste.pile[0].rank.name}")
            card = self.waste.pile[0]
            card.turn_face_down()
            card.place(self.stock)
            #self.move_on_top([card])
            #self.stock.pile[-1].move_on_top(self.controls, [self.stock.pile[-1]])
        
        self.update

    def check_foundation_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.name == top_card.suite.name
                and current_card.rank.value - top_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "Ace"

    def check_tableau_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.color != top_card.suite.color
                and top_card.rank.value - current_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "King"


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()
        self.solitaire = solitaire
        #self.controls = solitaire.controls
        self.suite = suite
        self.rank = rank
        self.face_up = False
        self.slot = None

        self.mouse_cursor = ft.MouseCursor.MOVE
        # self.visible = False
        self.drag_interval = 5
        self.on_pan_update = self.drag
        self.on_pan_start = self.start_drag
        self.on_pan_end = self.drop
        self.on_tap = self.click
        self.on_double_tap = self.doubleclick
        self.content = ft.Container(
            width=65,
            height=100,
            border_radius=ft.border_radius.all(6),
            border=ft.border.all(2),
            bgcolor="GREEN",
            content=ft.Text(f"{rank.name} of {suite.name}", size=8, color=suite.color),
        )

    def turn_face_up(self):
        self.face_up = True
        self.content.bgcolor = "WHITE"
        self.update()

    
    def turn_face_down(self):
        self.face_up = False
        self.content.bgcolor = "GREEN"
        self.update()
    

    # def move_on_top(self, controls, cards_to_drag):
    #     """Brings draggable card pile to the top of the stack"""

    #     for card in cards_to_drag:
    #         controls.remove(card)
    #         controls.append(card)
    #     self.page.update()

    def start_drag(self, e: ft.DragStartEvent):
        if e.control.face_up:
            cards_to_drag = self.get_partial_pile()
            #self.move_on_top(self.controls, cards_to_drag)
            self.solitaire.move_on_top(cards_to_drag)
            # remember card original position to return it back if needed
            self.solitaire.current_top = e.control.top
            self.solitaire.current_left = e.control.left
            # self.page.update()

    def drag(self, e: ft.DragUpdateEvent):
        if e.control.face_up:
            i = 0
            for card in self.get_partial_pile():
                card.top = max(0, self.top + e.delta_y)
                if card.slot.type == "tableau":
                    card.top += i * self.solitaire.card_offset
                card.left = max(0, self.left + e.delta_x)
                i += 1
                card.update()

    def drop(self, e: ft.DragEndEvent):
        if e.control.face_up:
            cards_to_drag = self.get_partial_pile()
            slots = self.solitaire.tableau + self.solitaire.foundation
            # check if card is close to any of the tableau slots
            for slot in slots:
                # compare with top and left position of the upper card in the slot pile
                if (
                    abs(self.top - slot.upper_card_top()) < 40
                    and abs(self.left - slot.left) < 40
                ):
                    # tableau slot
                    # place cards_to_drag to the slot in proximity, if:
                    # *** For tableau slots: if cards' color is different or slot is empty
                    # *** For foundation slots: [TBD]
                    if (
                        slot.type == "tableau"
                        and self.solitaire.check_tableau_rules(
                            self, slot.get_top_card()
                        )
                        # (
                        #     len(slot.pile) == 0
                        #     or (
                        #         len(slot.pile) != 0
                        #         and self.suite.color != slot.pile[-1].suite.color
                        #     )
                        # )
                    ) or (
                        slot.type == "foundation"
                        and len(cards_to_drag) == 1
                        and self.solitaire.check_foundation_rules(
                            self, slot.get_top_card()
                        )
                    ):

                        old_slot = self.slot
                        for card in cards_to_drag:
                            card.place(slot)
                        # reveal top card in old tableau slot if exists
                        if len(old_slot.pile) > 0 and old_slot.type == "tableau":
                            old_slot.get_top_card().turn_face_up()
                        self.solitaire.display_waste()
                        self.page.update()

                        return

            # return card to original position
            self.solitaire.bounce_back(cards_to_drag)
            self.page.update()

    def doubleclick(self, e):
        if self.slot.type in ("waste", "tableau"):
            if self.face_up:
                #self.move_on_top(self.solitaire.controls, [self])
                self.solitaire.move_on_top([self])
                old_slot = self.slot
                for slot in self.solitaire.foundation:
                    if self.solitaire.check_foundation_rules(self, slot.get_top_card()):
                        # if True:
                        self.place(slot)
                        if len(old_slot.pile) > 0:
                            old_slot.get_top_card().turn_face_up()
                        self.solitaire.display_waste()
                        self.page.update()
                        return

    def click(self, e):
        if self.slot.type == "stock":
            print("Clicked on stock pile")
            for i in range(
                min(self.solitaire.waste_size, len(self.solitaire.stock.pile))
            ):
                top_card = self.solitaire.stock.pile[-1]
                #self.move_on_top(self.solitaire.controls, [top_card])
                #self.solitaire.move_on_top([top_card])
                top_card.place(self.solitaire.waste)
                top_card.turn_face_up()
            self.solitaire.display_waste()
            self.page.update()

    def place(self, slot):
        self.top = slot.top
        self.left = slot.left
        if slot.type == "tableau":
            self.top += self.solitaire.card_offset * len(slot.pile)

        # remove the card form the old slot's pile if exists

        if self.slot is not None:
            # if self.slot.type == 'waste':
            #    self.solitaire.update_waste()
            self.slot.pile.remove(self)

        # set card's slot as new slot
        self.slot = slot

        # add the card to the new slot's pile
        slot.pile.append(self)
        self.solitaire.move_on_top([self])
        self.update()

    def get_partial_pile(self):
        """returns list of cards that will be dragged together, starting with the current card"""
        partial_pile = []

        if self.slot is not None:
            card_index = self.slot.pile.index(self)

            for card in self.slot.pile:
                if self.slot.pile.index(card) >= card_index:
                    partial_pile.append(card)

        return partial_pile


class slot(ft.Container):
    def __init__(self, solitaire, slot_type, top, left, border):
        super().__init__()
        self.solitaire = solitaire
        self.pile = []
        self.type = slot_type
        self.width = 65
        self.height = 100
        self.left = left
        self.top = top
        self.border_radius = ft.border_radius.all(6)
        self.border = border
        self.on_click = self.click

    def get_top_card(self):
        if len(self.pile) > 0:
            return self.pile[-1]

    def upper_card_top(self):
        if self.type == "tableau":
            if len(self.pile) > 1:
                return self.top + self.solitaire.card_offset * (len(self.pile) - 1)
        return self.top

    def click(self, e):
        if self.type == "stock":
            print(f"Restart stock pile. Stock pile {len(self.solitaire.stock.pile)}")
            self.solitaire.restart_stock()


def main(page: ft.Page):

    solitaire = Solitaire()

    page.add(solitaire)


ft.app(target=main)
