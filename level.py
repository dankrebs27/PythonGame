import newrender  # @UnresolvedImport
import enemies  # @UnresolvedImport
import pygame

class Level(object):

    def __init__(self, map):
        self.map = map
        
        
    def load_level(self):
        maprender = newrender.NewRender(map)
        mapWidth, mapHeight = maprender.get_dims()
        #layersList = maprender.tmx_data.layers
        badguys = enemies.create_enemies(maprender)
        
        blockers = []
        for objs in maprender.tmx_data.objects:
            properties = objs.__dict__
            if properties['name'] == 'tree':
                x = properties['x'] 
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                blockers.append(new_rect)
                
        return mapWidth, mapHeight