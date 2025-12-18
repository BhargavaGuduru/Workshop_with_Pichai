"""
Card module: Defines playing cards with suits and ranks.
Supports comparison operations and value calculations.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Union

class Suit(Enum):
    """Playing card suits with unicode symbols"""
    HEARTS = "♥"
    CLUBS = "♣" 
    DIAMONDS = "♦"
    SPADES = "♠"

class Rank(Enum):
    """Card ranks with numeric values for comparison"""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

@dataclass
class Card:
    """Represents a single playing card"""
    suit: Suit
    rank: Rank
    
    def __post_init__(self):
        """Initialize derived properties"""
        self.value = self.rank.value
    
    def __gt__(self, other: 'Card') -> bool:
        """Compare cards by rank"""
        return self.value > other.value
    
    def __eq__(self, other: 'Card') -> bool:
        """Check if cards have equal rank"""
        return self.value == other.value
    
    def __lt__(self, other: 'Card') -> bool:
        """Check if this card is lower than another"""
        return self.value < other.value
    
    def get_numeric_value(self) -> int:
        """Get numeric value of the card"""
        return self.value
    
    def __str__(self) -> str:
        """String representation of card"""
        return f"{self.rank.name}{self.suit.value}"
    
    def __repr__(self) -> str:
        """Developer representation of card"""
        return f"Card({self.suit.name}, {self.rank.name})"
