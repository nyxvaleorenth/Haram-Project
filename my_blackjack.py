import random
import sys   # for sys.exit()


# set up the constant
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = 'backside'


def main():
    pass


def getBet(maxBet):
    """ask the player how much they want to bet for this round"""
    # Keep asking until they enter a valid amout.
    while True:
        print(f"Enter the bet: (1 - {maxBet}, QUIT)")
        user_input = input('> ').upper().strip()

        if user_input == 'QUIT':
            print("Thanks for playing!")
            sys.exit()
        
        if not user_input.isdecimal():
            continue

        bet = int(user_input)
        if (1 <= bet <= maxBet):
            return bet


def getDeck():
    """return a list of (rank, suit) tuples for all 52 cards"""
    deck = []
    for suit in (HEARTS, SPADES, CLUBS, DIAMONDS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """show the player and dealer cards. hide the dealer first
    card if showDealerHand is False"""
    pass


def getHandValue(cards):
    """return the value of the cards. face cards are worth 10, aces are
    worth 11 or 1 (this function picks the most suitable ace value)"""
    value = 0
    nAces = 0

    for card in cards:
        rank = cards[0]
        if rank == 'A':
            nAces += 1
        elif rank in ('J', 'Q', 'K'):
            value += 10
        else:
            value += int(rank)

    value += nAces
    for i in nAces:
        if value + 10 <= 21:
            value += 10

    return value


def displayCards(cards):
    pass


def getMove(playerHand, money):
    pass
