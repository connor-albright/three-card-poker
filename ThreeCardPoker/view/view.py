from io import UnsupportedOperation
import PySimpleGUI as sg

from model.model import Model

class View:
    """This class represents the view of the game, controlling the visual aspects of each stage of the game."""
    def __init__(self, model=Model(), display='menu') -> None:
        """Constructs a view for a given display input given
        Args:
            model (_type_): the model the view is constructed from.
            display (str): selects the specific view needed for a certain stage in the game.
            card_image_dict (dict): maps each card to respective image path
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
        if self.window != sg.WIN_CLOSED:
            return self.window.Read()
        else:
            raise ValueError('Tried to read closed window')
    
    def refresh(self):
        self.window.refresh()
    