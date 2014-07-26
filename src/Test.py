from kivy.app import App
from kivy.garden.magnet import Magnet
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
 
from os import listdir
 
IMAGEDIR = './'
 
IMAGES = filter(
    lambda x: x.endswith('.png'),
    listdir(IMAGEDIR))

counter = 0

kv = '''
FloatLayout:
    GridLayout:
        cols: 2
        rows: 2
    
        GridLayout:
            id: dealer_layout
            cols: 3
            rows: 3
            
            
        GridLayout:
            id: player_layout
            cols: 3
            rows: 3
            
          
        GridLayout:
            id: new_cards_layout
            cols: 5
            rows: 1

        GridLayout:
            id: empty_layout
            cols: 0
            rows: 0
            
      
                  
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
        dealer_layout = self.app.root.ids.dealer_layout
        player_layout = self.app.root.ids.player_layout
        cards_layout = self.app.root.ids.new_cards_layout
 
        if touch.grab_current == self:
            self.img.center = touch.pos
            if cards_layout.collide_point(*touch.pos):
                cards_layout.remove_widget(self)
                dealer_layout.remove_widget(self)
                #player_layout.add_widget(self)
                #player_layout.remove_widget(self)
 
                for i, c in enumerate(cards_layout.children):
                    if c.collide_point(*touch.pos):
                        cards_layout.add_widget(self, i - 1)
                        break
                else:
                    cards_layout.add_widget(self)
            else:
                if self.parent == cards_layout:
                    cards_layout.remove_widget(self)
                    dealer_layout.add_widget(self)
                    #player_layout.remove_widget(self)
                    #player_layout.add_widget(self)
 
                self.center = touch.pos
 
        return super(DraggableImage, self).on_touch_move(touch, *args)
 
    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            self.app.root.remove_widget(self.img)
            self.add_widget(self.img)
            touch.ungrab(self)
            return True
        return super(DraggableImage, self).on_touch_up(touch, *args)
 
 
class DnDMagnet(App):
    def build(self):
        self.root = Builder.load_string(kv)
        counter = 0
        
        for i in IMAGES:            
            image = Image(source=IMAGEDIR + i, size=(100, 100),
                          size_hint=(None, None))
            draggable = DraggableImage(img=image, app=self,
                                       size_hint=(None, None), pos_hint={'x': 0, 'center_y': .5},
                                       size=(100, 100))
            
            empty_image = Image(source="empty_square.png", size=(100, 100),
                          size_hint=(None, None))
            empty_draggable = DraggableImage(img=empty_image, app=self,
                                       size_hint=(None, None), pos_hint={'x': 0, 'center_y': .5},
                                       size=(100, 100))   
 
            if counter < 9:
                self.root.ids.dealer_layout.add_widget(empty_draggable)
            elif counter <= 17:
                self.root.ids.player_layout.add_widget(empty_draggable) 
            elif counter <= 22:
                self.root.ids.new_cards_layout.add_widget(draggable)  
            
            if counter == 22:
                break 
               
            counter += 1
            
        return self.root
 
 
if __name__ == '__main__':
    DnDMagnet().run()
