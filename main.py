import pygame
from pygame.locals import *
import tkinter as tk
import random
import sys
import os
import matplotlib.pyplot as plt
SCREEN_SIZE = (640, 480)
k_up=0
k_right=0
k_left=0
k_down=0
k_space=0
Xm=4
Ym=4
class Obj():
    def __init__(self,x,y,width,height,vx,vy,flag):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.flag=flag
        self.hp=10
    def update(self):
        self.x+=self.vx
        self.y+=self.vy

class Player(Obj):
    def __init__(self, x, y, width, height, vx, vy, flag):
        super().__init__(x, y, width, height, vx, vy, flag)
        self.action = 0
        self.outf=0
        pass
    def init(self,x,y,width,height,vx,vy,flag):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.flag=flag
        self.hp=10
    def control(self,action):
        self.action=action
        if action==1:
            self.vx=10
        elif action==2:
            self.vx=-10
        elif action==3:
            self.vy=10
        elif action==4:
            self.vy=-10
        elif action==5:
            pass

    def out(self):
        if self.x + self.width  > SCREEN_SIZE[0]:
            self.x=SCREEN_SIZE[0]-self.width
            self.outf=1
        if self.x<0:
            self.x=0
            self.outf=1
        if self.y+self.height>SCREEN_SIZE[1]:
            self.y=SCREEN_SIZE[1]-self.height
            self.outf=1
        if self.y<SCREEN_SIZE[1]/2:
            self.y=SCREEN_SIZE[1]/2
            self.outf=1
class Bot(Obj):
    def __init__(self, x, y, width, height, vx, vy, flag):
        super().__init__(x, y, width, height, vx, vy, flag)
        self.action=0
        self.outf = 0
    def init(self,x,y,width,height,vx,vy,flag):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy
        self.flag=flag
        self.hp=10
    def control(self,action):
        self.action = action
        if action==1:
            self.vx=10
        elif action==2:
            self.vx=-10
        elif action==3:
            self.vy=10
        elif action==4:
            self.vy=-10
        elif action==5:
            pass

    def out(self):
        if self.x + self.width / 2 > SCREEN_SIZE[0] or self.x < 0 + self.width / 2 < 0 or self.y + self.height / 2 > SCREEN_SIZE[1]/2 or self.y + self.height / 2 < 0:
            pass
        if self.x + self.width  > SCREEN_SIZE[0]:
            self.x=SCREEN_SIZE[0]-self.width
            self.outf=1
        if self.x<0:
            self.x=0
            self.outf=1
        if self.y+self.height>SCREEN_SIZE[1]/2:
            self.y=SCREEN_SIZE[1]/2-self.height
            self.outf=1
        if self.y<0:
            self.y=0
            self.outf=1
class bullet(Obj):
    def __init__(self, x, y, width, height, vx, vy, flag):
        super().__init__(x, y, width, height, vx, vy, flag)
        self.dead=0
        self.action=1
    def out(self):
        if self.x+self.width/2>SCREEN_SIZE[0] or self.x<0+self.width/2 <0 or self.y+self.height/2>SCREEN_SIZE[1] or self.y+self.height/2<0:
            return 1

