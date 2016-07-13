import pygame
import sheetreader  # @UnresolvedImport @UnusedImport
import projectile  # @UnresolvedImport @UnusedImport

gunRects = [pygame.Rect(0, 0, 20, 20),
             pygame.Rect(20, 0, 20, 20),
             pygame.Rect(40, 0, 20, 20),
             pygame.Rect(60, 0, 20, 20)]

ss = sheetreader.Spritesheet('weaponsheet.png')
guns = ss.images_at(gunRects, colorkey=(0, 0, 0))

class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = guns
        self.direction = 'd'
        self.fireRate = 0
        self.rect = pygame.Rect(1, 12, 20, 20)
        self.fireSurf = pygame.image.load('fire.png')
        self.fireSurf.set_colorkey((255,255,255))
        self.leftFire = pygame.transform.flip(self.fireSurf, True, False)
        self.upFire = pygame.transform.rotate(self.fireSurf, 90)
        self.downFire = pygame.transform.rotate(self.fireSurf, -90)
        self.fireRect = self.fireSurf.get_rect()
        self.image = pygame.Surface
        
    def draw_self(self, x, y, surface):
        #list that holds x&y vals associated with each gun directions
        directions = [['u', 0, 15, 5],
                      ['d', 1, 0, 15],
                      ['r', 2, 20, 10],
                      ['l', 3, 5, 5]]
        
        #finds which direction player is facing, and draws that gun image with correct x and y vals
        for item in directions:
            if self.direction == item[0]:
                self.rect.x = x + item[2]
                self.rect.y = y + item[3]
                #surface.blit(self.images[item[1]], self.rect)
                self.image = self.images[item[1]]
                
    def fire(self, surface, blockers, enemies):
        directions = [['u', self.rect.x, 2, self.rect.y, -(self.rect.height), self.upFire], # x, width, y, height, surface
                      ['d', self.rect.x, 0, self.rect.y, self.rect.height, self.downFire],
                      ['r', self.rect.x, self.rect.width, self.rect.y, 3, self.fireSurf],
                      ['l', self.rect.x, -(self.rect.width), self.rect.y, 3, self.leftFire]]
        
        for item in directions:
            if self.direction == item[0]:
                tempRect = item[5].get_rect()
                tempRect.x = item[1] + item[2]
                tempRect.y = item[3] + item[4]
                surface.blit(item[5], tempRect)
        
        bullet = projectile.Projectile('bullet.png', self.rect.x, self.rect.y, self.direction)
        #bullet.firing(surface, blockers, enemies)