from model.player import User, Dealer, HandType
from model.deck import Deck

class Model:
    """This class represents the game's model"""
    def __init__(self, user=User(), dealer=Dealer(), deck=Deck(), pot=0, pair_plus=0) -> None:
        """Constructs a model for the basis of the game. Controls the actions the user can
        perform such as folding, controlling the betting, dealing hands as well as comparing them.
        Args:
            user (_type_): Calls the user's functions. Defaults to User().
            dealer (_type_: Calls the dealer's functions. Defaults to Dealer().
            deck (_type_): Calls the deck's functions. Defaults to Deck().
            pot (int): Accumulates balance to return to the user if won. Defaults to 0.
            pair_plus (int): Returns appropriete amount dependent on the user's hand. Defaults to 0.
        """
        self.user = user
        self.dealer = dealer
        self.deck = deck
        self.pot = pot
        self.pair_plus = pair_plus
        self.round_over = False
        self.game_over = False
        self.winner = None
        
    def place_pair_plus(self, amount):
        self.user.place_bet(amount=amount)
        self.pair_plus = amount
    
    def place_bet(self, amount):
        self.user.place_bet(amount=amount)
        self.pot += amount

    def get_pair_plus(self):
        hand_type = self.user.evaluate_hand()[0]
        new_amount = 0.0
        if hand_type == HandType.STRAIGHT_FLUSH:
            new_amount = 40 * self.pair_plus
            self.user.money += new_amount
        elif hand_type == HandType.THREE_OF_A_KIND:
            new_amount = 30 * self.pair_plus
            self.user.money += new_amount
        elif hand_type == HandType.STRAIGIHT:
            new_amount = 6 * self.pair_plus
            self.user.money += new_amount    
        elif hand_type == HandType.FLUSH:
            new_amount = 4 * self.pair_plus
            self.user.money += new_amount    
        elif hand_type == HandType.PAIR:
            new_amount = self.pair_plus
            self.user.money += new_amount    
        
        self.pair_plus = 0
        return new_amount
             
    def fold(self):
        self.round_over = True
    
    def deal_hands(self):
        self.user.set_hand(self.deck.get_n_cards(n=3, face_up=True))
        self.dealer.set_hand(self.deck.get_n_cards(n=3, face_up=False))
    
    def compare_hands(self):
        """Using evaluate.hand() from user/dealer, compares the tuple returned by the function
        by first using the handtype of the hand and if the same, compares highcard to determine
        the winner.
        Returns:
            self.winner: winner of the round to be used in controller
        """
        user_hand = self.user.evaluate_hand()
        dealer_hand = self.dealer.evaluate_hand()
        
        if user_hand[0] == dealer_hand[0]:
            self.winner = user_hand[1] > dealer_hand[1]
            return self.winner
        else:
            self.winner = user_hand[0] > dealer_hand[0]
            return self.winner
        
    def get_pot(self):
        return self.pot
    
    def get_cards_on_table(self):
        return self.user.hand, self.dealer.hand