class Game():
    def __init__(self):
        self.pBullet=[]
        self.bBullet=[]
        self.player=Player(SCREEN_SIZE[0] / 2 - 15, SCREEN_SIZE[1] / 3*2 - 15, 30, 30,0,0,1)
        self.bot=Bot(SCREEN_SIZE[0] / 2 - 15, SCREEN_SIZE[1] / 3 - 15, 30, 30,0,0,2)
        self.pHp=10
        self.bHp=10
        self.bBuoutf=0
        self.pBuoutf=0
        self.reflectf=0
        self.table = [[[[[[[[0 for i8 in range(Xm*Ym+1)] for i7 in range(2)] for i6 in range(Xm*Ym+1)] for i5 in range(2)] for i4 in
                    range(Xm*Ym)] for i3 in range(5)] for i2 in range(Xm*Ym)] for i1 in range(5)]
        count = 0
        for i1 in range(5):
            for i2 in range(Xm*Ym):
                for i3 in range(5):
                    for i4 in range(Xm*Ym):
                        for i5 in range(2):
                            for i6 in range(Xm*Ym+1):
                                for i7 in range(2):
                                    for i8 in range(Xm*Ym+1):
                                        count += 1
                                        self.table[i1][i2][i3][i4][i5][i6][i7][i8] = count# 状態を整数値に

    def draw(self,screen,font):
        for item in self.pBullet:
            pygame.draw.rect(screen, (100, 0, 0), Rect(item.x, item.y, item.width, item.height))
        for item in self.bBullet:
            pygame.draw.rect(screen, (0, 100, 0), Rect(item.x, item.y, item.width, item.height))
        pygame.draw.rect(screen, (255, 0, 0), Rect(self.player.x, self.player.y, self.player.width, self.player.height))
        pygame.draw.rect(screen, (0, 255, 0), Rect(self.bot.x, self.bot.y, self.bot.width, self.bot.height))
        text = font.render(f"Player HP:{self.player.hp}", True, (255, 100, 100))  # 描画する文字列の設定
        screen.blit(text, [20, 10])  # 文字列の表示位置
        text = font.render(f"Bot HP:{self.bot.hp}", True, (100, 255, 100))  # 描画する文字列の設定
        screen.blit(text, [SCREEN_SIZE[0]/10*8, 10])  # 文字列の表示位置
    def update(self):
        self.player.update()
        self.player.out()
        if self.player.action==5:
            if len(self.pBullet)<1:
                b = bullet(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 45, 45, 0, -5, 1)
                self.pBullet.append(b)
        self.bot.update()
        self.bot.out()
        if self.bot.action == 5:
            if len(self.bBullet) < 1:
                b = bullet(self.bot.x + self.bot.width / 2, self.bot.y + self.bot.height / 2, 45, 45, 0, 5,2)
                self.bBullet.append(b)

        for item in self.pBullet:
            item.update()
            dead=0
            if item.y<0:
                self.pBuoutf=1
                dead=1
            if abs(item.x + item.width /2 -self.bot.x-self.bot.width/2)<item.width/2+self.bot.width/2 and abs(item.y + item.height / 2 - self.bot.y -self.bot.height/2)<item.height/2+self.bot.height/2:
                dead=1
                self.bot.hp-=1
            if dead==1:
                self.pBullet.remove(item)

        for item in self.bBullet:
            item.update()
            dead=0
            if item.y+item.height>SCREEN_SIZE[1]:
                self.bBuoutf=1
                dead=1
            if abs(item.x + item.width / 2 - self.player.x - self.player.width / 2) < item.width/2+self.player.width/2 and abs(item.y + item.height / 2 - self.player.y - self.player.height / 2) < item.height/2+self.player.height/2:
                dead=1
                self.player.hp-=1
            if dead==1:
                self.bBullet.remove(item)
        """弾同士がぶつかって反射する
        for item in self.pBullet:
            for item2 in self.bBullet:
                if item.x + item.width / 2 > item2.x and item.x + item.width / 2 < item2.x + item2.width and item.y + item.height / 2 > item2.y and item.y + item.height / 2 < item2.y + item2.height:
                    item.vy,item2.vy=item2.vy,item.vy
                    self.reflectf=1
                    """
    def init(self):
        self.player.init(SCREEN_SIZE[0] / 2 - 15, SCREEN_SIZE[1] / 3*2 - 15, 30, 30,0,0,1)
        self.bot.init(SCREEN_SIZE[0] / 2 - 15, SCREEN_SIZE[1] / 3 - 15, 30, 30,0,0,2)
        self.pBullet.clear()
        self.bBullet.clear()
        self.pHp=10
        self.bHp=10
    def gameover(self):
        if self.player.hp<=0:
            return 1
        if self.bot.hp<=0:
            return 2
    def pos(self,x,y):
        if x<0:
            x=0
        if y<0:
            y=0
        if x>SCREEN_SIZE[0]:
            x=SCREEN_SIZE[0]-1
        if y>SCREEN_SIZE[1]:
            y=SCREEN_SIZE[1]-1
        for i in range(Ym):
            for j in range(Xm):
                if SCREEN_SIZE[0]/3*j<=x and SCREEN_SIZE[0]/3*(j+1)>=x and SCREEN_SIZE[1]/3*i<=y and SCREEN_SIZE[1]/3*(i+1)>=y:
                    return i*3+(j+1)
    def get_state(self,pa,pp,ba,bp,pba,pbp,bba,bbp):
        return self.table[pa-1][pp-1][ba-1][bp-1][pba][pbp-1][bba][bbp-1]

    def now_state(self):#############bulletactionは今後弾が直進以外の行動をする時を考慮して残しておく。
        if len(self.pBullet)==0:
            pba=0
            pbp=9
        else:
            pba=self.pBullet[0].action
            pbp=self.pos(self.pBullet[0].x,self.pBullet[0].y)
        if len(self.bBullet) == 0:
            bba = 0
            bbp = 9
        else:
            bba = self.bBullet[0].action
            bbp = self.pos(self.bBullet[0].x,self.bBullet[0].y)

