import random

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
values = {'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Please enter a valid number of chips.")
        else:
            if chips.bet > chips.total:
                print("Sorry, you don't have enough chips.")
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal_card())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing
    while True:
        choice = input("Would you like to hit or stand? Enter 'h' or 's'. ")
        if choice.lower() == 'h':
            hit(deck, hand)
        elif choice.lower() == 's':
            print("Player stands. Dealer's turn.")
            playing = False
        else:
            print("Please enter 'h' or 's'.")
            continue
        break

def show_some(player, dealer):
    print("\nPlayer's hand:")
    for card in player.cards:
        print(f"{card.rank} of {card.suit}")
    print("\nDealer's hand:")
    print("Hidden Card")
    for card in dealer.cards[1:]:
        print(f"{card.rank} of {card.suit}")

def show_all(player, dealer):
    print("\nPlayer's hand:")
    for card in player.cards:
        print(f"{card.rank} of {card.suit}")
    print(f"\nPlayer's hand value: {player.value}")
    print("\nDealer's hand:")
    for card in dealer.cards:
        print(f"{card.rank} of {card.suit}")
    print(f"\nDealer's hand value: {dealer.value}")

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    print(" Push.")

#Gamesetup
player_name = input("Enter your name: ")
player_chips = Chips()

while True:
    print("\n" + "=" * 20)
    print("Hi, " + player_name + "! Welcome to Blackjack!")
    print("Player chips:", player_chips.total)
    print("=" * 20)

    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    take_bet(player_chips)
    show_some(player_hand, dealer_hand)

    playing = True
    while playing:
        hit_or_stand(deck, player_hand)

 
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)


    print("Player chips:", player_chips.total)

    play_again = input("Would you like to play again?  'y' or 'n': ")
    if play_again.lower() != 'y':
        break