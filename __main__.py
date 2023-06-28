import sys
import random
import math
import pygame
import pygame.locals

import conf
import platform
import ball


def main():
    pygame.init()

    # load window surface
    screen  = pygame.display.set_mode((conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT))
    main_clock = pygame.time.Clock()

    platforms = [platform.Platform(conf.PLATFORMSEDGE, conf.WINDOW_HEIGHT/2, *conf.PLATFORMSSIZE, (0,0,0)), platform.Platform(conf.WINDOW_WIDTH-conf.PLATFORMSEDGE, conf.WINDOW_HEIGHT/2, *conf.PLATFORMSSIZE, (0,0,0))]
    gameball = ball.Ball(conf.WINDOW_WIDTH/2,conf.WINDOW_HEIGHT/2,conf.BALLRADIUS, (0,0,0))
    
    playerindex = random.randint(0,1)
    balldeg = random.randint(*conf.BALLINITDEGRANGE) + random.randint(0,3)*90
    
    font = pygame.font.SysFont(None, 60)
    
    stop = False

    while True:
        # 偵測事件
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        # 背景顏色，清除畫面
        screen .fill(conf.BACKCOLOR)

        # 渲染物件
        if gameball.rect.x < 0 or gameball.rect.x+gameball.rect.w > conf.WINDOW_WIDTH:
            stop = True
            gameover = font.render('Game over!', True, (0, 0, 0))
            screen.blit(gameover, (conf.WINDOW_WIDTH/2 - gameover.get_width()/2,conf.WINDOW_HEIGHT/2 - gameover.get_height()/2))
            
        if not stop:
            #platforms[playerindex].rect.centery = pygame.mouse.get_pos()[1]
            if pygame.sprite.collide_rect(gameball, platforms[0]) or pygame.sprite.collide_rect(gameball, platforms[1]):
                balldeg = 180 - balldeg
                balldeg += random.randint(-conf.BALLHITDEGRAN,conf.BALLHITDEGRAN)
            if gameball.rect.y < 0 or gameball.rect.y+gameball.rect.h > conf.WINDOW_HEIGHT:
                balldeg = 0 - balldeg
                balldeg += random.randint(-conf.BALLHITDEGRAN,conf.BALLHITDEGRAN)
            gameball.rect.center = (gameball.rect.centerx + conf.BALLSPEED * math.cos(float(balldeg)/180*math.pi), gameball.rect.centery + conf.BALLSPEED * math.sin(float(balldeg)/180*math.pi))
            for a in platforms:
                a.rect.centery = pygame.mouse.get_pos()[1]
            
        for a in platforms:
            a.draw(screen)
        gameball.draw(screen)

        pygame.display.update()
        # 控制遊戲迴圈迭代速率
        main_clock.tick(conf.FPS)

if __name__ == '__main__':    
    main()