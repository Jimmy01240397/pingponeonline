import sys
import random
import math
import socket
import json
import threading
import time
import pygame
import pygame.locals

import conf
import platform
import ball


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", conf.PORT))
data = {}
lock = threading.Lock()

kill = False

def recving():
    global data
    while(not kill):
        indata, host = sock.recvfrom(conf.BUFFERSIZE)
        lock.acquire()
        data = json.loads(indata.decode())
        lock.release()

def main():
    global kill
    host = input("set your server host and port to connect game or set empty to be a server: ")
    
    if host == "":
        print(f"listen port {conf.PORT}")
        print("wait for connect")
        indata = b""
        while(indata != b"connect"):
            indata, host = sock.recvfrom(conf.BUFFERSIZE)
        sock.sendto(b"connect", host)
        print("wait for ack")
        indata = b""
        while(indata != b"ack"):
            indata, host = sock.recvfrom(conf.BUFFERSIZE)
        playerindex = 0
    else:
        host = (host.rsplit(':', 1)[0], int(host.rsplit(':', 1)[1]))
        sock.sendto(b"connect", host)
        print("wait for connect")
        indata = b""
        while(indata != b"connect"):
            indata, host = sock.recvfrom(conf.BUFFERSIZE)
        sock.sendto(b"ack", host)
        playerindex = 1
            
    kill = False
    
    t = threading.Thread(target = recving)
    t.daemon = True
    t.start()
    
    pygame.init()

    # load window surface
    screen  = pygame.display.set_mode((conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT))
    main_clock = pygame.time.Clock()

    platforms = [platform.Platform(conf.PLATFORMSEDGE, conf.WINDOW_HEIGHT/2, *conf.PLATFORMSSIZE, (0,0,0)), platform.Platform(conf.WINDOW_WIDTH-conf.PLATFORMSEDGE, conf.WINDOW_HEIGHT/2, *conf.PLATFORMSSIZE, (0,0,0))]
    gameball = ball.Ball(conf.WINDOW_WIDTH/2,conf.WINDOW_HEIGHT/2,conf.BALLRADIUS, (0,0,0))
    
    if playerindex == 0:
        balldeg = random.randint(*conf.BALLINITDEGRANGE) + random.randint(0,3)*90
    else:
        balldeg = 0
    
    font = pygame.font.SysFont(None, 60)
    
    stop = False
    
    if playerindex == 0:
        starttime = time.time()
    else:
        starttime = None
    
    while True:
        lock.acquire()
        nowdata = data
        lock.release()
        # 偵測事件
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                kill = True
                pygame.quit()
                sys.exit()

        # 背景顏色，清除畫面
        screen .fill(conf.BACKCOLOR)

        # 渲染物件
        if playerindex == 1 and 'counting' in data:
            counting = data['counting']
        elif playerindex == 1:
            counting = conf.STARTCOUNT
        else:
            counting = conf.STARTCOUNT - (time.time() - starttime)
        if counting >= 0:
            counttime = font.render(str(int(counting)), True, (0, 0, 0))
            screen.blit(counttime, (conf.WINDOW_WIDTH/2 - counttime.get_width()/2,conf.WINDOW_HEIGHT/2 - counttime.get_height()*2))
        else:
            if playerindex == 1 and (gameball.rect.x < 0 or gameball.rect.x+gameball.rect.w > conf.WINDOW_WIDTH):
                stop = True
            elif playerindex == 0 and 'stop' in data:
                stop = data['stop']
                
            if stop:
                gameover = font.render('Game over!', True, (0, 0, 0))
                screen.blit(gameover, (conf.WINDOW_WIDTH/2 - gameover.get_width()/2,conf.WINDOW_HEIGHT/2 - gameover.get_height()/2))
            else:
                if playerindex == 0:
                    if pygame.sprite.collide_rect(gameball, platforms[0]) or pygame.sprite.collide_rect(gameball, platforms[1]):
                        balldeg = 180 - balldeg
                        balldeg += random.randint(-conf.BALLHITDEGRAN,conf.BALLHITDEGRAN)
                    if gameball.rect.y < 0 or gameball.rect.y+gameball.rect.h > conf.WINDOW_HEIGHT:
                        balldeg = 0 - balldeg
                        balldeg += random.randint(-conf.BALLHITDEGRAN,conf.BALLHITDEGRAN)
                    gameball.rect.center = (gameball.rect.centerx + conf.BALLSPEED * math.cos(float(balldeg)/180*math.pi), gameball.rect.centery + conf.BALLSPEED * math.sin(float(balldeg)/180*math.pi))
                elif 'ball' in data:
                    balldeg = data["ball"]["balldeg"]
                    gameball.rect.center = (data["ball"]["x"], data["ball"]["y"])
                    
                platforms[playerindex].rect.centery = pygame.mouse.get_pos()[1]
                if 'platform' in data:
                    platforms[int(not bool(playerindex))].rect.centery = data["platform"]["y"]
                #for a in platforms:
                #    a.rect.centery = pygame.mouse.get_pos()[1]
            
        # send data
        sock.sendto(json.dumps({"counting":counting,"stop": stop, "ball":{"balldeg": balldeg, "x": gameball.rect.centerx, "y": gameball.rect.centery}, "platform": {"y": platforms[playerindex].rect.centery}}).encode(), host)
        
        for a in platforms:
            a.draw(screen)
        gameball.draw(screen)

        pygame.display.update()
        # 控制遊戲迴圈迭代速率
        main_clock.tick(conf.FPS)

if __name__ == '__main__':    
    main()