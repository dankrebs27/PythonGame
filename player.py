import pygame
import collision  # @UnresolvedImport @UnusedImport
from collision import CollisionHandler  # @UnusedImport
import enemies  # @UnresolvedImport @UnusedImport
import sheetreader  # @UnresolvedImport
import weapon  # @UnresolvedImport @UnusedImport

#stand still
mainRects = [pygame.Rect(128, 0, 32, 32),
             pygame.Rect(128, 32, 32, 32),
             pygame.Rect(128, 64, 32, 32),
             pygame.Rect(128, 96, 32, 32)]

#walking images 1
mainWRects = [pygame.Rect(160, 0, 32, 32),
              pygame.Rect(160, 32, 32, 32),
              pygame.Rect(160, 64, 32, 32),
              pygame.Rect(160, 96, 32, 32)]

#walking images 2
mainW2Rects = [pygame.Rect(96, 0, 32, 32),
               pygame.Rect(96, 32, 32, 32),
               pygame.Rect(96, 64, 32, 32),
               pygame.Rect(96, 96, 32, 32)]

ss = sheetreader.Spritesheet('sheet.png')
standstill = ss.images_at(mainRects, colorkey=(0, 0, 0))
walk1 = ss.images_at(mainWRects, colorkey=(0, 0, 0))
walk2 = ss.images_at(mainW2Rects, colorkey=(0, 0, 0))

gun = weapon.Weapon()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 3
        self.direction = 'd'
        self.state = 's'
        self.images = []
        self.rect = pygame.Rect(150, 150, 32, 32)
        self.rect.x = x
        self.rect.y = y
        self.count = 0
        self.ailment = 'nothing'
        self.count2 = 0
        self.weapon = gun
        self.image = pygame.Surface
        
    def draw_self(self, display):
        self.determine_images()
        directions = {'d': 0, 'l': 1, 'r': 2, 'u': 3}
        
        for key in directions:
            if self.direction == key:
                self.image = self.images[directions[key]]
#         display.blit(self.image, (self.rect.x,self.rect.y))

        gun.direction = self.direction
        gun.draw_self(self.rect.x, self.rect.y, display)
        
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
     
    def check_move(self, blockers, enemies, display):
        keyActions = [[pygame.K_LEFT, -1, 'x', 'l'],
                          [pygame.K_RIGHT, 1, 'x', 'r'],
                          [pygame.K_UP, -1, 'y', 'u'],
                          [pygame.K_DOWN, 1, 'y', 'd']]
        if self.ailment == 'stun':
            self.state = 's'
            self.count2 += 1
            if self.count2 == 29:
                self.ailment = 'nothing'
                self.count2 = 0
            return
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    
                if event.type == pygame.KEYDOWN: 
                    for item in keyActions:
                        if event.key == item[0] and item[2] == 'x':
                            self.x_vel = item[1] * self.speed
                            self.direction = item[3]
                            self.state = 'w'
                        elif event.key == item[0] and item[2] == 'y':
                            self.y_vel = item[1] * self.speed
                            self.direction = item[3]
                            self.state = 'w'
                    if event.key == pygame.K_SPACE:
                        gun.fire(display, blockers, enemies)
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.x_vel += self.speed
                    if event.key == pygame.K_RIGHT:
                        self.x_vel -= self.speed
                    if event.key == pygame.K_DOWN:
                        self.y_vel -= self.speed
                    if event.key == pygame.K_UP:
                        self.y_vel += self.speed
                        
            if self.x_vel == 0 and self.y_vel == 0:
                self.state = 's'
    
            self.rect.x += self.x_vel
            self.rect.y += self.y_vel
                
    def update_player(self, display, blockers, enemies):
        self.check_move(blockers, enemies, display)
        self.draw_self(display)
