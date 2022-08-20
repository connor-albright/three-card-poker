from abc import ABC
from enum import Enum

class HandType(Enum):
    """This class represents the possible hands that can be obtained"""
    HIGH_CARD = 0
    PAIR = 1
    FLUSH = 2
    STRAIGIHT = 3
    THREE_OF_A_KIND = 4
    STRAIGHT_FLUSH = 5

    def __gt__(self, other):
        """Greater than override."""
        return self.value > other.value

    def __le__(self, other):
        """Less than or equal to override."""
        return self.value <= other.value
        
class Player(ABC):
    """This class represents the actions of the user or dealer (abstract)"""
    def __init__(self):
        """Constructs the Player abstract class."""
        self.hand = tuple()
        
    def set_hand(self, cards: tuple):
        """Sets the hand of the player.
        Args:
            cards (tuple): Cards that the hand is set as in a tuple.
        Raises:
            TypeError: if cards do not get set as a tuple while this function is called.
        """
        if isinstance(cards, tuple): 
            self.hand = cards
        else:
            raise TypeError('cards must be a tuple')

    def discard_hand(self):
        temp = [card for card in self.hand]
        self.hand = tuple()
        return temp
    
    def has_pair(self):
        """Checks to see if hand has a pair.
        Returns:
            int: if the length of hand returns as 2, the user has a pair since
            duplicates are disregarded.
        """
        return len(set([card.card_value for card in self.hand])) == 2
    
    def has_flush(self):
        """Checks hand for flush.
        Returns:
            int: if the length of hand returns as 1, the user has a flush since
            duplicates are disregarded. Suit of card is evaluated.
        """
        return len(set([card.card_suit for card in self.hand])) == 1
    
    def has_straight(self):
        """Checks hand for a straight.
        Returns:
            tuple: checks values of cards and sorts them as 1, 2, 3 if in sequential order 
            and returns a straight if conditions are met.
        """
        sorted_hand = sorted(self.hand)
        lowest_card_val = sorted_hand[0].card_value - 1
        sorted_hand = [x.card_value - lowest_card_val for x in sorted_hand]
        return sorted_hand == (1, 2, 3)
    
    def has_three_pair(self):
        """Checks hand for three of a kind.
        Returns:
            int: if the length of hand returns as 1, the user has a flush since
            duplicates are disregarded. Value of card is evaluated.
        """        
        return len(set([card.card_value for card in self.hand])) == 1
    
    def evaluate_hand(self):
        """Evaluates the hand of the Player and returns a tuple containing
        handtype and highcard so when comparing two hands it can determine the winner of the
        round based on either parameter if the handtype returns the same
        Returns:
            tuple(HandType, High Card): returns the user's hand as a tuple
        """
        highest_card = max(self.hand)
        
        if self.has_straight() and self.has_flush():
            return HandType.STRAIGHT_FLUSH, highest_card
        elif self.has_three_pair():
            return HandType.THREE_OF_A_KIND, highest_card
        elif self.has_straight():
            return HandType.STRAIGIHT, highest_card
        elif self.has_flush():
            return HandType.FLUSH, highest_card
        elif self.has_pair():
            return HandType.PAIR, highest_card
        else:
            return HandType.HIGH_CARD, highest_card
        
class Dealer(Player):
    """This class represents the dealer's parameters"""
    
    def __init__(self):
        """Constructs the dealer class as a subclass of player."""
        super().__init__() 
    
    def reveal_hand(self):
        """Changes bool value of card to be interpreted by the view to show the cards"""
        for card in self.hand:
            card.face_up = True

class User(Player):
    """This class represents the user's parameters"""
    INITIAL_MONEY = 250.0
    
    def __init__(self, money=INITIAL_MONEY):
        """Constructs the user class as a subclass of player.
        Args:
            money (float): Overall balence of the player. Defaults to INITIAL_MONEY.
        """
        super().__init__()
        self.money = money
         
    def place_bet(self, amount):
        """Removes money from the user's money in game when prompted to bet
        Args:
            amount (_type_): amount the user has bet on the round
        Raises:
            ValueError: if the user places a bet larger the balence in money
        """
        if amount > self.money:
            raise ValueError('Invalid Bet: Insufficient Funds')
        else:
            self.money -= amount
