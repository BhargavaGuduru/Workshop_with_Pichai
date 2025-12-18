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

The Blind Auction Card Game is a turn-based strategic card game where players bid cards from their hands to win **hidden reward cards**. Each round awards one hidden card to the winning bidder. The player with the highest total score at the end of the game wins.

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

| Role          | Suit     | Visibility         |
| ------------- | -------- | ------------------ |
| Player 1      | Hearts   | Visible            |
| Player 2      | Clubs    | Visible            |
| Auction Deck  | Diamonds | Hidden (Face-down) |
| Excluded Suit | Spades   | Not used           |

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
4. The Diamond deck is placed face-down as the auction deck.
5. Players cannot see the Diamond cards before winning them.

---

## 6. Game Rules and Flow

### 6.1 Rounds

* The game consists of **13 rounds**.
* Each round corresponds to one Diamond card from the auction deck.

---

### 6.2 Round Execution

For each round:

1. The top Diamond card remains hidden.
2. Both players secretly select one card from their hand.
3. Selected cards are revealed simultaneously.
4. The player who plays the higher-ranked card wins the round.
5. The winner receives the top Diamond card.
6. Played cards are discarded and cannot be reused.

---

### 6.3 Tie Condition

If both players play cards of equal rank:

* The round is declared a tie.
* The Diamond card may be discarded or handled using a predefined tie-break rule (to be decided during implementation).

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

