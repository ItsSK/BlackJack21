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
outcome = ""
value_ace = 0
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

    def remove_cards(self):
        return self.cards.clear()

    def return_cards(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        global popped
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

    def remove_cards(self):
        self.player_hand.clear()
        return self.player_hand

    def get_value(self):
        global value_ace
        value = 0
        ace_count = 0
        for card in self.player_hand:
            rank = card.get_rank()
            value = value + VALUES[rank]
            if rank == 'A':
                ace_count += 1
        value_ace = value
        for card in self.player_hand:
            rank = card.get_rank()
            if ace_count < 2:
                if rank == 'A' and value <= 11:
                    value += 10
            else:
                break
        return value


def game_loop():  # What does the player want?
    global player, deck, player_value, hidden_card
    # Game Loop
    while not player_value > 21:
        # does the player have BJ
        if player_value == 21:
            dealer_move()
        else:
            message_is_valid = True
            message = input('Hit or Stand or Exit\n')
            while message_is_valid:
                if message.lower() == 'hit':
                    player.add_card(deck.deal_card())
                    player_value = player.get_value()
                    message_is_valid = False
                elif message.lower() == 'stand':
                    message_is_valid = False
                    dealer_move()
                elif message.lower() == 'exit':
                    print('####################')
                    exiting()
                else:
                    message = input('Hit or Stand or Exit\n')
        if player_value < 21:
            print_player()
            print('Dealer:', hidden_card, '=', get_hidden_value())
    who_busted()


def dealer_move():
    global dealer, dealer_value, player_value, deck, dealer_score
    # dealer draws until hand value > 17
    while not dealer_value > 21:
        # TODO possibly create different get_value() methods in Hand()
        if dealer_value < 17:  # soft 17 ACE and 6 should just be 7 not 17
            dealer.add_card(deck.deal_card())
            dealer_value = dealer.get_value()
        else:
            compare_values()
    who_busted()


def compare_values():
    global player_value, dealer_value, player_score, dealer_score
    if player_value > dealer_value:
        print('\n####################\n')
        print('Player Wins!')
        player_score += 1
    elif player_value < dealer_value:
        print('\n####################\n')
        print('Dealer Wins!')
        dealer_score += 1
    elif player_value == dealer_value:
        print('\n####################\n')
        print('Push, Nobody wins')
    print_player()
    print_dealer()
    print('\nHouse:', dealer_score, 'Player:', player_score)
    print('\n####################')
    restart_hand()


def exiting():
    # print_player()
    # print_dealer()
    print('\nHouse:', dealer_score, 'Player:', player_score)
    print('\n####################')
    exit(0)


def who_busted():
    global player_value, dealer_value, player_score, dealer_score
    # who Busted?
    if player_value > 21:
        print('\n####################\n')
        print('Player: Busted')
        dealer_score += 1
    elif dealer_value > 21:
        player_score += 1
        print('\n####################\n')
        print('Dealer: Busted\nYou Win!')
    print_player()
    print_dealer()
    print('\nHouse:', dealer_score, 'Player:', player_score)
    print('\n####################')
    restart_hand()


def print_player():
    global player, player_value, value_ace
    player_value = player.get_value()
    if value_ace == player_value:
        print('\nPlayer:', player, '=', player_value)
    else:
        # print player value with ace
        print('\nPlayer:', player, '=', str(value_ace) + '/' + str(player_value))


def print_dealer():
    global dealer, dealer_value, value_ace
    dealer_value = dealer.get_value()
    if value_ace == dealer_value:
        print('Dealer:', dealer, '=', dealer_value)
    else:
        # print dealer card with ace
        print('Dealer:', dealer, '=', str(value_ace)+'/'+str(dealer_value))


def get_hidden_value():
    global hidden_card
    hidden_card_value = VALUES[hidden_card.get_rank()]
    value = 0
    value = value + hidden_card_value
    if hidden_card.get_rank() == 'A' and value <= 11:
        value += 10
        return str(hidden_card_value) + '/' + str(value)
    else:
        return str(hidden_card_value)


def restart_deck():
    global deck, player, dealer
    player.remove_cards()
    dealer.remove_cards()
    deck.remove_cards()
    deck = Deck()
    player = Hand()
    dealer = Hand()


def restart_hand():
    global player, dealer, deck, hidden_card, player_value, dealer_value, value_ace
    if len(deck.return_cards()) < 6:
        restart_deck()
    print(len(deck.return_cards()))
    print('\nHand:')
    player.remove_cards()
    dealer.remove_cards()
    player.add_card(deck.deal_card())  # shown
    dealer.add_card(deck.deal_card())  # hidden
    player.add_card(deck.deal_card())  # shown
    hidden_card = deck.deal_card()  # no hole card
    dealer.add_card(hidden_card)  # shown
    player_value = player.get_value()
    if value_ace == player_value:
        print('Player:', player, '=', str(player_value))
    else:
        # print player value with ace
        print('Player:', player, '=', str(value_ace) + '/' + str(player_value))
    dealer_value = dealer.get_value()
    print('Dealer:', hidden_card, '=', get_hidden_value())
    game_loop()


def start_game():
    global player, dealer, deck, hidden_card, player_value, dealer_value, value_ace
    print("Hand:")
    deck = Deck()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())  # shown
    dealer.add_card(deck.deal_card())  # hidden
    player.add_card(deck.deal_card())  # shown
    hidden_card = deck.deal_card()  # no hole card
    dealer.add_card(hidden_card)  # shown
    player_value = player.get_value()
    if value_ace == player_value:
        print('Player:', player, '=', str(player_value))
    else:
        # print player value with ace
        print('Player:', player, '=', str(value_ace)+'/'+str(player_value))
    dealer_value = dealer.get_value()
    print('Dealer:', hidden_card, '=', get_hidden_value())
    game_loop()

# TODO multi player mode
# TODO add betting/money
# TODO add splitting hand


start_game()
