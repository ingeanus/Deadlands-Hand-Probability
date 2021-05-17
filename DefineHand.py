from copy import deepcopy

def defineHand(hand):
    if len(hand) == 0: # For an uninitialized list, just return High (All hands are at least a high)
        return "High"

    
    if deadMansHand(deepcopy(hand)): # These is usually a two pair hand, but certain hexes give amazing effects for this (ex: Soul Blast causes instant death)
        return "Dead Man's Hand"
    elif straightFlush(deepcopy(hand)) != False: # straightFlush() doesn't return True! Only type of Flush or False!
        return straightFlush(deepcopy(hand))
    elif fourOfAKind(deepcopy(hand)):
        return "Four of a Kind"
    elif fullHouse(deepcopy(hand)):
        return "Full House"
    elif flush(deepcopy(hand)):
        return "Flush"
    elif straight(deepcopy(hand)):
        return "Straight"
    elif threeOfAKind(deepcopy(hand)):
        return "Three of a Kind"
    elif twoPair(deepcopy(hand)):
        return "Two Pair"
    elif onePair(deepcopy(hand)) != False:
        return onePair(deepcopy(hand))
    elif ace(deepcopy(hand)):
        return "Ace"
    return "High"

def straightFlush(hand):
    i = 0
    ranks = [rank for suite,rank in hand]
    jokers = ranks.count(69)
    while (i < 4):
        if (hand[i].rank != 69):
            if (hand[i].rank != hand[i+1].rank-1 or 
                    hand[i].suite != hand[i+1].suite):
                if (jokers > 0):
                    jokers -= 1
                    hand[i+1].rank = hand[i+1].rank
                else:
                    return False
        i += 1

    return "Royal Flush" if royalFlush(hand) else "Straight Flush"
        
def royalFlush(hand):
    i = 0
    curRank = 10
    while (i < 5):
        if (hand[i].rank != curRank and hand[i].rank != 69):
            return False
        i += 1
        curRank += 1
    return True

def fourOfAKind(hand):
    ranks = [rank for suite,rank in hand]
    rankTypes = set(ranks)
    if len(rankTypes) != 2:
       if (69 not in rankTypes or len(rankTypes) > 3):
           return False
    for r in rankTypes:
        if (ranks.count(r) + ranks.count(69)) == 4:
            return True
    return False

def fullHouse(hand):
    ranks = [rank for suite,rank in hand]
    rankTypes = set(ranks)
    if len(rankTypes) != 2:
       if (69 not in rankTypes or len(rankTypes) > 3):
           return False
    for r in rankTypes:
        if (ranks.count(r) + ranks.count(69)) == 3:
            return True
    return False

def flush(hand):
    suites = [suite for suite,rank in hand]
    suiteTypes = set(suites)
    if len(suiteTypes) > 1:
        if len(suiteTypes) - suites.count("R") - suites.count("B") != 1:
            return False
    return True

def straight(hand):
    ranks = [rank for suite,rank in hand]
    i = 0
    while i < 4:
        if ranks[i] != ranks[i+1]-1:
            return False
        i += 1
    return True

def threeOfAKind(hand):
    ranks = [rank for suite,rank in hand]
    rankTypes = set(ranks)
    if len(rankTypes) <= 2:
        return False
    for r in rankTypes:
        if (ranks.count(r) + ranks.count(69)) == 3:
            return True
    return False

# In most cases, this is just a normal two pair. However some hexes have special effects (Ex: Soul Blast gives instant death with this hand)
# This hand specifically is 2 black 8s, 2 black Aces, jack of Diamonds.
def deadMansHand(hand):
    for card in hand:
        if card.suite == "H": # If there are any hearts, it's false
            return False
        elif card.suite == "D": # If there's a diamond, it has to be the Jack
            if card.rank != 11:
                return False
        else: # For the black suites..
            if card.rank != 8 and card.rank != 14: # If it's not an 8 and not an Ace, return false.
                return False
    return True

# The hilarious thing about twoPairs, is that jokers don't matter! 
# If you have one Joker, match it with the existant pair and get a Three of a Kind. 
# If you have two Jokers, match it with any card and get a Three of a Kind.
# Therefore this code doesn't even care for jokers
def twoPair(hand):
    ranks = [rank for suite,rank in hand]
    rankTypes = set(ranks)
    pairs = [r for r in rankTypes if (ranks.count(r) == 2)]
    if len(pairs) == 2:
        return True
    return False

# Now the same for Two Pair cannot be said for One Pair of course
def onePair(hand):
    ranks = [rank for suite,rank in hand]
    rankTypes = set(ranks)
    if (ranks.count(69) > 0): # If you have even a single Joker and you haven't matched to anything above a One Pair, you can pair with literally any card!
        return True
    pairs = [r for r in rankTypes if (ranks.count(r) == 2)]
    if len(pairs) == 1:
        if pairs[0] >= 11:
            return "Jacks"
        return "One Pair"
    return False

# This is a Ace High. A small selection of hexes use this one in particular
def ace(hand):
    ranks = [rank for suite,rank in hand]
    if 14 in ranks:
        return True
    return False