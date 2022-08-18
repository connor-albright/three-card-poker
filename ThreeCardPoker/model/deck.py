from random import sample
from model.card import Card

class Deck:
    def __init__(self):
        self.cards = set()
        for card_value in range(2, 15):
            for card_suit in Card.CardSuit:
                self.cards.add(Card(card_value=card_value, card_suit=card_suit, face_up=True))


    def get_n_cards(self, n, face_up: bool):
        n_cards = sample(self.cards, n)
        for card in n_cards:
            self.cards.remove(card)
            card.face_up = face_up
            
        return tuple(n_cards)
    
    def return_used_cards(self, used_cards):
        for card in used_cards:
            self.cards.add(card)

    def __repr__(self) -> str:
        return f'The Current Deck Has {len(self)} Cards Remaining'