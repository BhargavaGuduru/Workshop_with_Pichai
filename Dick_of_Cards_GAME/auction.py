"""
Auction module: Manages bidding process and tie handling.
Handles winner determination and diamond card distribution.
"""
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from card import Card

class AuctionResult(Enum):
    """Possible auction outcomes"""
    WINNER_DETERMINED = "winner"
    TIE_SPLIT = "tie_split"
    TIE_CARRY_FORWARD = "tie_carry"

class Auction:
    """
    Manages the auction process for a single round
    """
    
    def __init__(self):
        self.current_diamond: Optional[Card] = None
        self.bids: Dict[Any, Card] = {}  # Player -> Card
        self.tie_handling_method = "split"  # "split" or "carry_forward"
        self.round_number = 0
    
    def start_auction(self, diamond_card: Card, round_number: int = 0) -> None:
        """Start a new auction with a diamond card"""
        self.current_diamond = diamond_card
        self.bids.clear()
        self.round_number = round_number
    
    def place_bid(self, player, card: Card) -> bool:
        """Place a bid for a player"""
        if player in self.bids:
            return False  # Player already bid
        
        self.bids[player] = card
        return True
    
    def get_all_bids(self) -> Dict[Any, Card]:
        """Get all current bids"""
        return self.bids.copy()
    
    def is_auction_complete(self, expected_players: int) -> bool:
        """Check if all expected players have bid"""
        return len(self.bids) == expected_players
    
    def determine_winner(self) -> Tuple[AuctionResult, Optional[Any], Optional[List[Any]]]:
        """
        Determine auction outcome
        Returns: (result, winner, tied_players)
        """
        if len(self.bids) < 2:
            # Not enough bids for a proper auction
            return AuctionResult.WINNER_DETERMINED, None, None
        
        # Sort bids by card value (highest first)
        sorted_bids = sorted(self.bids.items(), key=lambda x: x[1].get_numeric_value(), reverse=True)
        
        # Check for tie
        highest_value = sorted_bids[0][1].get_numeric_value()
        tied_players = [player for player, card in sorted_bids if card.get_numeric_value() == highest_value]
        
        if len(tied_players) > 1:
            # Tie occurred
            if self.tie_handling_method == "split":
                return AuctionResult.TIE_SPLIT, None, tied_players
            else:
                return AuctionResult.TIE_CARRY_FORWARD, None, tied_players
        else:
            # Clear winner
            return AuctionResult.WINNER_DETERMINED, sorted_bids[0][0], [sorted_bids[0][0]]
    
    def resolve_auction(self) -> Dict[str, Any]:
        """
        Resolve the auction and return results
        Returns dictionary with outcome details
        """
        result = {
            'diamond_card': self.current_diamond,
            'bids': self.bids.copy(),
            'result_type': None,
            'winner': None,
            'tied_players': [],
            'diamond_awarded': False,
            'carry_forward': False,
            'split_values': {}
        }
        
        if not self.bids:
            result['result_type'] = 'no_bids'
            return result
        
        auction_result, winner, tied_players = self.determine_winner()
        result['result_type'] = auction_result
        result['winner'] = winner
        result['tied_players'] = tied_players
        
        if auction_result == AuctionResult.WINNER_DETERMINED:
            if winner is not None:
                # Single winner gets the diamond
                result['diamond_awarded'] = True
            else:
                # Not enough bids for proper auction
                result['result_type'] = 'insufficient_bids'
        elif auction_result == AuctionResult.TIE_SPLIT:
            # Split diamond value between tied players
            result['diamond_awarded'] = True
            split_value = self.current_diamond.get_numeric_value() / len(tied_players)
            result['split_values'] = {player: split_value for player in tied_players}
        elif auction_result == AuctionResult.TIE_CARRY_FORWARD:
            # Diamond card carries forward to next round
            result['carry_forward'] = True
            result['diamond_awarded'] = False
        
        return result
    
    def get_bid_summary(self) -> str:
        """Get a summary of current bids"""
        if not self.bids:
            return "No bids placed"
        
        summary_parts = []
        for player, card in self.bids.items():
            summary_parts.append(f"{player.name}: {card} ({card.get_numeric_value()})")
        
        return " | ".join(summary_parts)
    
    def get_auction_summary(self) -> str:
        """Get complete auction summary"""
        if not self.current_diamond:
            return "No auction in progress"
        
        summary = f"Round {self.round_number}: {self.current_diamond} ({self.current_diamond.get_numeric_value()} points)\n"
        summary += f"Bids: {self.get_bid_summary()}"
        
        return summary
    
    def clear_bids(self) -> None:
        """Clear all bids for next auction"""
        self.bids.clear()
    
    def set_tie_handling(self, method: str) -> None:
        """Set tie handling method ('split' or 'carry_forward')"""
        if method in ['split', 'carry_forward']:
            self.tie_handling_method = method
        else:
            raise ValueError("Tie handling method must be 'split' or 'carry_forward'")
    
    def get_bid_value(self, player) -> Optional[int]:
        """Get the bid value for a specific player"""
        if player in self.bids:
            return self.bids[player].get_numeric_value()
        return None
    
    def get_highest_bid(self) -> Optional[Tuple[Any, Card]]:
        """Get the highest bid (player, card)"""
        if not self.bids:
            return None
        
        highest_bid = max(self.bids.items(), key=lambda x: x[1].get_numeric_value())
        return highest_bid
    
    def get_lowest_bid(self) -> Optional[Tuple[Any, Card]]:
        """Get the lowest bid (player, card)"""
        if not self.bids:
            return None
        
        lowest_bid = min(self.bids.items(), key=lambda x: x[1].get_numeric_value())
        return lowest_bid
    
    def __str__(self) -> str:
        """String representation of auction"""
        return self.get_auction_summary()
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"Auction(diamond={self.current_diamond}, bids={len(self.bids)})"
