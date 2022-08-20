import PySimpleGUI as sg

from model.model import Model

class View:
    """This class represents the view of the game, controlling the visual aspects of each stage of the game."""
    def __init__(self, model=Model(), display='menu') -> None:
        """Constructs a view for a given display input given
        Params:
            model (_type_): the model the view is constructed from.
            display (str): selects the specific view needed for a certain stage in the game.
            card_image_dict (dict): maps each card to respective image path - [0] gets image for 'card back'
            window (layout): initial window layout for the game, used to get events and values from the view
        """
        self.model = model
        self.curr_display = display
        self.window = [
            [sg.Text('Welcome to Three Card Poker!', justification='center', font=('Cooper Black', 50), size=(60, 1))],
            [sg.Frame(
                layout=[[sg.Button('Start', bind_return_key=True, size=(15, 1)),
                         sg.Button('Quit', size=(15, 1))]],
                title='',
                border_width=0
            )]
        ] 
        self.card_image_dict = {card.__hash__(): ('resources/cards/' + str(card.card_value) + str(card.card_suit.name[0]) + '.png') for card in self.model.deck.cards}
        self.card_image_dict[0] = 'resources/cards/card_back.png'
        
        
    def menu(self):
        """Updates view to the welcome screen of the game, called by the display function."""
        window_title = 'Welcome to Three Card Poker!'
        layout = [
            [sg.Text(window_title, justification='center', font=('Cooper Black', 50), size=(60, 1))],
            [sg.Frame(
                layout=[[sg.Button('Start', bind_return_key=True, size=(15, 1)),
                         sg.Button('Quit', size=(15, 1))]],
                title='',
                border_width=0
            )]
        ] 
        
        window =sg.Window(window_title, size=(1150, 840), background_color='#006600', layout=layout).Finalize()
        self.curr_loc = window.CurrentLocation()
        self.curr_size = window.Size
        self.window = window
    
    def preBet(self):
        """Updates view to the prebet stage of the game where the user bets on the pair
        plus, called by the display function."""    
        msg = 'Pair Plus Bet (Bet on your hand)\t Money: $' + str(self.model.user.money) + '\t Pot: $' + str(self.model.get_pot()) + '\t Pair Plus: $' + str(self.model.pair_plus)
        layout = [
            [sg.Text(msg, justification='center', font=('Cooper Black', 25), size=(60, 1))],
            [sg.Frame(
                layout=[[sg.Slider(range=(0, self.model.user.money), orientation='h', relief='flat',
                                   border_width=0, background_color='White', size=(50, 15), key='PreBet-Slider')],
                         [sg.Button('Bet', size=(15, 1))]],
                title='',
                border_width=0
            )]
        ]
        window =sg.Window(title=msg, size=(1150, 840), background_color='#006600', layout=layout).Finalize()
        self.curr_loc = window.CurrentLocation()
        self.curr_size = window.Size
        self.window = window

    def bet(self):   
        """Updates view to the betting stage of the game where the user bets on the play
        wager and can also fold, called by the display function.""" 
        window_title = 'Place a Bet or Fold\t Money: $' + str(self.model.user.money) + '\t Pot: $' + str(self.model.get_pot()) + '\t Pair Plus: $' + str(self.model.pair_plus)
        layout = [
            [sg.Text(window_title, justification='center', font=('Cooper Black', 25), size=(60, 1))],
            [sg.Image(self.card_image_dict[card.__hash__()]) for card in sum(self.model.get_cards_on_table(), ())],
            [sg.Frame(
                layout=[[sg.Slider(range=(10, self.model.user.money), orientation='h', relief='flat',
                                   border_width=0, background_color='White', size=(50, 15), key='Bet-Slider')],
                         [sg.Button('Bet', size=(15, 1))],
                         [sg.Button('Fold', size=(15, 1))]],
                title='',
                border_width=0
            )]
        ] 
        
        window =sg.Window(window_title, size=(1150, 840), background_color='#006600', layout=layout).Finalize()
        self.curr_loc = window.CurrentLocation()
        self.curr_size = window.Size
        self.window = window
        
    def postBet(self): 
        """Updates view to the post bet stage of the game, where the winner determines
        the message given by the game where the user can either quit or go on the next round.
        Called by the display function."""
        verb = ''
        if self.model.winner is not None:
            if self.model.winner:
                verb = ' won '
            else:
                verb = ' lost '
        else:
            ValueError('No winner assigned')
        
        self.model.dealer.reveal_hand()
        v = 'You' + verb + ' $' + str(self.model.get_pot() + self.model.get_pair_plus())
        
        layout = [
            [sg.Text(v, justification='center', font=('Cooper Black', 25), size=(60, 1))],
            [sg.Image(self.card_image_dict[card.__hash__()]) for card in sum(self.model.get_cards_on_table(), ())],
            [sg.Frame(
                layout=[[sg.Button('Next Round', size=(15, 1))],
                        [sg.Button('Quit', size=(15, 1))]],
                title='',
                border_width=0
            )]
        ]   
        
        window =sg.Window(title=v, size=(1150, 840), background_color='#006600', layout=layout).Finalize()
        self.curr_loc = window.CurrentLocation()
        self.curr_size = window.Size
        self.window = window
        
    def gameOver(self):
        """Updates the view to the game over stage of the game where the user can either restart the game or quit.
        Called by the display function."""
        window_title = 'Game Over!'
        layout = [
            [sg.Text(window_title, justification='center', font=('Cooper Black', 50), size=(60, 1))],
            [sg.Frame(
                layout=[[sg.Button('Play Again', bind_return_key=True, size=(15, 1)),
                         sg.Button('Quit', size=(15, 1))]],
                title='',
                border_width=0
            )]
        ]  
        
        window =sg.Window(window_title, size=(1150, 840), background_color='#006600', layout=layout).Finalize()
        self.curr_loc = window.CurrentLocation()
        self.curr_size = window.Size
        self.window = window

    def display(self):
        """Changes the 'display' of the view, where the stage is called from specified functions to
        return the window and layout for said stage
        Stages:
            'menu': menu(), Inital game layout (Event(s): 'Start', 'Quit', Value(s): None)
            'prebet': preBet(), pairplus layout (Event(s): 'Bet', Value(s): 'PreBet-Slider')
            'bet': bet(), play-wager layout (Event(s): 'Bet', 'Fold', Value(s): 'Bet-Slider')
            'postbet': postBet(), hand evaluation layout (Event(s): 'Next Round', 'Quit', Value(s): None)
            'gameover': gameOver(), end game layout (Event(s): 'Play Again', 'Quit', Value(s): None)
        Raises:
            NotImplementedError: in the case of an invalid display option given from the controller
        """
        if self.curr_display == 'menu':
            self.menu()
        else:
            if self.window != sg.WIN_CLOSED:
                self.window.close()
            
            if self.curr_display == 'prebet':
                self.preBet()
            elif self.curr_display == 'bet':
                self.bet()
            elif self.curr_display == 'postbet':
                self.postBet()
            elif self.curr_display == 'gameover':
                self.gameOver()
            else:
                raise NotImplementedError(self.curr_display + ' is not a valid display option')
        
    def get_events_values(self):
        """Gets events and values from the window of the current display.
        Raises:
            ValueError: if the program attempts to read a window which was already
            closed
        Returns:
            events, values: values and events given by the window.
        """
        if self.window != sg.WIN_CLOSED:
            return self.window.Read()
        else:
            raise ValueError('Tried to read closed window')
    
    def refresh(self):
        """Refreshes current window."""
        self.window.refresh()
    
