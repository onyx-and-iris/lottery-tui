import random
from abc import ABC, abstractmethod
from typing import NamedTuple


class Result(NamedTuple):
    """A named tuple to hold the results of a lottery draw."""

    kind: str
    numbers: list[int]
    bonus: list[int] | None

    def __str__(self) -> str:
        """Return a string representation of the lottery result."""
        out = f'Numbers: {", ".join(str(n) for n in sorted(self.numbers))}'
        if self.bonus:
            match self.kind:
                case 'EuroMillions':
                    bonus_name = 'Lucky Stars'
                case 'SetForLife':
                    bonus_name = 'Life Ball'
                case 'Thunderball':
                    bonus_name = 'Thunderball'
                case _:
                    bonus_name = 'Bonus Numbers'
            out += f'\n{bonus_name}: {", ".join(str(n) for n in sorted(self.bonus))}'
        return out


registry = {}


def register_lottery(cls):
    """A decorator to register lottery classes in the registry."""
    registry[cls.__name__.lower()] = cls
    return cls


class Lottery(ABC):
    """An abstract base class for different types of lotteries."""

    @abstractmethod
    def draw(self) -> Result:
        """Perform a lottery draw."""


@register_lottery
class Lotto(Lottery):
    """A class representing the Lotto lottery.

    Lotto draws 6 numbers from a pool of 1 to 59, without replacement.
    There is no bonus number in Lotto.
    """

    POSSIBLE_NUMBERS = range(1, 60)

    def draw(self) -> Result:
        """Perform a Lotto draw."""
        result = random.sample(Lotto.POSSIBLE_NUMBERS, 6)
        return Result(kind=type(self).__name__, numbers=result, bonus=None)


@register_lottery
class EuroMillions(Lottery):
    """A class representing the EuroMillions lottery.

    EuroMillions draws 5 numbers from a pool of 1 to 50, without replacement,
    and 2 "Lucky Star" numbers from a separate pool of 1 to 12, also without replacement.
    """

    POSSIBLE_NUMBERS = range(1, 51)
    POSSIBLE_BONUS_NUMBERS = range(1, 13)

    def draw(self) -> Result:
        """Perform a EuroMillions draw."""
        numbers = random.sample(EuroMillions.POSSIBLE_NUMBERS, 5)
        bonus = random.sample(EuroMillions.POSSIBLE_BONUS_NUMBERS, 2)
        return Result(kind=type(self).__name__, numbers=numbers, bonus=bonus)


@register_lottery
class SetForLife(Lottery):
    """A class representing the Set For Life lottery.

    Set For Life draws 5 numbers from a pool of 1 to 39, without replacement,
    and 1 "Life Ball" number from a separate pool of 1 to 10.
    """

    POSSIBLE_NUMBERS = range(1, 40)

    def draw(self) -> Result:
        """Perform a Set For Life draw."""
        numbers = random.sample(SetForLife.POSSIBLE_NUMBERS, 5)
        life_ball = [random.randint(1, 10)]
        return Result(kind=type(self).__name__, numbers=numbers, bonus=life_ball)


@register_lottery
class Thunderball(Lottery):
    """A class representing the Thunderball lottery.

    Thunderball draws 5 numbers from a pool of 1 to 39, without replacement,
    and 1 "Thunderball" number from a separate pool of 1 to 14.
    """

    POSSIBLE_NUMBERS = range(1, 40)

    def draw(self) -> Result:
        """Perform a Thunderball draw."""
        numbers = random.sample(Thunderball.POSSIBLE_NUMBERS, 5)
        thunderball = [random.randint(1, 14)]
        return Result(kind=type(self).__name__, numbers=numbers, bonus=thunderball)


def request_lottery_obj(lottery_name: str) -> Lottery:
    """Return a lottery object based on the provided lottery name."""
    lottery_cls = registry.get(lottery_name.lower())
    if lottery_cls is None:
        raise ValueError(f"Lottery '{lottery_name}' not found.")
    return lottery_cls()
