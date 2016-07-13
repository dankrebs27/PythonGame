import pygame
from pytmx import *  # @UnusedWildImport
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

class NewRender(object):

    def __init__(self, filename):
        self.tmx_data = util_pygame.load_pygame(filename)

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(self.tmx_data)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (640,640))
        self.map_layer.zoom = 1

        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=0)
        
    def draw_map(self, display, playChar):
        # center the map/screen on our Hero
        #self.group.center(self.hero.rect.center)
        self.group.center(playChar.rect.center)
        # draw the map and all sprites
        self.group.draw(display)
    
    def get_dims(self):
        props = self.tmx_data.properties
        width = int(props['Width'])
        height = int(props['Height'])
        
        return width, height