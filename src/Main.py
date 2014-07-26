from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from functools import partial
import random
from kivy.graphics.texture import Texture
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.app import App
from kivy.garden.magnet import Magnet
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
 
from os import listdir


CARD_SIZE = (120.71, 172.14)
CARD_CENTER = (60.355, 86.07)

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

kv = '''
GridLayout:
    FloatLayout:
        GridLayout:
            id: grid_layout
            cols: int(self.width / 32)
 
        FloatLayout:
            id: float_layout
'''
 
 
 
class DraggableImage(Magnet):
    img = ObjectProperty(None, allownone=True)
    app = ObjectProperty(None)
 
    def on_img(self, *args):
        self.clear_widgets()
 
        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)
 
    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.remove_widget(self.img)
            self.app.root.add_widget(self.img)
            self.center = touch.pos
            self.img.center = touch.pos
            return True
 
        return super(DraggableImage, self).on_touch_down(touch, *args)
 
    def on_touch_move(self, touch, *args):
        grid_layout = self.app.root.ids.grid_layout
        float_layout = self.app.root.ids.float_layout
 
        if touch.grab_current == self:
            self.img.center = touch.pos
            if grid_layout.collide_point(*touch.pos):
                grid_layout.remove_widget(self)
                float_layout.remove_widget(self)
 
                for i, c in enumerate(grid_layout.children):
                    if c.collide_point(*touch.pos):
                        grid_layout.add_widget(self, i - 1)
                        break
                else:
                    grid_layout.add_widget(self)
            else:
                if self.parent == grid_layout:
                    grid_layout.remove_widget(self)
                    float_layout.add_widget(self)
 
                self.center = touch.pos
 
        return super(DraggableImage, self).on_touch_move(touch, *args)
 
    def on_touch_up(self, touch, *args):
        #if touch.grab_current == self:
            #self.app.root.remove_widget(self.img)
            #self.add_widget(self.img)
            #touch.ungrab(self)
            #return True
 
        return super(DraggableImage, self).on_touch_up(touch, *args)

 
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def get_value(self):
        return VALUES[self.get_rank()]   
    
    def get_loc(self, wid, pos):
        card_loc = (CARD_CENTER[0] +  CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
          
        

class Hand:
    def __init__(self, app):
        self.hand = []
        self.app = app
        
    def add_card(self, card):
        self.hand.append(card) 
    
    def draw(self, wid, location, *largs):
        global random_card
        for x in self.hand:
            random_card = random.choice(['10_of_clubs.png',
'10_of_diamonds.png',
'10_of_hearts.png',
'10_of_spades.png',
'2_of_clubs.png',
'2_of_diamonds.png',
'2_of_hearts.png',
'2_of_spades.png',
'3_of_clubs.png',
'3_of_diamonds.png',
'3_of_hearts.png',
'3_of_spades.png',
'4_of_clubs.png',
'4_of_diamonds.png',
'4_of_hearts.png',
'4_of_spades.png',
'5_of_clubs.png',
'5_of_diamonds.png',
'5_of_hearts.png',
'5_of_spades.png',
'6_of_clubs.png',
'6_of_diamonds.png',
'6_of_hearts.png',
'6_of_spades.png',
'7_of_clubs.png',
'7_of_diamonds.png',
'7_of_hearts.png',
'7_of_spades.png',
'8_of_clubs.png',
'8_of_diamonds.png',
'8_of_hearts.png',
'8_of_spades.png',
'9_of_clubs.png',
'9_of_diamonds.png',
'9_of_hearts.png',
'9_of_spades.png',
'ace_of_clubs.png',
'ace_of_diamonds.png',
'ace_of_hearts.png',
'ace_of_spades.png',
'jack_of_clubs.png',
'jack_of_diamonds.png',
'jack_of_hearts.png',
'jack_of_spades.png',
'king_of_clubs.png',
'king_of_diamonds.png',
'king_of_hearts.png',
'king_of_spades.png',
'queen_of_clubs.png',
'queen_of_diamonds.png',
'queen_of_hearts.png',
'queen_of_spades.png'])
            
            with wid.canvas:
                image = Image(source = random_card, pos = location, size = (100, 100))
                self.app.add_image(image)
                
class Deck:
    def __init__(self): 
        self.deck = []
        for x in RANKS:
            for y in SUITS:
                self.deck.append(Card((y), (x)))
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal_card(self):
        self.card = self.deck[0]
        self.deck.remove(self.card)
        return self.card
    
def deal(wid, app):
    global my_deck, player_hand, dealer_hand
    my_deck = Deck()
    my_deck.shuffle()
    
    player_hand = Hand(app)
    dealer_hand = Hand(app)
    
    player_hand.add_card(my_deck.deal_card()) 
    dealer_hand.add_card(my_deck.deal_card())
    '''
    player_hand.add_card(my_deck.deal_card())  
    dealer_hand.add_card(my_deck.deal_card())
    player_hand.add_card(my_deck.deal_card())    
    dealer_hand.add_card(my_deck.deal_card())
    player_hand.add_card(my_deck.deal_card())    
    dealer_hand.add_card(my_deck.deal_card())
    player_hand.add_card(my_deck.deal_card())    
    dealer_hand.add_card(my_deck.deal_card())
    '''
    player_hand.draw(wid, (200, 100))
    dealer_hand.draw(wid, (350, 100))

                              
class CanvasApp(App):
    
    root = Builder.load_string(kv)
           
    def add_cards(self, wid, *largs):        
        with wid.canvas:                        
            deal(wid, self)       

    def add_image(self, image):
        draggable = DraggableImage(img=image, app=self,
                                       size_hint=(None, None),
                                       size=(100, 100))
                            
        self.root.add_widget(draggable)
        
    def reset_rects(self,wid, *largs):
        wid.canvas.clear()
 
    def build(self):
        wid = Widget()
        btn_add = Button(text='Draw cards',on_press=partial(self.add_cards, wid,'Adding a rectangle'))
        #btn_clear = Button(text='Clear',on_press=partial(self.reset_rects, wid,'Clear the canvas'))
        
        
        DealerHandLabel = Label(text = "Dealer Hand", font_size = 20, pos = (350, 300))
        PlayerHandLabel = Label(text = "Player Hand", font_size = 20, pos = (200, 300))
        
        #layout = GridLayout()
        CanvasApp.root.add_widget(btn_add)
        #layout.add_widget(btn_clear)
        CanvasApp.root.add_widget(DealerHandLabel)
        CanvasApp.root.add_widget(PlayerHandLabel)
        CanvasApp.root.add_widget(wid)
        
        return CanvasApp.root

if __name__ == '__main__':
    CanvasApp().run()  