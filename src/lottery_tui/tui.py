from loguru import logger
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container
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
                    ('UK Lotto', 'uklotto'),
                    ('EuroMillions', 'euromillions'),
                    ('Set For Life', 'setforlife'),
                    ('Thunderball', 'thunderball'),
                ],
                id='lottery-select',
            ),
            Button('Draw', id='draw-button'),
            Label('', id='result-label'),
            id='main-container',
        )

    def on_key(self, event):
        """Handle key events."""
        if event.key == 'q':
            self.exit()

    def on_button_pressed(self, event):
        """Handle button press events."""
        if event.button.id == 'draw-button':
            self._draw_button_handler()

    def _draw_button_handler(self):
        """Handle the draw button press."""
        if self.query_one('#lottery-select').is_blank():
            self._update_result_label(
                Text('Please select a lottery before drawing.', style='bold #ff8c42')
            )
            return

        selected_lottery = self.query_one('#lottery-select').value

        try:
            lottery_obj = request_lottery_obj(selected_lottery)
        except ValueError:
            ERR_MSG = f'Invalid lottery selection: {selected_lottery}'
            logger.exception(ERR_MSG)
            raise

        result = lottery_obj.draw()
        self._update_result_label(str(result))

    def _update_result_label(self, message: str):
        """Update the result label with a new message."""
        self.query_one('#result-label').update(message)


def main():
    """Entry point for the Lottery TUI."""
    app = LotteryTUI()
    app.run()
