from model.model import Model
from view.view import View

class Controller:
    """Represents controller of the game."""
    def __init__(self, model=Model()) -> None:
        """Constructs controller for the given model.
        Args:
            model (_type_): model that is controlled
        """
        self.model = model
        self.view = View(model=self.model)
        self.ANTE = 25
        
    def start_round(self):
        """Round start stage of the game. Updates model and view
        Returns:
            _type_: None or -1
        """
        self.model.winner = None
        self.model.round_over = False
        self.model.game_over = False
        self.model.pot = 0
        self.model.pair_plus = 0
        
        self.model.deck.return_used_cards(self.model.user.discard_hand())
        self.model.deck.return_used_cards(self.model.dealer.discard_hand())
        self.view.curr_display = 'prebet'
       
        try:   
            self.model.place_bet(self.ANTE)
        except ValueError:
            self.model.game_over = True
            return -1
        
        self.view.display()
        event, values = self.get_events_values()
        
        while event != 'Bet':
            pass
        
        pair_plus = values['PreBet-Slider']
        
        while True:
            try:
                self.model.place_pair_plus(amount=pair_plus)
                break
            except ValueError:
                pass
        
        self.model.deal_hands()
        
    def play_round(self):
        """Betting stage of game. Updates model and view.
        Returns:
            _type_: None or -1
        """
        self.view.curr_display = 'bet'
        self.view.display()
        event = ''
        while event != 'Bet':
            if event == 'Fold':
                return -1
            
            event, values = self.get_events_values()
            
        
        while True:
            event, values = self.get_events_values()
            play_wager = values['Bet-Slider']
            try:
                self.model.place_bet(amount=play_wager)
                break
            except ValueError:
                pass
        
    def end_round(self):
        """Evauation stage of game. Updates model and view."""
        if self.model.compare_hands():
            self.model.user.money += self.model.get_pot()
        
        self.model.round_over = True
        self.view.curr_display = 'postbet'
        self.view.display()
        
    def go(self):
        """Runs the game in a sequential order.
        Returns:
            _type_: self.go() or None.
        """
        self.view.display()
        while True:  
            event,_ = self.get_events_values()          
            if event == 'Quit':
                break
            if event == 'Start' or event == 'Next Round' or event == 'Fold':        
                if self.start_round() is not None:
                    self.gameover()
                    event,_ = self.get_events_values()          
                    if event == 'Quit':
                        return
                    elif event == 'Play Again':
                        #self.model.user.money = self.model.user.INITIAL_MONEY
                        #self.model.deck
                        self.model = Model()
                        self.view = View(self.model)
                        self.view.curr_display = 'prebet'
                        return self.go()
                if self.play_round() is not None:
                    continue
                self.end_round()

    def gameover(self):
        """Calls the gameover display if conditions are met."""
        self.view.curr_display = 'gameover'
        self.view.display()
    
    def query_pair_plus(self):
        """Updates view to the prebet display."""
        self.view.curr_display = 'prebet'
        self.view.display()

    def query_bet(self):
        """Updates ciew to bet display."""
        self.view.curr_display = 'bet'
        self.view.display()
        
    def get_events_values(self):
        """Retrieves the events and values given from the view
        Returns:
            events, values: value changes and events triggered in the view"""
        return self.view.get_events_values()
