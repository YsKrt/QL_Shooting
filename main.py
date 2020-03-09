import pygame
from pygame.locals import *
import  numpy as np
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
        self.table = [[[[[[[[0 for i8 in range(10)] for i7 in range(2)] for i6 in range(10)] for i5 in range(2)] for i4 in
                    range(9)] for i3 in range(5)] for i2 in range(9)] for i1 in range(5)]
        count = 0
        for i1 in range(5):
            for i2 in range(9):
                for i3 in range(5):
                    for i4 in range(9):
                        for i5 in range(2):
                            for i6 in range(10):
                                for i7 in range(2):
                                    for i8 in range(10):
                                        count += 1
                                        self.table[i1][i2][i3][i4][i5][i6][i7][i8] = count#max 810000 状態を整数値に

    def draw(self,screen,font):
        for item in self.pBullet:
            pygame.draw.rect(screen, (0, 0, 0), Rect(item.x, item.y, item.width, item.height))
        for item in self.bBullet:
            pygame.draw.rect(screen, (0, 0, 0), Rect(item.x, item.y, item.width, item.height))
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
                b = bullet(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 15, 15, 0, -15, 1)
                self.pBullet.append(b)
        self.bot.update()
        self.bot.out()
        if self.bot.action == 5:
            if len(self.bBullet) < 1:
                b = bullet(self.bot.x + self.bot.width / 2, self.bot.y + self.bot.height / 2, 15, 15, 0, 15,2)
                self.bBullet.append(b)

        for item in self.pBullet:
            item.update()
            dead=0
            if item.out()==1:
                dead=1
            if item.x + item.width / 2 > self.bot.x and item.x + item.width / 2 < self.bot.x + self.bot.width and item.y + item.height / 2 > self.bot.y and item.y + item.height / 2 < self.bot.y + self.bot.height:
                dead=1
                self.bot.hp-=1
            if dead==1:
                self.pBullet.remove(item)

        for item in self.bBullet:
            item.update()
            dead=0
            if item.out()==1:
                dead=1
            if item.x + item.width / 2 > self.player.x and item.x + item.width / 2 < self.player.x + self.player.width and item.y + item.height / 2 > self.player.y and item.y + item.height / 2 < self.player.y + self.player.height:
                dead=1
                self.player.hp-=1
            if dead==1:
                self.bBullet.remove(item)

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
        for i in range(3):
            for j in range(3):
                if SCREEN_SIZE[0]/3*j<=x and SCREEN_SIZE[0]/3*(j+1)>=x and SCREEN_SIZE[1]/3*i<=y and SCREEN_SIZE[1]/3*(i+1)>=y:
                    return i+j+1
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
    def review(self):
        if self.player.hp<self.pHp:
            self.pHp=self.player.hp
            return 1
        elif self.bot.hp<self.bHp:
            self.bHp=self.bot.hp
            return 2
        elif self.bot.outf==1:
            self.bot.outf=0
            return 3
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

            self.player.vx/=1.05
            self.player.vy /= 1.05
            self.player.control(action)

