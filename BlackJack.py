# BlackJack Game
# @author Sergey Klassen

import os
import time
import random

'''
Rules:
An Ace can count as either 1 or 11
The cards 2 - 9 are valued at their face value
the "10", jack, queen, king are all valued at 10.

The suits of the cards do not have any meaning in the game.
The value of a hand is simply the sum of the point counts of each card in the hand.

5 + 7 + 9 = 21, so this hand has a value of 21.
9 + 3 + 10 = 22, so this hand is a "bust".

Any hand that goes over 21 "breaks", or is "busted", and is an automatic loser.
'''

# initialize global variables
in_play = False
end_game = False
message = ""
outcome = ""
dealer_score = 0
player_score = 0
hidden_card = []
player_value = []
dealer_value = []
popped = []
player = []
dealer = []
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


# Deck class used for re-shuffling between hands and giving card objects to Hand as called
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def __str__(self):
        s = ''
        for c in self.cards:
            s = s + str(c) + ' '
        return s

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        popped = self.cards.pop(0)
        return popped


# Hand class used for adding card objects from Deck() and for getting the value of hands
class Hand:
    def __init__(self):
        self.player_hand = []

    def __str__(self):
        s = ''
        for c in self.player_hand:
            s = s + str(c) + ' '
        return s

    def add_card(self, card):
        self.player_hand.append(card)
        return self.player_hand

    def get_value(self):
        value = 0
        for card in self.player_hand:
            rank = card.get_rank()
            value = value + VALUES[rank]
        for card in self.player_hand:
            rank = card.get_rank()
            if rank == 'A' and value <= 11:  # TODO make the ACE work
                value += 10
        return value


def game_loop():  # What does the player want?
    global message, player, deck, player_value
    # Game Loop
    while not player_value > 21:
        # does the player have BJ
        if player_value == 21:
            dealer_move()
        else:
            message = input('Hit or Stand?\n')  # TODO make sure player enters word correctly
            if message.lower() == 'hit':
                player.add_card(deck.deal_card())
                player_value = player.get_value()
            else:
                dealer_move()
        print_hands()
    who_busted()


def dealer_move():
    global dealer, dealer_value, player_value, deck, dealer_score
    # does the dealer have BJ POST REVEAL
    while not dealer_value > 21:
        if dealer_value < 17:
            dealer.add_card(deck.deal_card())
            dealer_value = dealer.get_value()
        else:
            compare_values()
    who_busted()


def compare_values():
    global player_value, dealer_value, message, player_score, dealer_score
    if player_value > dealer_value:
        print('Player Wins!')
        player_score += 1
    elif player_value < dealer_value:
        print('Dealer Wins!')
        dealer_score += 1
    elif player_value == dealer_value:
        print('Push, Nobody wins')
    print_hands()
    print('\nHouse:', dealer_score, 'Player:', player_score)
    exit(0)


def who_busted():
    global player_value, dealer_value, player_score, dealer_score
    # who Busted?
    if player_value > 21:
        print('Player: Busted')
        dealer_score += 1
    elif dealer_value > 21:
        player_score += 1
        print('Dealer: Busted\nYou Win!')
    print_hands()
    print('\nHouse:', dealer_score, 'Player:', player_score)
    exit(0)


def print_hands():
    global player, dealer
    print('\nPlayer:', player, '=', player.get_value())
    print('Dealer:', dealer, '=', dealer.get_value())


def start_game():
    global player, dealer, deck, hidden_card, player_value, dealer_value
    print("Hand:")
    deck = Deck()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())  # shown
    dealer.add_card(deck.deal_card())  # shown
    player.add_card(deck.deal_card())  # shown
    hidden_card = deck.deal_card()  # hidden # no hole card
    dealer.add_card(hidden_card)  # shown
    player_value = player.get_value()
    dealer_value = dealer.get_value()
    print('Player:', player, '=', player_value)
    print('Dealer:', hidden_card, '=', VALUES[hidden_card.get_rank()])
    game_loop()

# TODO hide dealer hand when player hits
# TODO loop game_loop()
# TODO multi player mode
# TODO add betting/money


start_game()
