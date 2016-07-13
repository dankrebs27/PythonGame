import pygame
from pytmx import *  # @UnusedWildImport
import sheetreader  # @UnresolvedImport
import weapon  # @UnresolvedImport
import random  # @UnusedImport
import player  # @UnresolvedImport @UnusedImport
import collision  # @UnresolvedImport @UnusedImport

#stand still
standRects = [pygame.Rect(128, 128, 32, 32),
             pygame.Rect(128, 160, 32, 32),
             pygame.Rect(128, 192, 32, 32),
             pygame.Rect(128, 224, 32, 32)]

#walking images 1
walk1Rects = [pygame.Rect(160, 128, 32, 32),
              pygame.Rect(160, 160, 32, 32),
              pygame.Rect(160, 192, 32, 32),
              pygame.Rect(160, 224, 32, 32)]

#walking images 2
walk2Rects = [pygame.Rect(96, 128, 32, 32),
               pygame.Rect(96, 160, 32, 32),
               pygame.Rect(96, 192, 32, 32),
               pygame.Rect(96, 224, 32, 32)]

ss = sheetreader.Spritesheet('sheet.png')
standstill = ss.images_at(standRects, colorkey=(0, 0, 0))
walk1 = ss.images_at(walk1Rects, colorkey=(0, 0, 0))
walk2 = ss.images_at(walk2Rects, colorkey=(0, 0, 0))

gun = weapon.Weapon()


def create_enemies(maprender):
        enemies = []
        for bads in maprender.tmx_data.objects:      #This gets a dict of properties. maybe instead could create all the objects right here
            properties = bads.__dict__
            if properties['type'] == 'enemy':
                name = properties['name']
                x = properties['x'] 
                y = properties['y']
                width = properties['width']
                height = properties['height']
                #filename = properties['filename']
                newEnemy = Enemy(x, y, name, width, height)
                enemies.append(newEnemy)
        
        return enemies

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, name, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.dCount = 0
        self.direction = 'd'
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 2
        self.state = 's'
        self.images = standstill
        self.count = 0
        self.image = pygame.Surface
        self.weapon = gun

    def draw_self(self, display):
        self.determine_images()
        directions = {'d': 0, 'l': 1, 'r': 2, 'u': 3}
        
        for key in directions:
            if self.direction == key:
                self.image = self.images[directions[key]]
        #display.blit(playerSurf, (self.rect.x,self.rect.y))

        self.weapon.direction = self.direction
        self.weapon.draw_self(self.rect.x, self.rect.y, display)
        
    def determine_images(self):
        if self.state == 's':
            self.images = standstill
        elif self.state == 'w':
            if self.count == self.speed * 4:  #If 4 x char's speed frames have passed, switch to walk2 set of images
                if self.images == walk1:
                    self.images = walk2
                else:
                    self.images = walk1
                self.count = 0
            self.count += 1
            
            
    def change_direction(self):
        if self.dCount == 60 or self.state == 's':
            dNum = random.randint(1,4)
            dDict = {1: 'l', 2: 'r', 3: 'u', 4:'d'}
            
            for key in dDict:
                if dNum == key:
                    self.direction = dDict[key]
                    self.dCount = 0
        else:
            self.dCount += 1

    def check_move(self, blockers, enemies):
        self.x_vel = 0
        self.y_vel = 0
        directions = [['l', -1, 'x'],
                      ['r', 1, 'x'],
                      ['u', -1, 'y'],
                      ['d', 1, 'y']]
        
        for item in directions:
            if item[0] == self.direction and item[2] == 'x':
                self.x_vel += self.speed * item[1]
            if item[0] == self.direction and item[2] == 'y':
                self.y_vel += self.speed * item[1]
        
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.state = 'w'
        
    def update_enemies(self, display, blockers, enemies):
        self.change_direction()
        self.check_move(blockers, enemies)
        self.draw_self(display)