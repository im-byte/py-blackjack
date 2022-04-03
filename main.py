import sys
from random import shuffle, randint
import os

current_card_pack = []
CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]
CARD_SYMBOLS = ["♣", "♦", "♥", "♠"]


def take_new_pack():
    for n in range(4):
        for card in CARDS:
            current_card_pack.append(card + CARD_SYMBOLS[n])
    shuffle(current_card_pack)


def get_hand_value(_cards):
    value = 0
    value_soft = 0

    for card in _cards:
        if card[:-1] != "A":
            if card[:-1].isdigit():
                value += int(card[:-1])
                value_soft += int(card[:-1])
            else:
                value += 10
                value_soft += 10
        else:
            value += 11
            value_soft += 1

    if value > 21:
        return value_soft
    else:
        return value


def take_random_card():
    # Take a new deck if needed
    global current_card_pack
    if len(current_card_pack) == 0:
        take_new_pack()

    # Pick a random card
    i = randint(0, len(current_card_pack) - 1)
    card = current_card_pack[i]
    current_card_pack.remove(card)

    return card


def check_for_win(_player_cards, _dealer_cards):
    _player_value = get_hand_value(_player_cards)
    _dealer_value = get_hand_value(_dealer_cards)

    if _player_value == 21:
        print_table(_player_cards, _dealer_cards, False)
        print("Blackjack! You won.")
        return True

    if _player_value > 21:
        print_table(_player_cards, _dealer_cards, False)
        print("Bust. You lost.")
        return True

    if _dealer_value == 21:
        print_table(_player_cards, _dealer_cards, False)
        print("Dealer blackjack. You lost.")
        return True

    if _dealer_value > 21:
        print_table(_player_cards, _dealer_cards, False)
        print("Dealer busted. You won!")
        return True

    return False


def print_table(_player_cards, _dealer_cards, _player_turn):
    # Clear console
    os.system('cls')

    # Dealer cards
    n = 0
    dealer_cards_string = "The dealer cards are:\n"
    for card in _dealer_cards:
        if _player_turn is True:
            if n != len(_dealer_cards) - 1:
                dealer_cards_string += card + "  "
            else:
                dealer_cards_string += "??  "
        else:
            dealer_cards_string += card + "  "
        n += 1
    print(dealer_cards_string)

    if _player_turn:
        hidden_deck = _dealer_cards[:-1]
        print("Value: {0}\n".format(get_hand_value(hidden_deck)))
    else:
        print("Value: {0}\n".format(get_hand_value(_dealer_cards)))

    # Player cards
    player_cards_string = "Your cards are:\n"
    for card in _player_cards:
        player_cards_string += card + "  "
    print(player_cards_string)
    print("Value: {0}\n".format(get_hand_value(_player_cards)))

    for i in range(1):
        print(" ")


while True:
    dealer_cards = []
    player_cards = []

    # First 2 cards for both
    dealer_cards.append(take_random_card())
    player_cards.append(take_random_card())
    dealer_cards.append(take_random_card())
    player_cards.append(take_random_card())

    # New game
    if check_for_win(player_cards, dealer_cards):
        new_round = input("Would you like to play another round? (y/n)\n")
        if new_round.lower() == "n":
            sys.exit()
        else:
            continue

    print_table(player_cards, dealer_cards, True)

    # Player hitting
    player_action = input("HIT or STAND?\n").upper()
    while player_action != "STAND":
        player_cards.append(take_random_card())

        if check_for_win(player_cards, dealer_cards):
            player_action = "NEW_GAME"
            break
        else:
            print_table(player_cards, dealer_cards, True)
            player_action = input("HIT or STAND?\n").upper()

    # New game check
    if player_action == "NEW_GAME":
        new_round = input("Would you like to play another round? (y/n)\n")
        if new_round.lower() == "n":
            sys.exit()
        else:
            continue

    # Dealer hits
    dealer_value = get_hand_value(dealer_cards)
    while dealer_value < 17:
        dealer_cards.append(take_random_card())
        dealer_value = get_hand_value(dealer_cards)
    print_table(player_cards, dealer_cards, False)

    # Decide the winner
    dealer_value_end = get_hand_value(dealer_cards)
    player_value_end = get_hand_value(player_cards)

    if dealer_value_end > 21:
        print("Dealer busted. You won!")
    elif dealer_value_end == 21:
        print("Dealer blackjack. You lost.")
    else:
        if player_value_end > dealer_value_end:
            print("You won!")
        elif player_value_end < dealer_value_end:
            print("You lost.")
        elif player_value_end == dealer_value_end:
            print("Push. Nobody won.")

    new_round = input("Would you like to play another round? (y/n)\n")
    if new_round.lower() == "n":
        sys.exit()
