"""
Rules:
1. The game will have two players: the Dealer and the Player. The game will start off with a deck of 52 cards. The 52 cards will consist of 4 different suits: Clubs, Diamonds, Hearts and Spades. For each suit, there will be cards numbered 1 through 13.

Note:
1. No wildcards will be used in the program
2. When the game begins, the dealer will shuffle the deck of cards, making them randomized. After the dealer shuffles, it will deal the player 2 cards and will deal itself 2 cards from. The Player should be able to see both of their own cards, but should only be able to see one of the Dealer's cards.
3. The objective of the game is for the Player to count their cards after they're dealt. If they're not satisfied with the number, they have the ability to 'Hit'. A hit allows the dealer to deal the Player one additional card. The Player can hit as many times as they'd like as long as they don't 'Bust'. A bust is when the Player is dealt cards that total more than 21.
4. If the dealer deals the Player cards equal to 21 on the first deal, the Player wins. This is referred to as Blackjack. Blackjack is NOT the same as getting cards that equal up to 21 after the first deal. Blackjack can only be attained on the first deal.
5. The Player will never see the Dealer's hand until the Player chooses to 'stand'. A Stand is when the player tells the dealer to not deal it anymore cards. Once the player chooses to Stand, the Player and the Dealer will compare their hands. Whoever has the higher number wins. Keep in mind that the Dealer can also bust.
"""
import random

SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
RANKS = [ 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
VALUES = {
    'Ace' : 11,
    'Two' : 2,
    'Three' : 3,
    'Four' : 4,
    'Five' : 5,
    'Six' : 6,
    'Seven' : 7,
    'Eight' : 8,
    'Nine' : 9,
    'Ten' : 10,
    'Jack' : 10,
    'Queen' : 10,
    'King' : 10
}

is_playing = True

class Card():
    def __init__(self,suits,rank):
        self.suit = suits
        self.rank = rank

    def __str__(self):
        return f'{self.rank} {self.suit}'

class Deck():
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' +card.__str__()
        return f'Deck: {deck_comp}'

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def take_card(self,card):
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 # count aces on hand
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chip():
    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def bet(chips):
    while True:
        try:
            chips.bet = int(input('How much do you want to bet? '))
        except ValueError:
            print('Please enter an integer number!')
        else:
            if chips.bet > chips.total:
                print('You cannot bet over what you have!')
            else: break

# add check blackjack: def has blackjack

def hit(deck,hand):
    hand.take_card(deck.deal())
    #hand.adjust_ace_value()

def hit_or_stand(deck,hand):
    global is_playing

    while True:
        choice = input('\nHit (h) or Stand (s)? ')
        if choice[0].lower() == 'h':
            hit(deck,hand)
        elif choice[0].lower() == 's':
            print("Player stands")
            is_playing = False
        else:
            print("Please enter only 's' or 'h!") #handle input error
            continue
        break

def show_card(player, dealer):
    print(f"\nDEALER's Hand: <hidden card>\t{dealer.cards[1]}")
    print("DEALER'S SCORE:", VALUES[dealer.cards[1].rank])
    print("\nPLAYER's Hand: ", *player.cards,sep='\t')
    print("PLAYER SCORE: ", player.value)

def show_all(player,dealer):
    print("\n DEALER's Hand: ", *dealer.cards,sep='\t')
    print("\n DEALER'S Card Value:", dealer.value)
    print("\n PLAYER's Hand: ", *player.cards,sep='\t')
    print("\n PLAYER SCORE: ", player.value)

# results might happens
def player_busts(player, dealer,chips):
    print("\nPLAYER BURSTS!")
    chips.lose_bet()

def player_wins(player, dealer,chips):
    print("\nPLAYER WINS!")
    chips.win_bet()

def dealer_bursts(player, dealer,chips):
    print("\nDEALER BURSTS!")
    chips.win_bet()

def dealer_wins(player, dealer,chips):
    print("\nDEALER WINS!")
    chips.lose_bet()

def push(player, dealer):
    print("It's a Push! Player and Dealer Tie!")

#play Game
while True:
    print("Welcome to BlackJack!")

    # assign player's chips
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.take_card(deck.deal())
    player_hand.take_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.take_card(deck.deal())
    dealer_hand.take_card(deck.deal())

    player_chips = Chip()
    bet(player_chips)

    #check BlackJack
    if player_hand.value == 21: #round ends 1
        show_all(player_hand, dealer_hand)
        if dealer_hand.value != 21:
            print("Player got BLACKJACK!")
            print("PLAYER WINS!")
            player_wins(player_hand, dealer_hand, player_chips)
            print("Player have total: ", player_chips.total)
        if dealer_hand.value == 21:
            show_all(player_hand, dealer_hand)
            print("Both Player and Dealer got BalckJack! It's a Tie!")
        
        new_round = input("Would you like to play another round? (y/n): ")
        if new_round[0].lower() == 'y':
            is_playing = True
            continue
        else:
            print("Thanks for playing!")
            break

    if dealer_hand.value == 21: #round ends 2
        show_all(player_hand, dealer_hand)
        print("Dealer got BLACKJACK!")
        print("DEALER WINS!")
        dealer_wins(player_hand, dealer_hand, player_chips)
        print("Player have total: ", player_chips.total)
        
        new_round = input("Would you like to play another round? (y/n): ")
        if new_round[0].lower() == 'y':
            is_playing = True
            continue
        else:
            print("Thanks for playing!")
            break


    # There is no BlackJack
    else: show_card(player_hand,dealer_hand)

    while is_playing:
        hit_or_stand(deck, player_hand)
        show_card(player_hand, dealer_hand)

        if player_hand.value >21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    while player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)

        if dealer_hand.value >21:
            dealer_bursts(player_hand, dealer_hand,player_chips) # round ends
            break

        if dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
            break

        if dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand,player_chips)
            break

        if dealer_hand.value == player_hand.value:
            push(player_hand, dealer_hand)
            break

    print("\nPlayer have total: ", player_chips.total)

    new_round = input("\nWould you like to play another round? (y/n): ")
    if new_round[0].lower() == 'y':
        is_playing = True
        continue
    else:
        print("Thanks for playing!")
        break

    