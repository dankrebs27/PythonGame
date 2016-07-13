import pygame  # @UnusedImport
import collision  # @UnresolvedImport @UnusedImport


#list of all projectiles on map
projectiles = []

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = direction
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.set_direction()
        self.image = self.surf
        self.onMap = True
        projectiles.append(self)
    
    def firing(self, blockers, enemies, width, height):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        #display.blit(self.surf, self.rect)
        
        checker = collision.CollisionHandler(self, enemies, blockers)
        hitEnemy = checker.check_proj()
        hitBlocker = checker.check_blockers()
        
        if hitEnemy:
            self.kill()
        elif hitBlocker:
            self.kill()
        elif not checker.check_in_border(width, height):
            self.kill()
            
        return hitEnemy
        
    def set_direction(self):
        directions = [['u', 0, -10, pygame.transform.rotate, 90],
                      ['d', 0, 10, pygame.transform.rotate, -90],
                      ['l', -10, 0, pygame.transform.flip],
                      ['r', 10, 0]]
        
        for item in directions:
            if item[0] == self.direction and item[2] == 0:
                self.x_vel = item[1]
                self.y_vel = item[2]
                self.rect.x += item[1]
                if item[0] == 'l':
                    self.surf = item[3](self.surf, True, False)
                    self.rect.x += item[1]
            if item[0] == self.direction and item[1] == 0:
                self.x_vel = item[1]
                self.y_vel = item[2]
                self.rect.y += item[2]
                self.surf = item[3](self.surf, item[4])