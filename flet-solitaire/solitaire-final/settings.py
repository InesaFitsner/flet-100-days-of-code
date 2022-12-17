import flet as ft

class Settings:
    def __init__(self, waste_size=3, deck_passes_allowed="Unlimited", card_back=f"/images/card_back0.png"):
        self.waste_size = waste_size
        self.deck_passes_allowed = deck_passes_allowed
        self.card_back = card_back


class Settings_dialog(ft.AlertDialog):
    def __init__(self):
        pass



