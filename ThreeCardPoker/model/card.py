from enum import Enum

class Card:
    class CardSuit(Enum):
        """Enumerated class for card suit.
        Returns:
            str: suit of card.
        """
        SPADES = '♠'
        HEARTS = '♥'
        DAIMONDS = '♦'
        CLUBS = '♣'
        
        def get_color(self):
            """Gets color of card based on suit
            Returns:
                str: whether the card is black or red
            """
            if self.name == 'SPADES' or self.name == 'CLUBS':
                return 'BLACK'
            else:
                return 'RED'
    
    class CardValue(Enum):
        """Enumerated class for card values."""
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        JACK = 11
        QUEEN = 12
        KING = 13
        ACE = 14
    
    def __init__(self, card_value: CardValue, card_suit: CardSuit, face_up: bool) -> object:
        """Constructs the class for cards where each card has a value, suit, and face-up option
        Args:
            card_value (CardValue): value of the card.
            card_suit (CardSuit): suit and color of card.
            face_up (bool): determines if the card will be shown face up or down
        Returns:
            object: card.
        """
        self.card_value = card_value
        self.card_suit = card_suit
        self.face_up = face_up
        
        
    def get_color(self):
        """Gets the color of the card.
        Returns:
            str: color of card. Black or Red.
        """
        return self.card_suit.get_color()
        
    def __repr__(self) -> str:
        """String representation of the object 'Card'.
        Returns:
            str: value of suit. ex: Ace of Spades.
        """
        return str(f'{self.card_value} of {self.card_suit}')

    def __ge__(self, other):
        """Greater than or equal to override."""
        return self.card_value >= other.card_value
    
    def __lt__(self, other):
        """Less than override."""
        return self.card_value < other.card_value
    
    def __hash__(self) -> int:
        """Overrides hash function to return the hash value of the state of the card."""
        if self.face_up == False:
            return 0
        else:
            return hash(self.card_value) + hash(self.card_suit) + 1
