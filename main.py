import pygame  # @UnusedImport
import time
from pytmx import *  #@UnusedWildImport
import player #@UnresolvedImport
from renderer import *  #@UnresolvedImport @UnusedWildImport
import enemies  # @UnresolvedImport
import projectile  # @UnresolvedImport @UnusedImport
import collision  # @UnresolvedImport
import newrender  # @UnresolvedImport
import weapon  # @UnresolvedImport @UnusedImport
import level  # @UnresolvedImport @UnusedImport

pygame.init() #@UndefinedVariable

display_width = 640
display_height = 640
 
black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)
slate_gray = (119,136,153)
red = (200,0,0)
bright_red = (255, 0, 0)
green = (0,200,0)
bright_green = (0, 255, 0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A New Adventure')
clock = pygame.time.Clock()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
            
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("OpenSans-Semibold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def type_text(text, xpos, ypos):
    typeText = pygame.font.Font("OpenSans-Semibold.ttf",15)
    newstring = ""

    for char in text:
        newstring += char
        charSurf, charRect = text_objects(newstring, typeText, white)
        charRect.left = xpos
        charRect.top = ypos
        gameDisplay.blit(charSurf, charRect)
        
        pygame.display.update()
        time.sleep(0.1)
        
        charSurf.fill(black)
        gameDisplay.blit(charSurf, charRect)

def pause_menu():
    print("IN PAUSE MENU")
    copiedSurf = gameDisplay.copy()
    copiedRect = copiedSurf.get_rect()
    darkSurface = pygame.Surface((display_width,display_height))
    darkSurface.fill(black)
    darkSurface.set_alpha(100)
    darkRect = darkSurface.get_rect()
    pauseSurface = pygame.Surface((220,235))
    pauseRect = pauseSurface.get_rect()
    pauseRect.left = 140
    pauseRect.top = 290
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    
        gameDisplay.blit(copiedSurf, copiedRect)
        gameDisplay.blit(darkSurface, darkRect)
        gameDisplay.blit(pauseSurface, pauseRect)
        button("Settings",150,300,200,50,gray,slate_gray, game_intro)
        button("Save",150,355,200,50,gray,slate_gray, game_intro)
        button("Load",150,410,200,50,gray,slate_gray, game_intro)
        button("Quit",150,465,200,50,gray,slate_gray, game_intro)
        
        pygame.display.update()
    
def test_map():
    playChar = player.Player(150, 150)
    maprender = newrender.NewRender("tileset/tryout.tmx")
    mapWidth, mapHeight = maprender.get_dims()
    #layersList = maprender.tmx_data.layers
    badguys = enemies.create_enemies(maprender)
    running = True
    
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
    
    
    level1 = level.Level(maprender)
    while running:
        #Render map and give list of blocker objects
        
        #create enemies list from map
        for i in badguys:
            i.update_enemies(gameDisplay, blockers, badguys)
        playChar.update_player(gameDisplay, blockers, badguys)
        
        bullets = projectile.projectiles
        for i in bullets:
            maprender.group.add(i)
            hitEnemy = i.firing(blockers, badguys, mapWidth, mapHeight)
            if hitEnemy in badguys:
                badguys.remove(hitEnemy)
                hitEnemy.kill()
                i.kill()
        
        maprender.group.add(playChar)
        maprender.group.add(playChar.weapon)
        for i in badguys:
            maprender.group.add(i)
            maprender.group.add(i.weapon)
        
        checker = collision.CollisionHandler(playChar, badguys, blockers)
        checker.check_collisions(mapWidth, mapHeight)
        for i in badguys:
            eChecker = collision.CollisionHandler(i, badguys, blockers)
            eChecker.check_collisions(mapWidth, mapHeight)
        #render top layer of map last
        #maprender.render_tile_layer(gameDisplay, layersList[2])
        maprender.draw_map(gameDisplay, playChar)
        pygame.display.update()
        clock.tick(60)


def start_menu():
    startrun = True
    while startrun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('OpenSans-Semibold.ttf', 70)
        TextSurf, TextRect = text_objects("A New Adventure", largeText, black)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("New Game",150,450,100,50,green,bright_green, game_intro)
        button("Load Game",550,450,100,50,red,bright_red, pygame.quit)

        pygame.display.update()
        clock.tick(15)

def game_intro():
    msg1 = "You slowly begin to awaken"
    msg2 = "You cannot recall the last thing that happened to you..."
                
    gameDisplay.fill(black)
    pygame.display.update()
    type_text(msg1, 150, 300)
    type_text(msg2, 150, 325)
    time.sleep(2.5)
    
    gameDisplay.fill(black)

    test_map()
    
    pygame.quit()
    quit()

    pygame.display.update()
    clock.tick(60)


test_map()
#start_menu()