#（プレイヤーの行動、プレイヤーの座標、ボットの〃、ボットの〃、プレイヤーの弾の行動、プレイヤーの弾の座標、ボットの〃、ボットの〃）
        return self.get_state(self.player.action,self.pos(self.player.x,self.player.y),self.bot.action,self.pos(self.bot.x,self.bot.y),
                              pba,pbp,bba,bbp)
    def get_review(self,px,py,bx,by,pbx,pby,bbx,bby):
        if len(self.bBullet)>0:
            if abs(px+self.player.width/2-bbx-self.bBullet[0].width/2)<self.player.width/2+self.bBullet[0].width/2 and abs(py+self.player.height/2-bby-self.bBullet[0].height/2)<self.player.height/2+self.bBullet[0].height/2:#プレイヤーがダメージを受けたとき
                return 1
        if len(self.pBullet) > 0:
            if abs(bx+self.bot.width/2-pbx-self.pBullet[0].width/2)<self.bot.width/2+self.pBullet[0].width/2 and abs(by+self.bot.height/2-pby-self.pBullet[0].height/2)<self.bot.height/2+self.pBullet[0].height/2:#ボットがダメージを受けたとき
                return 2
        if len(self.bBullet) > 0:
            if bby+self.bBullet[0].height>SCREEN_SIZE[1]:#ボットの弾がステージ外に出たとき
                return 5
        if pby<0:#プレイヤーの弾がステージ外に出たとき
            return 6
        return 0
    def review(self):
        if self.player.hp<self.pHp:#プレイヤーがダメージを受けたとき
            self.pHp=self.player.hp
            return 1
        elif self.bot.hp<self.bHp:#ボットがダメージを受けたとき
            self.bHp=self.bot.hp
            return 2
        elif self.bot.outf==1:#ボットが端にいるとき
            self.bot.outf=0
            return 3
        elif self.player.outf==1:#プレイヤーが端にいるとき
            self.player.outf=0
            return 4
        elif self.bBuoutf==1:#ボットの弾がステージ外に出たとき
            self.bBuoutf=0
            return 5
        elif self.pBuoutf==1:#プレイヤーの弾がステージ外に出たとき
            self.pBuoutf=0
            return 6
        elif self.reflectf==1:#弾同士がぶつかったとき
            self.reflectf=0
            return 7
        else:
            return 0
    def bot_control(self,flag,action):
        if flag==0:
            self.bot.control(random.randint(1, 5))
        if flag==1:
            self.bot.control(action)
    def player_control(self,flag,action):
        if flag==0:
            self.player.control(random.randint(1, 5))
        if flag==1:
            if k_up>=1:
                action=4
            if k_down>=1:
                action=3
            if k_right>=1:
                action=1
            if k_left>=1:
                action=2
            if k_space==1:
                action=5
            if k_up>=1 or k_down>=1 or k_right>=1 or k_left>=1 or k_space:
                self.player.control(action)
            self.player.vx/=1.05
            self.player.vy /= 1.05
        if flag==2:
            self.player.control(action)


