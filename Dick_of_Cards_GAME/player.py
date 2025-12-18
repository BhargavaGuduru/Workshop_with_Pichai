"""
Player module: Defines human and computer players.
Extensible for new player types and strategies.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from card import Card, Suit

class Player(ABC):
    """
    Abstract base class for all player types.
    Handles common player functionality.
    """
    
    def __init__(self, name: str, suit: Suit, **kwargs):
        self.name = name
        self.suit = suit
        self.hand: List[Card] = []
        self.won_cards: List[Card] = []
        self.metadata = kwargs  # Store additional data
    
    def add_card(self, card: Card) -> None:
        """Add a card to player's hand"""
        self.hand.append(card)
    
    def remove_card(self, card: Card) -> bool:
        """Remove a card from player's hand"""
        try:
            self.hand.remove(card)
            return True
        except ValueError:
            return False
    
    def add_won_card(self, card: Card) -> None:
        """Add a won diamond card to player's collection"""
        self.won_cards.append(card)
    
    def get_score(self) -> int:
        """Calculate player's total score from won cards"""
        return sum(card.get_numeric_value() for card in self.won_cards)
    
    def has_cards(self) -> bool:
        """Check if player has cards left to bid"""
        return len(self.hand) > 0
    
    def get_hand_summary(self) -> str:
        """Get a summary of player's hand"""
        if not self.hand:
            return "No cards"
        cards_str = ", ".join(str(card) for card in sorted(self.hand))
        return f"{len(self.hand)} cards: {cards_str}"
    
    def get_won_cards_summary(self) -> str:
        """Get summary of won cards"""
        if not self.won_cards:
            return "No cards"
        cards_str = ", ".join(str(card) for card in sorted(self.won_cards))
        total = self.get_score()
        return f"{len(self.won_cards)} cards ({total} points): {cards_str}"
    
    def can_bid(self, card: Card) -> bool:
        """Check if player can bid a specific card"""
        return card in self.hand
    
    def get_available_bids(self) -> List[Card]:
        """Get all cards available for bidding"""
        return self.hand.copy()
    
    @abstractmethod
    def make_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Optional[Card]:
        """Abstract method for making bids"""
        pass
    
    def reset(self) -> None:
        """Reset player state for new game"""
        self.hand.clear()
        self.won_cards.clear()
    
    def __str__(self) -> str:
        """String representation of player"""
        return f"{self.name} ({self.suit.value}) - Score: {self.get_score()}"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"Player({self.name}, {self.suit.name})"

class HumanPlayer(Player):
    """Human player requiring user input"""
    
    def __init__(self, name: str, suit: Suit, **kwargs):
        super().__init__(name, suit, **kwargs)
        self.input_method = kwargs.get('input_method', 'console')
    
    def make_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Optional[Card]:
        """Get bid from human user"""
        return self._get_user_input(auction_card, game_state)
    
    def _get_user_input(self, auction_card: Card, game_state: Dict[str, Any]) -> Optional[Card]:
        """Get user input for bid selection"""
        if self.input_method == 'console':
            return self._console_input(auction_card)
        return None  # Other input methods can be added
    
    def _console_input(self, auction_card: Card) -> Optional[Card]:
        """Console-based input for testing"""
        print(f"\n{self.name}'s turn")
        print(f"Auction Card: {auction_card} (Value: {auction_card.get_numeric_value()})")
        print(f"Your hand: {self.get_hand_summary()}")
        
        while True:
            try:
                card_input = input("Enter card to bid (e.g., 'ACE' or 'KING') or 'pass': ").strip().upper()
                
                if card_input == 'PASS':
                    return None
                
                # Try to find the card in hand
                for card in self.hand:
                    if card.rank.name == card_input:
                        return card
                
                print(f"Card '{card_input}' not found in your hand. Try again.")
                
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print(f"Invalid input: {e}")

class ComputerPlayer(Player):
    """Computer player with configurable strategies"""
    
    def __init__(self, name: str, suit: Suit, strategy: str = "random", **kwargs):
        super().__init__(name, suit, **kwargs)
        self.strategy = strategy
        self.strategies = {
            "random": self._random_bid,
            "smart": self._smart_bid, 
            "conservative": self._conservative_bid,
            "aggressive": self._aggressive_bid,
            "balanced": self._balanced_bid
        }
    
    def make_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Optional[Card]:
        """Make bid using configured strategy"""
        if not self.hand:
            return None
        
        strategy_func = self.strategies.get(self.strategy, self._random_bid)
        return strategy_func(auction_card, game_state)
    
    def _random_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Card:
        """Random bid selection"""
        import random
        return random.choice(self.hand)
    
    def _smart_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Card:
        """Smart bid based on card values"""
        auction_value = auction_card.get_numeric_value()
        
        if auction_value >= 11:  # Jack or higher
            # Bid high for valuable cards
            return max(self.hand)
        elif auction_value >= 7:  # 7-10
            # Bid medium for medium cards
            sorted_hand = sorted(self.hand)
            return sorted_hand[len(sorted_hand) // 2]
        else:  # Low cards
            # Bid low for less valuable cards
            return min(self.hand)
    
    def _conservative_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Card:
        """Always bid the lowest card"""
        return min(self.hand)
    
    def _aggressive_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Card:
        """Always bid the highest card"""
        return max(self.hand)
    
    def _balanced_bid(self, auction_card: Card, game_state: Dict[str, Any]) -> Card:
        """Balanced strategy considering auction value"""
        auction_value = auction_card.get_numeric_value()
        hand_values = [card.get_numeric_value() for card in self.hand]
        avg_hand_value = sum(hand_values) / len(hand_values)
        
        if auction_value > avg_hand_value:
            # Auction card is valuable, bid higher
            return max(self.hand)
        else:
            # Auction card is less valuable, bid lower
            return min(self.hand)
    
    def get_strategy_description(self) -> str:
        """Get description of current strategy"""
        descriptions = {
            "random": "Bids randomly from available cards",
            "smart": "Bids based on auction card value",
            "conservative": "Always bids the lowest card",
            "aggressive": "Always bids the highest card",
            "balanced": "Balanced approach based on hand strength"
        }
        return descriptions.get(self.strategy, "Unknown strategy")
