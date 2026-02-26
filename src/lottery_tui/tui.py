from typing import NoReturn

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.types import SelectType
from textual.widgets import Button, Label, Select, Static

from .lottery import request_lottery_obj


class LotteryTUI(App):
    """A Textual TUI for the Lottery application."""

    CSS_PATH = 'tui.tcss'

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(
            Static('Welcome to the Lottery TUI!', id='welcome'),
            Static('Pick a lottery to play:', id='instructions'),
            Select(
                options=[
                    ('Lotto', 'lotto'),
                    ('EuroMillions', 'euromillions'),
                    ('Set For Life', 'setforlife'),
                    ('Thunderball', 'thunderball'),
                ],
                value='lotto',
                allow_blank=False,
                id='lottery-select',
            ),
            Button('Draw', id='draw-button'),
            Label('', id='result-label'),
            id='main-container',
        )

    def on_key(self, event: Key) -> NoReturn:
        """Handle key events."""
        if event.key == 'q':
            self.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == 'draw-button':
            self._draw_button_handler()

    def _draw_button_handler(self) -> None:
        """Handle the draw button press."""
        lottery_obj = request_lottery_obj(self._read_lottery_selection())
        result = lottery_obj.draw()
        self._update_result_label(str(result))

    def _read_lottery_selection(self) -> SelectType:
        """Read the selected lottery from the dropdown."""
        return self.query_one('#lottery-select').value

    def _update_result_label(self, message: str) -> None:
        """Update the result label with a new message."""
        self.query_one('#result-label').update(message)


def main():
    """Entry point for the Lottery TUI."""
    app = LotteryTUI()
    app.run()
