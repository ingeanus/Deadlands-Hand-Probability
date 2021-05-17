import random
from copy import deepcopy
from itertools import combinations
from math import ceil
from DefineHand import defineHand

class Card:
    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank

    def __str__(self):
        return (str(self.rank) + " of " + self.suite)
    
    def __lt__(self, other):
        return self.rank < other.rank

    def __iter__(self):
        return CardIterator(self)

class CardIterator:
    def __init__(self, card):
        self.card = card
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == 1:
            return self.card.suite
        elif self.index == 2:
            return self.card.rank
        else:
            raise StopIteration

def drawHand(size, deck):
    count = len(deck)
    hand = []
    for i in range(size):
        index = random.randint(0, count-1)
        hand.append(deck.pop(index))
        count -= 1
    return hand

handRanks = {
    "High": 1,
    "Ace": 2,
    "One Pair": 3,
    "Jacks": 4,
    "Two Pair": 5,
    "Three of a Kind": 6,
    "Straight": 7,
    "Flush": 8,
    "Full House": 9,
    "Four of a Kind": 10,
    "Straight Flush": 11,
    "Royal Flush": 12,
    "Dead Man's Hand": 13
}

def compareHand(handOne, handTwo):
    if handRanks[defineHand(handOne)] > handRanks[defineHand(handTwo)]:
        return 1
    elif handRanks[defineHand(handTwo)] > handRanks[defineHand(handOne)]:
        return -1
    return 0

def chooseHand(hand):
    count = len(hand)
    if count == 5:
        return hand

    bestHand = []
    for handSelect in combinations(hand, 5):
            if (compareHand(bestHand, handSelect) == -1):
                bestHand = handSelect
    return bestHand

baseDeck = []
jokerDeck = []

for suite in ["D", "H", "J", "S"]:
    for rank in [2,3,4,5,6,7,8,9,10,11,12,13,14]: # Aces = 14
        newCard = Card(suite, rank)
        #print(newCard)
        baseDeck.append(newCard)
        
redJoker = Card("R", 69)
blackJoker = Card("B", 69)
jokerDeck = deepcopy(baseDeck)
jokerDeck.append(redJoker)
jokerDeck.append(blackJoker)


timeBase = 100000
for handSize in range(5,8):
    handCounts = {
        "Dead Man's Hand": 0,
        "Royal Flush": 0,
        "Straight Flush": 0,
        "Four of a Kind": 0,
        "Full House": 0,
        "Flush": 0,
        "Straight": 0,
        "Three of a Kind": 0,
        "Two Pair": 0,
        "Jacks": 0,
        "One Pair": 0,
        "Ace": 0,
        "High": 0
    }

    loops = ceil(timeBase)
    cumulative = 0

    for i in range(loops):
        #if i%(loops/100) == 0:
        #    print("Hand: ", i)
        hand = drawHand(handSize, deepcopy(baseDeck))
        hand.sort()
        handCounts[defineHand(chooseHand(hand))] += 1

    print("HAND SIZE: ", handSize)
    print("LOOPS: ", loops)
    print("%-20s %-10s %-15s %s" % ("Hand", "Count", "Percentage", "Cumulative"))
    for handType, count in handCounts.items():
        cumulative += count
        print("%-20s %-10s %-15.3f %.3f" % (handType, count, count/loops*100, cumulative/loops*100))
