from enum import Enum

class Card:
    class CardSuit(Enum):
        SPADES = '♠'
        HEARTS = '♥'
        DAIMONDS = '♦'
        CLUBS = '♣'
        
        def get_color(self):
            if self.name == 'SPADES' or self.name == 'CLUBS':
                return 'BLACK'
            else:
                return 'RED'
    
    class CardValue(Enum):
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
        self.card_value = card_value
        self.card_suit = card_suit
        self.face_up = face_up
        
        
    def get_color(self):
        return self.card_suit.get_color()
        
    def __repr__(self) -> str:
        return str(f'{self.card_value} of {self.card_suit}')

    def __ge__(self, other):
        return self.card_value >= other.card_value
    
    def __lt__(self, other):
        return self.card_value < other.card_value
    
    def __hash__(self) -> int:
        if self.face_up == False:
            return 0
        else:
            return hash(self.card_value) + hash(self.card_suit) + 1