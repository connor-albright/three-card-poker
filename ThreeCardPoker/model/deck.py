from random import sample
from model.card import Card

class Deck:
    """This represents the class for the deck."""
    def __init__(self):
        """Constructs the class Deck(). Creates a set of all 52 cards with value and suit."""
        self.cards = set()
        for card_value in range(2, 15):
            for card_suit in Card.CardSuit:
                self.cards.add(Card(card_value=card_value, card_suit=card_suit, face_up=True))


    def get_n_cards(self, n, face_up: bool):
        """Gets 'n' cards as a random sample and returns said cards
        and if they are face up or not
        Args:
            n (int): number of cards.
            face_up (bool): determines if the card is faced up or not
        Returns:
            tuple: 'n' amount of cards in a tuple.
        """
        n_cards = sample(self.cards, n)
        for card in n_cards:
            self.cards.remove(card)
            card.face_up = face_up
            
        return tuple(n_cards)
    
    def return_used_cards(self, used_cards):
        """Returns cards back to the deck.
        Args:
            used_cards (tuple): said cards to be returned to the deck.
        """
        for card in used_cards:
            self.cards.add(card)

    def __repr__(self) -> str:
        """String representation of the Deck. Returns amount of cards
        left in the deck."""
        return f'The Current Deck Has {len(self)} Cards Remaining'