class Learn():
    def __init__(self):
        self.table = [[[[[[[[0 for i8 in range(10)] for i7 in range(2)] for i6 in range(10)] for i5 in range(2)] for i4 in
                    range(11)] for i3 in range(6)] for i2 in range(10)] for i1 in range(6)]
        self.game=Game()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        pygame.init()
        pygame.display.set_caption(u"シューティング")
        clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.q_table=[0]*810001
        self.winrate=0
        self.player_win=0
        self.bot_win=0
        self.count=0
        self.trainF=1

        self.y=[]

        self.read=read()
        self.read.loop()
        self.trainCount=self.read.learncount
        self.playORai=self.read.playORai
        self.q_table=self.read.q_table
        print(f"{self.q_table}")
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
        self.game.player_control(self.playORai, 0)
        #self.game.bot_control(0, 0)
        self.reflect()
        self.game.update()
        self.update_qtable()
    def update_qtable(self):
        review=self.game.review()
        state=self.game.now_state()
        if review!=0:
            self.q_table[state] += self.get_reward(review)
    def get_reward(self,flag):
        reward=0
        if flag == 1:
            reward=273
        elif flag==2:
            reward=-349
        elif flag==3:
            reward=-7
        return reward
    def reflect(self):
        self.game.bot_control(1,self.get_action())
    def get_action(self):
        review=[]
        maxreview=0
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!次の行動をしたときの評価値を得る。プレイヤーはめんどいから動かさない
        if len(self.game.pBullet)==0:
            pba=0
            pbp=9
        else:
            pba=self.game.pBullet[0].action
            pbp=self.game.pos(self.game.pBullet[0].x,self.game.pBullet[0].y-50)
        if len(self.game.bBullet) == 0:
            bba = 0
            bbp = 9
        else:
            bba = self.game.bBullet[0].action
            bbp = self.game.pos(self.game.bBullet[0].x,self.game.bBullet[0].y+self.game.bBullet[0].vy)
        next_state = self.game.get_state(self.game.player.action, self.game.pos(self.game.player.x, self.game.player.y),
                                         1, self.game.pos(self.game.bot.x + 10,self.game.bot.y),
                                         pba, pbp, bba, bbp)
        review.append(self.q_table[next_state])
        next_state = self.game.get_state(self.game.player.action, self.game.pos(self.game.player.x, self.game.player.y),
                                         2, self.game.pos(self.game.bot.x - 10, self.game.bot.y),
                                         pba, pbp, bba, bbp)
        review.append(self.q_table[next_state])
        next_state = self.game.get_state(self.game.player.action, self.game.pos(self.game.player.x, self.game.player.y),
                                         3, self.game.pos(self.game.bot.x, self.game.bot.y+10),
                                         pba, pbp, bba, bbp)
        review.append(self.q_table[next_state])
        next_state = self.game.get_state(self.game.player.action, self.game.pos(self.game.player.x, self.game.player.y),
                                         4, self.game.pos(self.game.bot.x , self.game.bot.y-10),
                                         pba, pbp, bba, bbp)
        review.append(self.q_table[next_state])
        next_state = self.game.get_state(self.game.player.action, self.game.pos(self.game.player.x, self.game.player.y),
                                         5, self.game.pos(self.game.bot.x, self.game.bot.y),
                                         pba, pbp, bba, bbp)
        review.append(self.q_table[next_state])

        action=0
        for i,item in enumerate(review):
            if item>action:
                action=i+1
                maxreview=item
        if maxreview==0 or random.randint(1,100)==1:#全ての評価値が0か、1%の確率でランダムに
            action=random.randint(1,5)
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
                    #strlist = [str(n) for n in self.q_table]
                    strlist=[]
                    for n in self.q_table:
                        strlist.append(str(n)+"\n")
                    f.writelines(strlist)
            self.y.append(self.winrate)
            if self.count == self.trainCount:
                plt.plot(self.y)
                plt.show()
            self.game.init()


#プレイヤーの操作改善、強化学習同士の対戦、何もしない状態を追加@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class read():
    def __init__(self):
        self.q_table=[0]*810001
        self.win = tk.Tk()
        self.win.title("読み込む学習回数")
        self.label = tk.Label(text="読み込むデータの学習回数(.txtは不要)を指定してください。作成されていないと読み込めません。")
        self.box = tk.Entry()
        self.box.focus_set()
        self.label2=tk.Label(text="行う学習回数を指定してください。自分で操作する場合は0を入力してください。")
        self.box2=tk.Entry()
        self.label3 = tk.Label(text="乱数:0, 操作可能:1")
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
                self.q_table = [int(s) for s in strlist]
        self.learncount = int(self.box2.get())
        self.playORai=int(self.box3.get())
        self.win.destroy()



if __name__ == '__main__':
    Learn()
