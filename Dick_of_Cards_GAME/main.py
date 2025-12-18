"""
Main entry point for Blind Auction Card Game
Follows the exact procedure specified by user
"""
import random
from deck import Deck
from player import HumanPlayer, ComputerPlayer
from auction import Auction, AuctionResult
from card import Card, Suit, Rank

def get_player_count():
    """Get number of players (2 or 3)"""
    while True:
        try:
            count = int(input("How many players are playing? (2 or 3): "))
            if count in [2, 3]:
                return count
            print("Please enter 2 or 3")
        except ValueError:
            print("Please enter a valid number")

def get_player_types_2player():
    """Get player types for 2-player game"""
    while True:
        try:
            choice = int(input("1. 2 humans\n2. 1 human and 1 machine\nChoose (1 or 2): "))
            if choice == 1:
                return ["human", "human"]
            elif choice == 2:
                return ["human", "computer"]
            print("Please enter 1 or 2")
        except ValueError:
            print("Please enter a valid number")

def get_player_types_3player():
    """Get player types for 3-player game"""
    while True:
        try:
            choice = int(input("1. 3 humans\n2. 2 humans and 1 machine\n3. 1 human and 2 machines\nChoose (1, 2, or 3): "))
            if choice == 1:
                return ["human", "human", "human"]
            elif choice == 2:
                return ["human", "human", "computer"]
            elif choice == 3:
                return ["human", "computer", "computer"]
            print("Please enter 1, 2, or 3")
        except ValueError:
            print("Please enter a valid number")

def assign_random_suits(player_count):
    """Randomly assign suits to players"""
    available_suits = [Suit.HEARTS, Suit.CLUBS, Suit.SPADES]
    random.shuffle(available_suits)
    return available_suits[:player_count]

def create_players(player_types, suits):
    """Create players with assigned suits"""
    players = []
    for i, (player_type, suit) in enumerate(zip(player_types, suits)):
        if player_type == "human":
            player = HumanPlayer(f"Human {i+1}", suit)
        else:
            player = ComputerPlayer(f"Machine {i+1}", suit, strategy="smart")
        players.append(player)
    return players

def display_player_hands(players):
    """Display each player's cards"""
    print("\n=== PLAYER HANDS ===")
    for player in players:
        print(f"{player.name} ({player.suit.value}):")
        player.hand.sort()
        for card in player.hand:
            print(f"  {card} (Value: {card.get_numeric_value()})")
        print()

def get_human_bid(player, auction_card):
    """Get bid from human player"""
    while True:
        print(f"\n{player.name}'s turn to bid")
        print(f"Auction Card: {auction_card} (Value: {auction_card.get_numeric_value()})")
        print("Your cards:")
        for i, card in enumerate(player.hand):
            print(f"  {i+1}. {card} (Value: {card.get_numeric_value()})")
        
        try:
            choice = int(input(f"Choose a card to bid (1-{len(player.hand)}): "))
            if 1 <= choice <= len(player.hand):
                return player.hand[choice - 1]
            print(f"Please enter a number between 1 and {len(player.hand)}")
        except ValueError:
            print("Please enter a valid number")

def play_round(players, auction_deck, round_num):
    """Play a single round"""
    print(f"\n{'='*50}")
    print(f"ROUND {round_num}")
    print(f"{'='*50}")
    
    # Reveal auction card
    auction_card = auction_deck.draw_card()
    if not auction_card:
        return None  # No more cards
    
    print(f"\n🎯 AUCTION CARD: {auction_card} (Value: {auction_card.get_numeric_value()})")
    
    # Collect bids
    bids = {}
    for player in players:
        if isinstance(player, HumanPlayer):
            bid = get_human_bid(player, auction_card)
        else:
            bid = player.make_bid(auction_card, {'round': round_num})
            print(f"{player.name} bids: {bid}")
        
        bids[player] = bid
    
    # Determine winner
    sorted_bids = sorted(bids.items(), key=lambda x: x[1].get_numeric_value(), reverse=True)
    highest_bid = sorted_bids[0][1].get_numeric_value()
    tied_players = [p for p, card in bids.items() if card.get_numeric_value() == highest_bid]
    
    if len(tied_players) > 1:
        # Tie - split diamond value
        split_value = auction_card.get_numeric_value() / len(tied_players)
        print(f"\n🤝 TIE! Diamond value split: {split_value} points each")
        for player in tied_players:
            player.add_won_card(auction_card)  # Add card for scoring
            print(f"  {player.name} gets {split_value} points")
    else:
        # Clear winner
        winner = sorted_bids[0][0]
        winner.add_won_card(auction_card)
        print(f"\n🏆 {winner.name} wins the {auction_card}!")
    
    # Remove bid cards from hands
    for player, bid in bids.items():
        player.remove_card(bid)
        print(f"{player.name} used {bid}")
    
    return auction_card

def calculate_final_scores(players):
    """Calculate and display final scores"""
    print(f"\n{'='*50}")
    print("GAME OVER - FINAL SCORES")
    print(f"{'='*50}")
    
    scores = {}
    for player in players:
        score = player.get_score()
        scores[player.name] = score
        print(f"{player.name}: {score} points")
        print(f"  Won cards: {player.get_won_cards_summary()}")
    
    # Determine winner
    max_score = max(scores.values())
    winners = [name for name, score in scores.items() if score == max_score]
    
    if len(winners) == 1:
        print(f"\n🏆 WINNER: {winners[0]} with {max_score} points!")
    else:
        print(f"\n🤝 DRAW: {', '.join(winners)} with {max_score} points each!")
    
    return scores

def main():
    """Main game function following user's exact procedure"""
    print("🎮 BLIND AUCTION CARD GAME")
    print("="*50)
    
    # Step 2: Get player count
    player_count = get_player_count()
    
    # Step 3: Get player types
    if player_count == 2:
        player_types = get_player_types_2player()
    else:
        player_types = get_player_types_3player()
    
    # Step 4: Random suit assignment
    suits = assign_random_suits(player_count)
    
    # Create players
    players = create_players(player_types, suits)
    
    # Create and setup deck
    deck = Deck()
    deck.create_standard_deck()
    deck.shuffle()
    
    # Deal cards to players
    for player in players:
        player_cards = deck.get_cards_by_suit(player.suit)
        for card in player_cards:
            player.add_card(card)
        # Remove dealt cards from deck
        for card in player_cards:
            deck.remove_card(card)
    
    # Create auction deck (Diamonds only)
    auction_deck = Deck()
    diamonds = [card for card in deck.cards if card.suit == Suit.DIAMONDS]
    auction_deck.add_cards(diamonds)
    auction_deck.shuffle()
    
    # Display initial setup
    print(f"\n📋 GAME SETUP")
    print(f"Players: {player_count}")
    for i, player in enumerate(players):
        print(f"  {player.name}: {player.suit.value} suit")
    
    display_player_hands(players)
    
    # Step 5-9: Play rounds
    round_num = 1
    while True:
        # Check if any players have cards
        if not any(player.has_cards() for player in players):
            break
        
        # Check if auction deck has cards
        if auction_deck.is_empty():
            break
        
        # Play round
        auction_card = play_round(players, auction_deck, round_num)
        if auction_card is None:
            break
        
        round_num += 1
    
    # Calculate final scores and determine winner
    final_scores = calculate_final_scores(players)
    
    print(f"\nGame completed in {round_num - 1} rounds!")

if __name__ == "__main__":
    main()
