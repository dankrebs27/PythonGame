from pygame import *  # @UnusedWildImport
import player  # @UnresolvedImport

class CollisionHandler(object):
    def __init__(self, thing, enemies, blockers):
        self.thing = thing
        self.thingRect = thing.rect
        self.enemies = enemies
        self.blockers = blockers
    
    def collided(self):
        for item in self.enemies:
            if self.thingRect.colliderect(item) and self.thingRect != item:
                return self.thing.direction
            else:
                return False
    
    def collided_on(self):
        for item in self.enemies:
            if item.rect.colliderect(self.thingRect) and self.thingRect != item:
                return item.direction
            else:
                return False
    def check_blockers(self):
        for item in self.blockers:
            if self.thingRect.colliderect(item):
                return item
            else:
                return False
            
    def check_proj(self):
        for item in self.enemies:
            if self.thingRect.colliderect(item):
                return item
            else:
                return False
    
    def check_in_border(self, width, height):
        inBorder = True
        if self.thingRect.x < 0 or self.thingRect.x + self.thingRect.width > width:
            inBorder = False
        elif self.thingRect.y < 0 or self.thingRect.y + self.thingRect.height > height:
            inBorder = False
             
        return inBorder
    
    def check_collisions(self, width, height):
        #Check player collision w/ enemies
        if self.collided() and isinstance(self.thing, player.Player):
            if self.collided() == 'u':
                self.thingRect.y += 20
            if self.collided() == 'd':
                self.thingRect.y -= 20
            if self.collided() == 'l':
                self.thingRect.x += 20
            if self.collided() == 'r':
                self.thingRect.x -= 20
            self.thing.ailment = 'stun'
            
        #Check if enemies collide with player
        if self.collided_on() and isinstance(self.thing, player.Player):
            if self.collided() == 'u':
                self.thingRect.y -= 20
            if self.collided() == 'd':
                self.thingRect.y += 20
            if self.collided() == 'l':
                self.thingRect.x -= 20
            if self.collided() == 'r':
                self.thingRect.x += 20
            self.thing.ailment = 'stun'
        
        #Check player collision w/ blockers
        if self.check_blockers():
            self.thingRect.x -= self.thing.x_vel
            self.thingRect.y -= self.thing.y_vel
            
        #Check player collision w/ borders
        if not self.check_in_border(width, height):
                self.thingRect.x -= self.thing.x_vel
                self.thingRect.y -= self.thing.y_vel