class Learn():
    def __init__(self):
        self.game=Game()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        pygame.init()
        pygame.display.set_caption(u"シューティング")
        clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.q_table=[0.0]*(5*(Xm*Ym)*5*(Xm*Ym)*2*(Xm*Ym+1)*2*(Xm*Ym+1))
        self.player_qtable=[0.0]*(5*(Xm*Ym)*5*(Xm*Ym)*2*(Xm*Ym+1)*2*(Xm*Ym+1))
        self.winrate=0
        self.player_win=0
        self.bot_win=0
        self.count=0
        self.trainF=1
        self.y=[]
        self.sigma=100.0

        self.read=read()
        self.read.loop()
        self.trainCount=self.read.learncount
        self.playORai=self.read.playORai
        self.q_table=self.read.q_table
        self.player_qtable=self.read.player_qtable

        while True:
            if self.trainF==1:
                self.update()
                self.game_init()
                if self.count==self.trainCount:
                    self.trainF=0
            elif self.trainF==0:
                self.screen.fill((255, 255, 255))
                self.update()
                self.draw()
                self.game_init()
                pygame.display.update()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type==KEYDOWN:
                        global k_up,k_down,k_left,k_right,k_space
                        if event.key==K_UP:
                            k_up+=1
                        if event.key==K_DOWN:
                            k_down+=1
                        if event.key==K_RIGHT:
                            k_right+=1
                        if event.key==K_LEFT:
                            k_left+=1
                        if event.key==K_SPACE:
                            k_space+=1
                    if event.type==KEYUP:
                        if event.key==K_UP:
                            k_up=0
                        if event.key==K_DOWN:
                            k_down=0
                        if event.key==K_RIGHT:
                            k_right=0
                        if event.key==K_LEFT:
                            k_left=0
                        if event.key==K_SPACE:
                            k_space=0
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
    def update(self):
        self.player_control()
        self.bot_control()
        self.game.update()

    def get_reward(self,flag):
        reward=0
        if flag==0:
            reward=-1
        elif flag == 1:
            reward=777
        elif flag==2:
            reward=-333
        elif flag==3:
            reward=-1
        elif flag==4:
            pass
        elif flag==5:
            reward=-88
        elif flag==6:
            reward=1
        elif flag==7:
            reward=-1
        return reward
    def player_get_reward(self,flag):
        reward = 0
        if flag == 0:
            reward = -1
        elif flag == 1:
            reward = -77
        elif flag == 2:
            reward = 99
        elif flag == 3:
            pass
        elif flag == 4:
            reward = 0
        elif flag == 5:
            reward = 1
        elif flag == 6:
            reward = -39
        elif flag==7:
            reward=0
        return reward
    def bot_control(self):
        self.game.bot_control(1,self.get_action())
    def player_control(self):
        self.game.player_control(self.playORai, self.player_get_action())
    def player_get_action(self):
        if len(self.game.pBullet) != 0:
            pbx = self.game.pBullet[0].x
            pby = self.game.pBullet[0].y
            pbx_next = pbx + self.game.pBullet[0].vx
            pby_next = pby + self.game.pBullet[0].vy
        else:
            pbx=-99999 #どうせ値は使われないはずだから適当な値入れてみた
            pby=-99999
            pbx_next = 877#ばななにした意味はない
            pby_next = 877
        if len(self.game.bBullet) != 0:
            bbx = self.game.bBullet[0].x
            bby = self.game.bBullet[0].y
            bbx_next = bbx + self.game.bBullet[0].vx
            bby_next = bby + self.game.bBullet[0].vy
        else:
            bbx = -99999
            bby = -99999
            bbx_next = 877
            bby_next = 877
        now_max=self.get_next_max_AQ(self.game.player.x,self.game.player.y,self.game.bot.x,self.game.bot.y,pbx,pby,bbx,bby,0)
        next_pos=self.get_next_pos(self.game.player.x,self.game.player.y,now_max[0])

        next_max=self.get_next_max_AQ(next_pos[0],next_pos[1],self.game.bot.x+self.game.bot.vx,self.game.bot.y+self.game.bot.vy,pbx_next,pby_next,bbx_next,bby_next,0)

        if len(self.game.pBullet)==0:
            pba=0
            pbp=9
        else:
            pba=self.game.pBullet[0].action
            pbp=self.game.pos(self.game.pBullet[0].x,self.game.pBullet[0].y)
        if len(self.game.bBullet) == 0:
            bba = 0
            bbp = 9
        else:
            bba = self.game.bBullet[0].action
            bbp = self.game.pos(self.game.bBullet[0].x,self.game.bBullet[0].y)
        pa=now_max[0]
        pp=self.game.pos(self.game.player.x,self.game.player.y)
        ba=self.game.bot.action
        bp=self.game.pos(self.game.bot.x,self.game.bot.y)

        #######Q値更新
        eta = 0.2
        g = 0.8
        now_state = self.game.get_state(pa,pp,ba,bp,pba,pbp,bba,bbp)
        R=now_max[2]
        Q_next_max=next_max[1]

        self.player_qtable[now_state]=self.player_qtable[now_state]*(1-eta)+eta*(R+g*Q_next_max)
        action=now_max[0]
        return action
    def get_next_pos(self,x,y,action):
        if action==1:
            x+=10
        elif action==2:
            x-=10
        elif action==3:
            y += 10
        elif action==4:
            y -= 10
        elif action==5:
            pass
        return x,y
    def get_next_max_AQ(self,px,py,bx,by,pbx,pby,bbx,bby,flag):#flag　0:Player, 1:bot
        review = []
        R_next = []
        next_state = []
        Q_max = -9999999.0

        if len(self.game.pBullet) == 0:
            pba = 0
            pbp = Xm * Ym
        else:
            pba = self.game.pBullet[0].action
            pbp = self.game.pos(pbx+ self.game.pBullet[0].vx, pby + self.game.pBullet[0].vy)
        if len(self.game.bBullet) == 0:
            bba = 0
            bbp = Xm * Ym
        else:
            bba = self.game.bBullet[0].action
            bbp = self.game.pos(bbx+ self.game.bBullet[0].vx, bby + self.game.bBullet[0].vy)
        if flag==0:#プレイヤー基準
            next_state.append(self.game.get_state(1, self.game.pos(px + 10, py),
                                                  self.game.bot.action, self.game.pos(bx + self.game.bot.vx,
                                                                                      by + self.game.bot.vy),
                                                  pba, pbp, bba, bbp))
            review.append(self.player_qtable[next_state[0]])
            R_next.append(self.player_get_reward(self.game.get_review(px + 10, py,
                                                                      bx + self.game.bot.vx,
                                                                      by + self.game.bot.vy,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(2, self.game.pos(px - 10, py),
                                                  self.game.bot.action, self.game.pos(bx + self.game.bot.vx,
                                                                                      by + self.game.bot.vy),
                                                  pba, pbp, bba, bbp))
            review.append(self.player_qtable[next_state[1]])
            R_next.append(self.player_get_reward(self.game.get_review(px - 10, py,
                                                                      bx + self.game.bot.vx,
                                                                      by + self.game.bot.vy,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(3, self.game.pos(px, py + 10),
                                                  self.game.bot.action, self.game.pos(bx + self.game.bot.vx,
                                                                                      by + self.game.bot.vy),
                                                  pba, pbp, bba, bbp))
            review.append(self.player_qtable[next_state[2]])
            R_next.append(self.player_get_reward(self.game.get_review(px, py + 10,
                                                                      bx + self.game.bot.vx,
                                                                      by + self.game.bot.vy,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(4, self.game.pos(px, py - 10),
                                                  self.game.bot.action, self.game.pos(bx + self.game.bot.vx,
                                                                                      by + self.game.bot.vy),
                                                  pba, pbp, bba, bbp))
            review.append(self.player_qtable[next_state[3]])
            R_next.append(self.player_get_reward(self.game.get_review(px, py - 10,
                                                                      bx + self.game.bot.vx,
                                                                      by + self.game.bot.vy,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(5, self.game.pos(px, py),
                                                  self.game.bot.action, self.game.pos(bx + self.game.bot.vx,
                                                                                      by + self.game.bot.vy),
                                                  1, pbp if pba == 1 else self.game.pos(px,
                                                                                        py), bba, bbp))
            review.append(self.player_qtable[next_state[4]])
            R_next.append(self.player_get_reward(self.game.get_review(px, py,
                                                                      bx + self.game.bot.vx,
                                                                      by + self.game.bot.vy,
                                                                      pbx if pba == 1 else px - 7.5,
                                                                      pby if pba == 1 else py - 7.5, bbx,
                                                                      bby)))
        else:#bot用
            next_state.append(self.game.get_state(1, self.game.pos(px + self.game.player.vx, py+ self.game.player.vy),
                                                  self.game.bot.action, self.game.pos(bx + 10,
                                                                                      by ),
                                                  pba, pbp, bba, bbp))
            review.append(self.q_table[next_state[0]])
            R_next.append(self.get_reward(self.game.get_review(px +self.game.player.vx, py+self.game.player.vy,
                                                                      bx + 10,
                                                                      by ,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(2, self.game.pos(px +self.game.player.vx, py+self.game.player.vy),
                                                  self.game.bot.action, self.game.pos(bx -10,
                                                                                      by ),
                                                  pba, pbp, bba, bbp))
            review.append(self.q_table[next_state[1]])
            R_next.append(self.get_reward(self.game.get_review(px +self.game.player.vx, py+self.game.player.vy,
                                                                      bx -10,
                                                                      by ,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(3, self.game.pos(px +self.game.player.vx, py+self.game.player.vy),
                                                  self.game.bot.action, self.game.pos(bx ,
                                                                                      by + 10),
                                                  pba, pbp, bba, bbp))
            review.append(self.q_table[next_state[2]])
            R_next.append(self.get_reward(self.game.get_review(px +self.game.player.vx, py+self.game.player.vy,
                                                                      bx,
                                                                      by+10,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(4, self.game.pos(px +self.game.player.vx, py+self.game.player.vy),
                                                  self.game.bot.action, self.game.pos(bx ,
                                                                                      by -10),
                                                  pba, pbp, bba, bbp))
            review.append(self.q_table[next_state[3]])
            R_next.append(self.get_reward(self.game.get_review(px +self.game.player.vx, py+self.game.player.vy,
                                                                      bx,
                                                                      by-10,
                                                                      pbx, pby, bbx, bby)))
            next_state.append(self.game.get_state(5, self.game.pos(px +self.game.player.vx, py+self.game.player.vy),
                                                  self.game.bot.action, self.game.pos(bx,
                                                                                      by),
                                                  pba, pbp, 1, bbp if bba == 1 else self.game.pos(bx,
                                                                                        by)))
            review.append(self.q_table[next_state[4]])
            R_next.append(self.get_reward(self.game.get_review(px +self.game.player.vx, py+self.game.player.vy,
                                                                      bx ,
                                                                      by ,
                                                                      pbx ,
                                                                      pby , bbx if bba == 1 else bx - 7.5,
                                                                      bby if bba == 1 else by - 7.5)))

        action = 0
        R_max=0
        for i in range(4):
            if review[i] > Q_max:
                action = i + 1
                Q_max = review[i]
                R_max=R_next[i]

        if Q_max == 0 or random.uniform(0.0, 100.0) <=self.sigma:
            action = random.randint(1, 5)
            if self.sigma>0.1:
                self.sigma/=1.5
                print(f"{self.sigma}")

        return action,Q_max,R_max

    def get_action(self):
        if len(self.game.pBullet) != 0:
            pbx = self.game.pBullet[0].x
            pby = self.game.pBullet[0].y
            pbx_next = pbx + self.game.pBullet[0].vx
            pby_next = pby + self.game.pBullet[0].vy
        else:
            pbx = -99999  # どうせ値は使われないはずだから適当な値入れてみた
            pby = -99999
            pbx_next = 877  # ばななにした意味はない
            pby_next = 877
        if len(self.game.bBullet) != 0:
            bbx = self.game.bBullet[0].x
            bby = self.game.bBullet[0].y
            bbx_next = bbx + self.game.bBullet[0].vx
            bby_next = bby + self.game.bBullet[0].vy
        else:
            bbx = -99999
            bby = -99999
            bbx_next = 877
            bby_next = 877
        now_max = self.get_next_max_AQ(self.game.player.x, self.game.player.y, self.game.bot.x, self.game.bot.y, pbx,
                                       pby, bbx, bby,1)
        next_pos = self.get_next_pos(self.game.bot.x, self.game.bot.y, now_max[0])

        next_max = self.get_next_max_AQ(self.game.player.x+self.game.player.vx, self.game.player.y+self.game.player.vy, next_pos[0], next_pos[1], pbx_next, pby_next, bbx_next, bby_next,1)

        if len(self.game.pBullet) == 0:
            pba = 0
            pbp = 9
        else:
            pba = self.game.pBullet[0].action
            pbp = self.game.pos(self.game.pBullet[0].x, self.game.pBullet[0].y)
        if len(self.game.bBullet) == 0:
            bba = 0
            bbp = 9
        else:
            bba = self.game.bBullet[0].action
            bbp = self.game.pos(self.game.bBullet[0].x, self.game.bBullet[0].y)
        pa = self.game.bot.action
        pp = self.game.pos(self.game.player.x, self.game.player.y)
        ba = now_max[0]
        bp = self.game.pos(self.game.bot.x, self.game.bot.y)

        #######Q値更新
        eta = 0.2
        g = 0.8
        now_state = self.game.get_state(pa, pp, ba, bp, pba, pbp, bba, bbp)
        R = now_max[2]
        Q_next_max = next_max[1]

        self.q_table[now_state] = self.q_table[now_state] * (1 - eta) + eta * (R + g * Q_next_max)
        action = now_max[0]
        return action
    def draw(self):
        self.game.draw(self.screen,self.font)
    def game_init(self):
        if self.game.gameover() == 1 or self.game.gameover() == 2:
            if self.game.gameover() == 1:
                self.bot_win += 1
            if self.game.gameover() == 2:
                self.player_win += 1
            self.count+=1
            self.winrate = self.bot_win / self.count*100
            print(f"勝率:{self.winrate}%,回数:{self.count}")
            if self.count%100==0 and self.count>=100:
                with open(f"{self.count}.txt","w") as f:
                    strlist=[]
                    for n in self.q_table:
                        strlist.append(str(n)+"\n")
                    f.writelines(strlist)
                if self.playORai==2:
                    with open("P_"+f"{self.count}.txt","w") as f:
                        strlist=[]
                        for n in self.player_qtable:
                            strlist.append(str(n)+"\n")
                        f.writelines(strlist)
            self.y.append(self.winrate)
            if self.count == self.trainCount:
                plt.plot(self.y)
                plt.show()
            self.game.init()


class read():
    def __init__(self):
        self.q_table=[0.0]*(5*(Xm*Ym)*5*(Xm*Ym)*2*(Xm*Ym+1)*2*(Xm*Ym+1))
        self.player_qtable=[0.0]*(5*(Xm*Ym)*5*(Xm*Ym)*2*(Xm*Ym+1)*2*(Xm*Ym+1))
        self.win = tk.Tk()
        self.win.title("読み込む学習回数")
        self.label = tk.Label(text="読み込むデータの学習回数(.txtは不要)を指定してください。")
        self.box = tk.Entry()
        self.box.focus_set()
        self.label2=tk.Label(text="行う学習回数を指定してください。自分で操作する場合は0を入力してください。")
        self.box2=tk.Entry()
        self.label3 = tk.Label(text="乱数:0, 操作可能:1, 学習済みは学習回数(>=100):")
        self.box3 = tk.Entry()
        self.learncount=0
        self.playORai=0
    def loop(self):
        self.label.pack()
        self.box.pack()
        self.label2.pack()
        self.box2.pack()
        self.label3.pack()
        self.box3.pack()
        self.win.bind("<Return>", self.decide)
        self.win.mainloop()
    def decide(self,event):
        if os.path.exists(f"{self.box.get()}.txt") == True:
            with open(f"{self.box.get()}.txt", "r") as f:
                strlist = f.readlines()
                self.q_table = [float(s) for s in strlist]
        self.learncount = int(self.box2.get())
        if int(self.box3.get())>=100:
            self.playORai = 2
            if os.path.exists("P_"+f"{self.box.get()}.txt") == True:
                with open("P_"+f"{self.box.get()}.txt", "r") as f:
                    strlist = f.readlines()
                    self.player_qtable = [float(s) for s in strlist]
        else:
            self.playORai=int(self.box3.get())
        self.win.destroy()



if __name__ == '__main__':
    Learn()
