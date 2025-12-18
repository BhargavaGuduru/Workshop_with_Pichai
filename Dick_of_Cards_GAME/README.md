# Blind Auction Card Game

## Game Requirements Document (2-Player Version)

---

## 1. Introduction

### 1.1 Purpose

This document defines the rules, structure, and requirements for implementing a **Blind Auction Card Game** for two players. It serves as a clear reference for development, testing, and future enhancement of the game as a group project.

### 1.2 Scope

This document covers:

* Two-player gameplay
* Card distribution and auction mechanics
* Scoring and win conditions

A three-player version and advanced features are considered future enhancements and are out of scope for this document.

---

## 2. Game Overview

The Blind Auction Card Game is a turn-based strategic card game where players bid cards from their hands to win **visible Diamond cards**. Unlike a blind auction, the Diamond card for each round is revealed before bidding, allowing players to see its value and strategically decide how much to bid. The player who bids higher wins the Diamond card, and the player with the highest total Diamond score at the end of the game wins.

---

## 3. Game Components

### 3.1 Card Deck

A standard deck of playing cards contains four suits:

* Hearts
* Clubs
* Diamonds
* Spades

Each suit contains the following 13 cards:

```
A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
```

---

### 3.2 Suit Allocation (2-Player Mode)

| Role          | Suit     | Visibility                   |
| ------------- | -------- | ---------------------------- |
| Player 1      | Hearts   | Visible                      |
| Player 2      | Clubs    | Visible                      |
| Auction Deck  | Diamonds | Visible (Revealed per round) |
| Excluded Suit | Spades   | Not used                     |

---

## 4. Card Ranking and Values

### 4.1 Card Ranking

Cards are ranked in the following order:

```
A (highest) > K > Q > J > 10 > 9 > ... > 2 (lowest)
```

### 4.2 Numeric Values (for scoring)

| Card | Value      |
| ---- | ---------- |
| A    | 14         |
| K    | 13         |
| Q    | 12         |
| J    | 11         |
| 2–10 | Face value |

---

## 5. Game Setup

1. Player 1 receives all 13 **Hearts** cards.
2. Player 2 receives all 13 **Clubs** cards.
3. All 13 **Diamond** cards are shuffled randomly.
4. The Diamond deck is placed face-down initially.
5. At the start of each round, the top Diamond card is **revealed** to both players, showing its value before bidding.

---

## 6. Game Rules and Flow

### 6.0 Auction Clarifications and Special Rules

The following rules define how bidding, card consumption, and visible Diamond cards are handled:

1. **Visible Diamond Value Rule**

   * At the start of each round, the top Diamond card is revealed.
   * Players can see the **exact value** of the Diamond card before placing bids.

2. **Competitive Bidding Rule**

   * Both players must bid **one card** from their hand to compete for the revealed Diamond card.
   * The player who bids the higher-ranked card wins the Diamond card.

3. **Consumable Bid Rule**

   * The bid cards used by **both players** are removed from play once the auction resolves.
   * Bid cards **cannot be reused** in future rounds.

4. **Diamond Consumption Rule**

   * The Diamond card won in a round is removed from the auction deck and added to the winner’s score pile.

5. **Tie (Equal Bid) Rule**

   * If both players bid cards of equal value, **share the diamond card in to two and values should be euqual to them**.
   * Both bid cards are still **consumed and removed from play**.
   * The same Diamond card is carried forward to the next round.

6. **Diamond-Only Scoring Rule**

   * Only Diamond cards contribute to scoring.
   * Hearts and Clubs are used strictly for bidding purposes.

7. **Highest Bid Constraints**

   * Ace (A) is the highest possible bid.
   * King (K) can be beaten only by Ace (A).
   * Ace (A) is the highest possible bid.
   * King (K) can be beaten by Ace (A).
   * If both players bid Ace (A), the Tie Rule applies.

---

## 6.1 Rounds

### 6.1 Rounds

* The game consists of **13 rounds**.
* Each round corresponds to one Diamond card from the auction deck.

---

### 6.2 Round Execution

For each round:

1. Reveal the top Diamond card to both players.
2. Both players secretly select one card from their remaining hand as a bid.
3. Bid cards are revealed simultaneously.
4. The player with the higher-ranked bid wins the Diamond card.
5. **Both bid cards are removed from play permanently**.
6. The Diamond card is awarded to the winning player.
7. If bids are equal, no Diamond card is awarded and the same Diamond card is auctioned again in the next round.

---

### 6.3 Tie Condition

If both players bid cards of equal rank:

* No player wins the Diamond card.
* Both bid cards are discarded from play.
* The Diamond card remains available for the next round.

---

## 7. Scoring System

1. Each player collects the Diamond cards they win.
2. At the end of all rounds, each Diamond card is converted to its numeric value.
3. The total score for each player is calculated.

### 7.1 Score Formula

```
Total Score = Sum of Diamond card values won
```

---

## 8. Winning Conditions

* The player with the highest total score wins the match.
* If both players have the same score, the game ends in a draw.

---

## 9. Functional Requirements

* The system shall distribute cards according to the defined setup.
* The system shall shuffle the Diamond deck randomly.
* The system shall prevent players from reusing discarded cards.
* The system shall determine round winners correctly.
* The system shall assign Diamond cards to the correct player.
* The system shall calculate final scores accurately.

---

## 10. Non-Functional Requirements

* The game logic must be fair and deterministic.
* Random shuffling must ensure unpredictability.
* The implementation should be modular and maintainable.
* The design should allow future extension to a 3-player version.

---

## 11. Assumptions and Constraints

* Players follow the rules honestly.
* Card rankings and values are fixed.
* No player can view Diamond cards before winning them.

---

## 12. Future Enhancements

* 3-player gameplay using all four suits
* AI-controlled players
* Online multiplayer support
* Strategy analysis and statistics

---

## 13. Conclusion

This document provides a complete and clear specification for the **2-Player Blind Auction Card Game**. It can be used as a foundation for implementation, testing, and future enhancements in a group project environment.
