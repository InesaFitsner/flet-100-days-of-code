import os
import random
import sys
from pathlib import Path

import flet
from flet import (
    AlertDialog,
    Column,
    Container,
    Image,
    Page,
    Row,
    Text,
    TextButton,
    UserControl,
    alignment,
    border,
    border_radius,
    colors,
)


class GameProgress(UserControl):
    def __init__(self, attempts, option) -> None:
        super().__init__()
        self.attempts = attempts
        self.letters_guessed = 0
        self.attempts_failed = 0
        self.option = option
        self.lives = Text(value=f"Lives: {self.attempts}", text_align="center", size=30)
        self.img = Image(src=f"/{self.option}-0.png", height=500, fit="cover")

    def attempt_failed(self):
        self.attempts_failed = self.attempts_failed + 1
        self.lives.value = f"Lives: {self.attempts-self.attempts_failed}"
        self.img.src = f"/{self.option}-{self.attempts_failed}.png"
        self.update()

    def game_won(self):
        self.lives.value = "You won!"
        self.img.src = f"/{self.option}-you-won.png"
        self.update()

    def game_lost(self):
        self.lives.value = "You lost!"
        self.update()

    def reset(self, option):
        self.attempts_failed = 0
        self.letters_guessed = 0
        self.option = option
        self.lives.value = f"Lives: {self.attempts}"
        self.img.src = f"/{self.option}-0.png"
        self.update()

    def build(self):
        return Column(
            controls=[
                Container(content=self.lives),
                Container(content=self.img, height=500),
            ]
        )


class WordLetter(UserControl):
    def __init__(self, letter) -> None:
        super().__init__()
        self.letter = letter
        self.revealed = False

    def reveal(self):
        self.txt.visible = True
        self.cont.border = None
        self.revealed = True
        self.update()

    def build(self):
        self.txt = Text(self.letter, visible=False, size=20)
        self.cont = Container(
            content=self.txt,
            border=border.only(bottom=border.BorderSide(1, "black")),
            width=20,
            height=30,
        )
        return self.cont


def main(page: Page):
    page.title = "Hangman"
    # page.vertical_alignment = "center"

    def select_new_word():
        file_words = []
        file_path = str(
            Path(os.path.dirname(sys.argv[0])).joinpath("words.txt").resolve()
        )
        input_file = open(file_path)
        for line in input_file:
            line = line.strip()
            file_words.append(line)
        input_file.close()
        i = random.randint(0, len(file_words) - 1)
        return file_words[i]

    game_progress = GameProgress(9, "hangman")
    display_word_letters = Row()
    alphabet_letters = Row(wrap=True)

    def start_new_game():

        display_word_letters.controls.clear()
        alphabet_letters.controls.clear()

        for letter in list(select_new_word().upper()):
            display_word_letters.controls.append(WordLetter(letter))

        for letter in [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]:
            alphabet_letters.controls.append(
                Container(
                    content=Text(letter, size=20),
                    bgcolor=colors.BLUE_100,
                    padding=5,
                    border=border.all(2),
                    border_radius=border_radius.all(5),
                    on_click=letter_clicked,
                    data=letter,
                    width=30,
                    alignment=alignment.center,
                )
            )

        page.update()

    def letter_clicked(e):
        found = False
        for word_letter in display_word_letters.controls:
            if e.control.data == word_letter.letter:
                e.control.bgcolor = colors.GREEN_100
                word_letter.reveal()
                game_progress.letters_guessed = game_progress.letters_guessed + 1
                found = True

        if not found:
            game_progress.attempt_failed()
            e.control.bgcolor = colors.BLUE_GREY_100

        e.control.disabled = True

        if game_progress.letters_guessed == len(display_word_letters.controls):
            game_progress.game_won()

        if game_progress.attempts_failed > game_progress.attempts:
            game_progress.game_lost()
            for word_letter in display_word_letters.controls:
                if not word_letter.revealed:
                    word_letter.reveal()

        page.update()

    def option_clicked(e):
        start_new_game()
        game_progress.reset(e.control.data)
        dlg.open = False
        page.update()

    dlg = AlertDialog(
        modal=True,
        title=Text("Choose your animation"),
        content=Row(
            controls=[
                Container(
                    content=Image(
                        src=f"/hangman-0.png", height=60, width=80, fit="cover"
                    ),
                    # bgcolor=colors.GREEN_200,
                    padding=5,
                    border=border.all(2),
                    border_radius=border_radius.all(5),
                    on_click=option_clicked,
                    width=200,
                    height=100,
                    alignment=alignment.center,
                    data="hangman",
                ),
                Container(
                    content=Image(
                        src=f"/swordfish-0.png", height=60, width=80, fit="cover"
                    ),
                    # bgcolor=colors.BLUE_GREY_200,
                    padding=5,
                    border=border.all(2),
                    border_radius=border_radius.all(5),
                    on_click=option_clicked,
                    width=200,
                    height=100,
                    data="swordfish",
                    alignment=alignment.center,
                ),
            ]
        ),
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def new_game_clicked(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    page.dialog = dlg
    dlg.open = True

    page.add(
        Row(
            controls=[
                Column(
                    # alignment="spaceBetween",
                    spacing=200,
                    width=500,
                    controls=[
                        Container(
                            content=Text("New game", size=20),
                            # alignment=alignment.top_left,
                            # height=300,
                            width=200,
                            alignment=alignment.center,
                            on_click=new_game_clicked,
                            bgcolor=colors.BLUE_100,
                            padding=5,
                            border=border.all(2),
                            border_radius=border_radius.all(5),
                            # bgcolor=colors.AMBER_200,
                        ),
                        Container(content=display_word_letters),
                        Container(content=alphabet_letters),
                    ],
                ),
                game_progress,
            ],
        )
    )

    start_new_game()


flet.app(target=main, assets_dir="images")
