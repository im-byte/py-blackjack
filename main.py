from random import shuffle, randint
import os

current_card_pack = []
all_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]
card_symbols = ["♣", "♦", "♥", "♠"]


def new_pack():
    card_pack = []

    for card in all_cards:
        for i in range(4):
            card_pack.append(card + card_symbols[i])

    shuffle(card_pack)
    return card_pack


def take_random_card():
    global current_card_pack

    # Take a new deck if empty.
    if len(current_card_pack) == 0:
        current_card_pack = new_pack()

    # Pick a random card
    i = randint(0, len(current_card_pack) - 1)
    card = current_card_pack[i]
    current_card_pack.remove(card)
    return card


def get_card_value(card):
    for symbol in card_symbols:
        card = card.replace(symbol, "")

    if card.isdigit():
        return int(card)
    else:
        return 10


def print_table(_player_cards, _dealer_cards, _player_end):
    os.system('cls')
    # Dealer cards
    n = 0
    dealer_cards_string = "The dealer cards are:\n"
    for card in _dealer_cards:
        if _player_end is False:
            if n != len(_dealer_cards) - 1:
                dealer_cards_string += card + "  "
            else:
                dealer_cards_string += "??  "
        else:
            dealer_cards_string += card + "  "
        n += 1
    print(dealer_cards_string)

    if not _player_end:
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


def get_hand_value(cards):
    value = 0
    value_soft = 0

    for card in cards:
        if card[:-1] != "A":
            value += get_card_value(card)
            value_soft += get_card_value(card)
        else:
            value += 11
            value_soft += 1

    if value >= 21:
        return value_soft
    else:
        return value


while True:
    dealer_cards = []
    player_cards = []
    player_end = False

    # Give cards.
    dealer_cards.append(take_random_card())
    player_cards.append(take_random_card())
    dealer_cards.append(take_random_card())
    player_cards.append(take_random_card())

    print_table(player_cards, dealer_cards, player_end)
    next_action = input("HIT or STAND?\n")

    # Player Hits
    while next_action == "hit":
        # Take a new card and print the table.
        player_cards.append(take_random_card())
        print_table(player_cards, dealer_cards, player_end)

        # Game over because of bust.
        if get_hand_value(player_cards) > 21:
            print("Busted. Dealer won.")
            new_round = input("Would you like to play another round? (y/n)\n")
            if new_round == "y":
                next_action = "NEW"
                break
            else:
                exit()
        elif get_hand_value(player_cards) == 21:  # Blackjack
            player_end = True
            print_table(player_cards, dealer_cards, player_end)
            print("BLACKJACK! You won.")
            new_round = input("Would you like to play another round? (y/n)\n")
            if new_round == "y":
                next_action = "NEW"
                break
            else:
                exit()

        # Next
        next_action = input("HIT or STAND?\n")

    # New game.
    if next_action == "NEW":
        continue

    player_end = True

    # Dealer hits
    dealer_value = get_hand_value(dealer_cards)
    while dealer_value < 17:
        dealer_cards.append(take_random_card())
        dealer_value = get_hand_value(dealer_cards)
    print_table(player_cards, dealer_cards, player_end)

    # Decide the winner
    dealer_value_end = get_hand_value(dealer_cards)
    player_value_end = get_hand_value(player_cards)

    if dealer_value_end > 21:
        print("Dealer busted.")
    elif dealer_value_end == 21:
        print("Blackjack. Dealer won.")
    else:
        if player_value_end > dealer_value_end:
            print("You won!")
        elif player_value_end < dealer_value_end:
            print("Dealer won.")
        elif player_value_end == dealer_value_end:
            print("Push. Nobody won.")

    new_round = input("Would you like to play another round? (y/n)\n")
    if new_round.lower == "n":
        exit()
