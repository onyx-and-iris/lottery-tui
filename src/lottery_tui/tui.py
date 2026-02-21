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
            if self.query_one('#lottery-select').is_blank():
                self.query_one('#result-label').update(
                    'Please select a lottery before drawing.'
                )
                return

            selected_lottery = self.query_one('#lottery-select').value

            try:
                lottery_obj = request_lottery_obj(selected_lottery)
                result = lottery_obj.draw()
            except ValueError as e:
                self.query_one('#result-label').update(str(e))

            self.query_one('#result-label').update(str(result))


def main():
    """Entry point for the Lottery TUI."""
    app = LotteryTUI()
    app.run()
