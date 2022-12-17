import flet as ft
from solitaire import Solitaire

def create_appbar(page):

    def start_new_game():
        page.controls.pop()
        new_solitaire = Solitaire(int(waste_size.value))
        page.add(new_solitaire)
        page.update()

    def new_game_clicked(e):
        start_new_game()

    def show_rules(e):
        page.dialog = rules_dialog
        rules_dialog.open = True
        page.update()

    def show_settings(e):
        page.dialog = settings_dialog
        settings_dialog.open = True
        page.update()


    def apply_settings(e):
        settings_dialog.open = False
        start_new_game()

    page.appbar = ft.AppBar(
        leading=ft.Image(src=f"/images/card.png"),
        leading_width=30,
        title=ft.Text("Flet solitaire"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.TextButton(text="New game", on_click=new_game_clicked),
            ft.TextButton(text="Rules", on_click=show_rules),
            ft.IconButton(ft.icons.SETTINGS, on_click=show_settings),
            
        ],
    )

    rules_md = ft.Markdown(
        """
    Klondike is played with a standard 52-card deck, without Jokers.

    The four foundations (light rectangles in the upper right of the figure) are built up by suit from Ace (low in this game) 
    to King, and the tableau piles can be built down by alternate colors. Every face-up card in a partial pile, or a complete pile, 
    can be moved, as a unit, to another tableau pile on the basis of its highest card. Any empty piles can be filled with a King, 
    or a pile of cards with a King. The aim of the game is to build up four stacks of cards starting with Ace and ending with King, 
    all of the same suit, on one of the four foundations, at which time the player would have won. There are different ways 
    of dealing the remainder of the deck from the stock to the waste, which can be selected in the Settings:

    - Turning three cards at once to the waste, with no limit on passes through the deck.
    - Turning three cards at once to the waste, with three passes through the deck.
    - Turning one card at a time to the waste, with three passes through the deck.
    - Turning one card at a time to the waste with only a single pass through the deck, and playing it if possible.
    - Turning one card at a time to the waste, with no limit on passes through the deck.

    If the player can no longer make any meaningful moves, the game is considered lost.
        """)

    rules_dialog = ft.AlertDialog(
        title=ft.Text("Solitaire rules"), content=rules_md, on_dismiss=lambda e: print("Dialog dismissed!")
    )

    waste_size = ft.RadioGroup(value=3, content=ft.Row(controls=[
                ft.Radio(value=1, label="One card"),
                ft.Radio(value=3, label="Three cards")
            ]))

    deck_passes_allowed = ft.RadioGroup(value="Unlimited", content=ft.Row(controls=[
                ft.Radio(value=1, label="One"),
                ft.Radio(value=3, label="Three"),
                ft.Radio(value="Unlimited", label="Unlimited"),
            ]))

    settings_dialog = ft.AlertDialog(
        title=ft.Text("Solitare Settings"), 
        content=ft.Column(controls=[
            ft.Text("Waste pile size:"),
            waste_size,
            ft.Text("Passes through the deck:"),
            deck_passes_allowed
            ], tight=True), 
        on_dismiss=apply_settings
    )
