"""
Deck module: Manages card decks with shuffling and filtering.
Supports standard deck operations and suit-based filtering.
"""
import random
from typing import List, Optional, Set
from card import Card, Suit, Rank

class Deck:
    """Manages a collection of playing cards"""
    
    def __init__(self):
        """Initialize empty deck"""
        self.cards: List[Card] = []
    
    def create_standard_deck(self) -> None:
        """Create a standard 52-card deck"""
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
    
    def shuffle(self) -> None:
        """Shuffle the deck randomly"""
        random.shuffle(self.cards)
    
    def filter_by_suits(self, suits: List[Suit]) -> None:
        """Keep only cards from specified suits"""
        self.cards = [card for card in self.cards if card.suit in suits]
    
    def get_cards_by_suit(self, suit: Suit) -> List[Card]:
        """Get all cards of a specific suit"""
        return [card for card in self.cards if card.suit == suit]
    
    def remove_card(self, card: Card) -> bool:
        """Remove a specific card from deck"""
        try:
            self.cards.remove(card)
            return True
        except ValueError:
            return False
    
    def draw_card(self) -> Optional[Card]:
        """Draw the top card from deck"""
        if self.is_empty():
            return None
        return self.cards.pop()
    
    def draw_cards(self, count: int) -> List[Card]:
        """Draw multiple cards from deck"""
        drawn = []
        for _ in range(min(count, len(self.cards))):
            drawn.append(self.draw_card())
        return drawn
    
    def add_card(self, card: Card) -> None:
        """Add a card to the deck"""
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """Add multiple cards to the deck"""
        self.cards.extend(cards)
    
    def is_empty(self) -> bool:
        """Check if deck is empty"""
        return len(self.cards) == 0
    
    def size(self) -> int:
        """Get number of cards in deck"""
        return len(self.cards)
    
    def contains_card(self, card: Card) -> bool:
        """Check if deck contains a specific card"""
        return any(c.suit == card.suit and c.rank == card.rank for c in self.cards)
    
    def get_suit_counts(self) -> dict:
        """Get count of cards for each suit"""
        counts = {suit: 0 for suit in Suit}
        for card in self.cards:
            counts[card.suit] += 1
        return counts
    
    def sort(self) -> None:
        """Sort deck by card rank"""
        self.cards.sort()
    
    def clear(self) -> None:
        """Remove all cards from deck"""
        self.cards.clear()
    
    def copy(self) -> 'Deck':
        """Create a copy of the deck"""
        new_deck = Deck()
        new_deck.cards = self.cards.copy()
        return new_deck
    
    def __str__(self) -> str:
        """String representation of deck"""
        return f"Deck({self.size()} cards)"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"Deck(cards={self.size()})"
