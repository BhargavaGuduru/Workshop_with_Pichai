"""
Game module: Main game controller and flow manager.
Coordinates all game components and manages complete game flow.
"""
from typing import List, Dict, Any, Optional, Tuple
from deck import Deck
from player import Player, HumanPlayer, ComputerPlayer
from auction import Auction, AuctionResult
from card import Card, Suit, Rank

class Game:
    """
    Main game controller for Blind Auction Card Game
    """
    
    def __init__(self, players: List[Player], auction_suits: List[Suit] = None):
        self.players = players
        self.auction_suits = auction_suits or [Suit.DIAMONDS]
        self.deck = Deck()
        self.auction = Auction()
        self.round_number = 0
        self.max_rounds = 13
        self.game_over = False
        self.carry_forward_diamonds = []  # Diamonds that carry forward from ties
        self.tie_handling = "split"  # "split" or "carry_forward"
        self.game_history = []
        
    def setup_game(self) -> None:
        """Initialize and setup the game"""
        # Create and shuffle standard deck
        self.deck.create_standard_deck()
        self.deck.shuffle()
        
        # Deal cards to players based on their suits
        self._deal_cards_to_players()
        
        # Setup auction deck (remaining cards after dealing)
        self._setup_auction_deck()
        
        # Setup auction with tie handling method
        self.auction.set_tie_handling(self.tie_handling)
        
        self.round_number = 0
        self.game_over = False
        self.carry_forward_diamonds = []
        self.game_history = []
        
        print(f"🎮 Game setup complete!")
        print(f"   Players: {len(self.players)}")
        print(f"   Auction suits: {[suit.value for suit in self.auction_suits]}")
        print(f"   Tie handling: {self.tie_handling}")
    
    def _deal_cards_to_players(self) -> None:
        """Deal appropriate cards to each player"""
        for player in self.players:
            # Get all cards of player's suit
            player_cards = self.deck.get_cards_by_suit(player.suit)
            
            # Add cards to player's hand
            for card in player_cards:
                player.add_card(card)
            
            # Remove dealt cards from deck
            for card in player_cards:
                self.deck.remove_card(card)
            
            print(f"   {player.name} received {len(player_cards)} {player.suit.value} cards")
    
    def _setup_auction_deck(self) -> None:
        """Setup auction deck with specified suits"""
        # Filter deck to only auction suits
        self.deck.filter_by_suits(self.auction_suits)
        
        # Shuffle auction deck
        self.deck.shuffle()
        
        print(f"   Auction deck: {self.deck.size()} cards")
    
    def play_round(self) -> Dict[str, Any]:
        """Play a single round of the game"""
        if self.game_over:
            return {'error': 'Game is already over'}
        
        self.round_number += 1
        round_result = {
            'round_number': self.round_number,
            'diamond_card': None,
            'bids': {},
            'result': None,
            'winner': None,
            'carry_forward': False,
            'game_over': False
        }
        
        # Check if game should end
        if self._should_end_game():
            round_result['game_over'] = True
            self.game_over = True
            return round_result
        
        # Get auction card (including any carry-forward diamonds)
        auction_card = self._get_auction_card()
        if not auction_card:
            round_result['game_over'] = True
            self.game_over = True
            return round_result
        
        round_result['diamond_card'] = auction_card
        
        # Start auction
        self.auction.start_auction(auction_card, self.round_number)
        
        # Collect bids from all players
        self._collect_bids()
        round_result['bids'] = self.auction.get_all_bids()
        
        # Resolve auction
        auction_result = self.auction.resolve_auction()
        round_result['result'] = auction_result
        
        # Process auction results
        self._process_auction_results(auction_result)
        
        # Update round result
        if auction_result['winner']:
            round_result['winner'] = auction_result['winner']
        elif auction_result['carry_forward']:
            round_result['carry_forward'] = True
            self.carry_forward_diamonds.append(auction_result['diamond_card'])
        
        # Remove bid cards from players' hands
        self._remove_bid_cards(auction_result['bids'])
        
        # Clear auction for next round
        self.auction.clear_bids()
        
        # Add to game history
        self.game_history.append(round_result)
        
        return round_result
    
    def _get_auction_card(self) -> Optional[Card]:
        """Get the next auction card, including carry-forwards"""
        # First, use any carry-forward diamonds
        if self.carry_forward_diamonds:
            return self.carry_forward_diamonds.pop(0)
        
        # Then draw from auction deck
        return self.deck.draw_card()
    
    def _collect_bids(self) -> None:
        """Collect bids from all players"""
        for player in self.players:
            if not player.has_cards():
                continue
            
            # Get bid from player
            bid = player.make_bid(self.auction.current_diamond, {
                'round': self.round_number,
                'players': self.players,
                'game_history': self.game_history
            })
            
            if bid:
                self.auction.place_bid(player, bid)
    
    def _process_auction_results(self, auction_result: Dict[str, Any]) -> None:
        """Process auction results and award cards"""
        if auction_result['result_type'] == AuctionResult.WINNER_DETERMINED:
            # Award diamond to winner
            winner = auction_result['winner']
            diamond_card = auction_result['diamond_card']
            winner.add_won_card(diamond_card)
            
        elif auction_result['result_type'] == AuctionResult.TIE_SPLIT:
            # Split diamond value between tied players
            split_values = auction_result['split_values']
            diamond_card = auction_result['diamond_card']
            
            for player, points in split_values.items():
                # Create a special card to represent split points
                # For now, we'll add the original card and handle scoring separately
                player.add_won_card(diamond_card)
    
    def _remove_bid_cards(self, bids: Dict[Any, Card]) -> None:
        """Remove bid cards from players' hands"""
        for player, card in bids.items():
            player.remove_card(card)
    
    def _should_end_game(self) -> bool:
        """Check if game should end"""
        # Game ends when all players are out of cards
        return all(not player.has_cards() for player in self.players)
    
    def get_game_scores(self) -> Dict[str, int]:
        """Get current scores for all players"""
        scores = {}
        for player in self.players:
            scores[player.name] = player.get_score()
        return scores
    
    def get_winner(self) -> Optional[Player]:
        """Determine the game winner"""
        if not self.game_over:
            return None
        
        scores = self.get_game_scores()
        max_score = max(scores.values())
        winners = [player for player in self.players if player.get_score() == max_score]
        
        # Return winner if clear, None if tie
        return winners[0] if len(winners) == 1 else None
    
    def is_draw(self) -> bool:
        """Check if game ended in a draw"""
        if not self.game_over:
            return False
        
        scores = self.get_game_scores()
        max_score = max(scores.values())
        winners = [player for player in self.players if player.get_score() == max_score]
        
        return len(winners) > 1
    
    def play_full_game(self) -> Dict[str, Any]:
        """Play the complete game from start to finish"""
        self.setup_game()
        
        print(f"\n🎯 Starting game with {len(self.players)} players...")
        print("=" * 60)
        
        while not self.game_over:
            # Play round
            round_result = self.play_round()
            
            if round_result.get('error'):
                print(f"❌ Error: {round_result['error']}")
                break
            
            # Display round results
            self._display_round_results(round_result)
            
            # Check if game is over
            if round_result.get('game_over'):
                break
        
        # Display final results
        return self._display_final_results()
    
    def _display_round_results(self, round_result: Dict[str, Any]) -> None:
        """Display results of a round"""
        print(f"\n📊 Round {round_result['round_number']}")
        print(f"   Diamond: {round_result['diamond_card']} ({round_result['diamond_card'].get_numeric_value()} points)")
        
        # Display bids
        print("   Bids:")
        for player, card in round_result['bids'].items():
            print(f"     {player.name}: {card}")
        
        # Display result
        result = round_result['result']
        if result['result_type'] == AuctionResult.WINNER_DETERMINED:
            winner = result['winner']
            print(f"   🏆 Winner: {winner.name}")
        elif result['result_type'] == AuctionResult.TIE_SPLIT:
            tied_players = [p.name for p in result['tied_players']]
            split_value = result['diamond_card'].get_numeric_value() / len(result['tied_players'])
            print(f"   🤝 Tie between {', '.join(tied_players)} - split {split_value} points each")
        elif result['result_type'] == AuctionResult.TIE_CARRY_FORWARD:
            print(f"   🔄 Tie - {result['diamond_card']} carries forward")
        
        # Display current scores
        scores = self.get_game_scores()
        print(f"   Scores: {', '.join([f'{name}: {score}' for name, score in scores.items()])}")
    
    def _display_final_results(self) -> Dict[str, Any]:
        """Display final game results"""
        print("\n" + "=" * 60)
        print("🏁 GAME OVER")
        print("=" * 60)
        
        scores = self.get_game_scores()
        winner = self.get_winner()
        
        # Display final scores
        print("\n📊 Final Scores:")
        for player in self.players:
            print(f"   {player.name}: {player.get_score()} points")
            print(f"      Won cards: {player.get_won_cards_summary()}")
        
        # Display winner
        result = {
            'winner': None,
            'is_draw': False,
            'scores': scores,
            'rounds_played': self.round_number
        }
        
        if self.is_draw():
            print("\n🤝 Game ended in a DRAW!")
            result['is_draw'] = True
        else:
            print(f"\n🏆 WINNER: {winner.name} with {winner.get_score()} points!")
            result['winner'] = winner
        
        return result
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state"""
        return {
            'round_number': self.round_number,
            'game_over': self.game_over,
            'players': [
                {
                    'name': player.name,
                    'suit': player.suit.value,
                    'cards_left': len(player.hand),
                    'score': player.get_score(),
                    'won_cards': len(player.won_cards)
                }
                for player in self.players
            ],
            'auction_deck_size': self.deck.size(),
            'carry_forward_diamonds': len(self.carry_forward_diamonds),
            'scores': self.get_game_scores()
        }
