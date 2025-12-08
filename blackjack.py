import random, sys


# Set up the constants
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = 'backside'


def main():
    print("""
    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.
    """)

    money = 5000
    # Main game loop
    while True:
        # Check if the player has run out of money:
        if money <= 0:
            print("You're broke!")
            print("Good thing you weren't playing with real money.")
            print("Thanks for playing!")
            sys.exist()

        # Let the player enter their bet for this round:
        print("Money: ", money)
        bet = getBet(money)

        # Give the dealer and the player two cards from the deck each:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Handle player actions:
        print("Bet:", bet)
        # Keep looping until player stands or busts
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            # check if the player has bust:
            if getHandValue(playerHand) > 21:
                break

            # Get the player's move, either H, S, D:
            move = getMove(playerHand, money-bet)

            # handle the player actions
            if move == 'D':
                # player is doubling down, they can increase their bet:
                additionalBet = getBet(min(bet, (money-bet)))
                bet += additionalBet
                print("Bet increased to {}".format(bet))
                print("Bet:", bet)

            if move in ("H", "D"):
                # Hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print(f"You drew a {rank} of {suit}")
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # the player has busted
                    continue
            if move in ('S', 'D'):
                # Stand/doubling down stops the player's turn
                break

        # Handle the dealer actions:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # the dealer hits
                print("Dealer hits...")
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    # The dealer has busted
                    break
                input("Press Enter to cotinue...")
                print("\n\n")

            # show the final hands
            displayHands(playerHand, dealerHand, True)

            playerValue = getHandValue(playerHand)
            dealerValue = getHandValue(dealerHand)
            # Handle whether the player won, lost or tied:
            if dealerValue > 21:
                print(f"Dealer busts! You win ${bet}")
                money += bet
            elif (playerValue > 21) or (playerValue < dealerValue):
                print("You lost!")
                money -= bet 
            elif playerValue == dealerValue:
                print("It's a tie, the bet is returned to you")

            input("Press Enter to continue...")
            print("\n\n")


def getBet(maxBet):
    """Ask the player how much they want to bet for this round."""
    # Keep asking until they enter a valid amount
    while True:
        print(f"How much do you bet? (1-{maxBet}, or QUIT)")
        bet = input("> ").upper().strip()
        if bet == "QUIT":
            print("Thanks for playing!")
            sys.exit()

        if not bet.isdecimal():
            continue
        
        bet = int(bet)
        if 1 <= bet <= maxBet:
            # Player entered a valid bet
            return bet


def getDeck():
    """Return a list of (rank, suit) tuples for all 52 cards."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            # Add the numbered cards
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'): # Add the face and ace cards
            deck.append(rank, suit)
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the player's and dealer's cards. Hide the dealer's first
    card if showDealerHand is False."""
    print()
    if showDealerHand:
        print("DEALER:", getHandValue(dealerHand))
        displayCards(dealerHand)


def getHandValue(cards):
    """Returns the value of the cards. Face cards are worth 10, aces are
    worth 11 or 1 (this function picks the most suitable ace value)."""
    value = 0
    number of Aces = 0

    # Add the value for the non-ace cards:
    for card in cards:
        # card is a tuple like (rank, suit)
        rank = card[0]
        if rank == "A":
            numberOfAces += 1
        # Face cards are worth 10 points
        elif rank in ('K', 'Q', 'J'):
            value += 1
        # Numbered cards are worth their number
        else:
            value += int(rank)
    
    # Add the value for aces:
    # Add 1 per ace 
    value += numberOfAces
    for i in range(numberOfAces):
        # If another 10 can be added without busting, do so:
        if value + 10 <= 21:
            value += 10

    return value


displayCards(cards):
    """Display all the cards in the cards list"""
    # The text to display on each row
    row = ['', '', '', '']

    for i, card in enumerate(cards):
        # print the top line of the card
        row[0] += ' ___  '
        if card == BACKSIDE:
            rows[1] += "|## | "
            rows[2] += "|###| "
            rows[3] += "|_##| "
        else:
            # print the card's front
            # The card is a tuple data structure
            rank, suit = card
            rows[1] += "|{} | ".format(rank.ljust(2))
            rows[2] += "| {} | ".format(suit)
            rows[3] += "|_{}| ".format(rank.rjust(2, '_'))

    # print each row on the screen
    for row in rows:
        print(row)


def getMove(playerHand, money):
    """Asks the player for their move and returns 'H' for hit, 'S' for
    stand, 'D' for double down"""
    # Keep looping until the player enter a correct move
    while True:
        # Determine what moves the player can make:
        moves = ['(H)it', '(S)tand']

        # The player can double down on their first move, which we can 
        # tell because they'll have exactly 2 cards:
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Get the player move
        movePrompt = ', '.join(moves) + "> "
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            # Player has entered a valid move 
            return move
        if move == 'D' and "(D)ouble down" in moves:
            return move

if __name__ == '__main__':
    main()
