# 最終課題-メイン: 迷路型ゲーム敵用 Python ソースファイル
# --------------------------
# -*- coding: utf-8 -*-
# --------------------------

# 注意
# winsound モジュールを使用したため、 Windows プラットフォーム上でないと
# 効果音が聞けません。

# --------------------------

import pygame
import random
import winsound #効果音を鳴らすため
import numpy as np
import time
from dataclasses import dataclass, field

# --------------------------
#プレイヤーの設定
PLAYER_X = 575 # プレイヤーの初期位置 x 座標
PLAYER_Y = 625 # プレイヤーの初期位置 y 座標
PLAYER_SIZE = 30 # 正方形型のプレイヤーの一辺の大きさ
PLAYER_SPEED = 4.5 # プレイヤーのスピード

#敵の設定
ENEMY_X = 475 # プレイヤーの初期位置 x 座標
ENEMY_Y = 425 # プレイヤーの初期位置 y 座標
ENEMY_SIZE = 30 # 正方形型のプレイヤーの一辺の大きさ
ENEMY_VX = 2 # Ball の x 方向の初速度
ENEMY_VY = 5 # Ball の y 方向の初速度


FPS = 60

screen = pygame.display.set_mode((1200, 800)) # screen の準備

# --------------------------

class Player: # プレイヤー
    def __init__(self, x, y, s, dx, dy):
        self.x = x # プレイヤーの左上の x 座標
        self.y = y # プレイヤーの左上の y 座標
        self.s = s # プレイヤーのサイズ
        self.dx = dx # プレイヤーの x 方向の速度
        self.dy = dy # プレイヤーの y 方向の速度
        self.hp = 0 # プレイヤーの HP(体力)

    def move_player(self):
        self.x += self.dx
        self.y += self.dy

    def move_up(self): # プレイヤーを上へ移動させる関数
        self.dy = -PLAYER_SPEED

    def move_down(self): # プレイヤーを下へ移動させる関数
        self.dy = PLAYER_SPEED

    def move_left(self): # プレイヤーを左へ移動させる関数
        self.dx = -PLAYER_SPEED

    def move_right(self): # プレイヤーを右へ移動させる関数
        self.dx = PLAYER_SPEED
        
    def stop_player(self): # パドルを停止させる関数
        self.dx = 0
        self.dy = 0

    def draw_status(self): # ステータスを描画する
        font = pygame.font.SysFont('broadway', 50)
        if self.hp >= 50:
            text = font.render(f"HP  {self.hp}", True, "white")
            screen.blit(text, (50, 675))
        else:
            text = font.render(f"HP  {self.hp}", True, "red")
            screen.blit(text, (50, 675))

class Enemy: #敵
    def __init__(self, x, y, s, vx, vy):
        self.x = x # 敵の左上の x 座標
        self.y = y # 敵の左上の y 座標
        self.s = s # 敵のサイズ
        self.vx = vx # 敵の x 方向の速度
        self.vy = vy # 敵の y 方向の速度

    def move_enemy(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15


@dataclass
class Field: # ゲーム領域
    def __init__(self, x, y, s):
        self.x = x # Field の左上のx座標
        self.y = y # Field の左上のy座標
        self.s = s # Field の大きさ
        self.Player = Player(PLAYER_X, PLAYER_Y, PLAYER_SIZE,
                             PLAYER_SPEED, PLAYER_SPEED)
        self.Enemy = Enemy(ENEMY_X, ENEMY_Y, ENEMY_SIZE,
                           ENEMY_VX, ENEMY_VY)
        self.enemies = [] # 敵のリスト
        self.hp = 100

    def create_field(self): # Field の作成
        pygame.draw.rect(screen, (127, 91,151), (self.x, self.y,
                                                 self.s, self.s))

    def create_player(self): # Player の作成
        player = pygame.image.load("player.PNG") # プレイヤー画像の読み込み
        player = player.convert() # プレイヤーの画像変換をする
        player.set_colorkey(player.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する
        screen.blit(player, (self.Player.x, self.Player.y))

    def make_enemy(self): # 敵の画像表示
        enemy = pygame.image.load("g_enemy.PNG") # 敵画像の読み込み
        enemy = enemy.convert() # 敵の画像変換をする
        enemy.set_colorkey(enemy.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する
        position = enemy.get_rect() # 敵の位置を取得
        position.center = (600, 150)
        screen.blit(enemy, position) # 敵を画面に転送
        font = pygame.font.SysFont('hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体', 35)
        text = font.render("十字キーで避けろ！", True, "white")
        position = text.get_rect() # 文字の位置を取得
        position.center = (600, 350)
        screen.blit(text, position) # 文字を画面に転送

    def make_boss(self): # ボスの画像表示
        boss = pygame.image.load("boss.PNG") # ボス画像の読み込み
        boss = boss.convert() # ボスの画像変換をする
        boss.set_colorkey(boss.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する
        position = boss.get_rect() # ボスの位置を取得
        position.center = (600, 150)
        screen.blit(boss, position) # ボスを画面に転送
        font = pygame.font.SysFont('hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体', 35)
        text = font.render("ボスだ・・・!!!", True, "red")
        position = text.get_rect() # 文字の位置を取得
        position.center = (600, 350)
        screen.blit(text, position) # 文字を画面に転送

    def create_enemy(self): # Enemy の作成
        pygame.draw.ellipse(screen, (255, 239, 110),(self.Enemy.x, self.Enemy.y,
                                                     self.Enemy.s, self.Enemy.s))

    def create(self): #オブジェクトを纏めて作成する関数
        screen.fill((0, 0, 0))
        objects = [self.Player, self]
        for obj in objects:
            obj.draw_status()
        self.create_field()
        self.create_player()
        self.make_enemy()
        self.create_enemy()
        pygame.display.flip() # 描画内容の更新

    def create_boss(self): # ボス対戦画面を作成する関数
        screen.fill((0, 0, 0))
        objects = [self.Player, self]
        for obj in objects:
            obj.draw_status()
        self.create_field()
        self.create_player()
        self.make_boss()
        self.create_enemy()
        pygame.display.flip() # 描画内容の更新
        
    def collision_field(self): # Field と Enemy の衝突に関する関数
        if (self.Enemy.y <= self.y
            or self.y + self.s <= self.Enemy.y + self.Enemy.s):
            self.Enemy.vy = -self.Enemy.vy*1.005
        if (self.Enemy.x <= self.x
            or self.x + self.s <= self.Enemy.x + self.Enemy.s):
            self.Enemy.vx = -self.Enemy.vx

    def  collision_eneplay(self): # Player と Enemy の衝突に関する関数
        px = self.Enemy.x + self.Enemy.s/2 # Enemy の中心座標x
        py = self.Enemy.y + self.Enemy.s/2 # Enemy の中心座標y
        p = np.array([px, py]) # Enemy の中心Pを表すベクトル

        side_list = [
            [self.Player.x, self.Player.y,
             self.Player.x+self.Player.s, self.Player.y],
            [self.Player.x, self.Player.y,
             self.Player.x, self.Player.y+self.Player.s],
            [self.Player.x+self.Player.s, self.Player.y,
             self.Player.x+self.Player.s, self.Player.y+self.Player.s],
            [self.Player.x, self.Player.y+self.Player.s,
             self.Player.x+self.Player.s, self.Player.y+self.Player.s]]
        for side in side_list:
            a = np.array([side[0],side[1]]) # Player の辺の一方の点を表すベクトル
            b = np.array([side[2],side[3]]) # Player の辺の他方の点を表すベクトル
            veca = p-a # Player の辺の一方の点からボールの中心Pへ向かうベクトルa
            vecb = p-b # Player の辺の他方の点からボールの中心Pへ向かうベクトルb
            vecs = b-a # Player の辺を表すベクトルs

            dot_as = np.dot(veca,vecs) # ベクトルaとベクトルsの内積dot
            dot_bs = np.dot(vecb,vecs) # ベクトルbとベクトルsの内積dot
                    
            la = ((px-side[0])**2+(py-side[1])**2)**(1/2) # ベクトルaのノルム
            lb = ((px-side[2])**2+(py-side[3])**2)**(1/2) # ベクトルbのノルム
            ls = ((side[2]-side[0])**2 +
                  (side[3]-side[1])**2)**(1/2) # ベクトルsのノルム

            # ベクトルaとベクトルsのなす角thetaを求める
            theta = np.arccos(dot_as/(ls*la))

            # Enemy の中心Pと Player の辺までの距離distance
            dis = la * np.sin(theta)
            
            # Enemy と Player の辺の衝突判定
            if dis <= self.Enemy.s/2:
                if dot_as * dot_bs <= 0:
                    if side[0]==side[2]:
                        self.Enemy.vx = -self.Enemy.vx
                        self.Player.hp -= 20
                        self.make_SE('attack.wav')
                    if side[1]==side[3]:
                        self.Enemy.vy = -self.Enemy.vy*0.8
                        self.Player -= 20
                        self.make_SE('attack.wav')
                if self.Enemy.s > la or self.Enemy.s > lb:
                    self.Enemy.vx = -self.Enemy.vx*0.8
                    self.Enemy.vy = -self.Enemy.vy*0.9
                    self.Player.hp -= 20
                    self.make_SE('attack.wav')

    def collision_wall(self): #プレイヤーとプレイフィールドの衝突に関する関数
        if (self.Player.y < self.y
            or self.y + self.s < self.Player.y + self.Player.s):
            self.Player.dy = -self.Player.dy
        if (self.Player.x < self.x
            or self.x + self.s < self.Player.x + self.Player.s):
            self.Player.dx = -self.Player.dx

    def collision(self): # 衝突判定を纏めて行う
        self.collision_field()
        self.collision_eneplay()
        self.collision_wall()

    def draw_status(self): # 敵のステータスを描画する
        font = pygame.font.SysFont('broadway', 50)
        text = font.render(f"HP  {self.hp:.0f}", True, "red")
        screen.blit(text, (900, 35))
        
    def make_SE(self, wav):
        with open(wav, 'rb') as file: # wav ファイルの効果音を鳴らす
                    data = file.read()
        winsound.PlaySound(data, winsound.SND_MEMORY)

    def check_key(self):
        event = pygame.event.get()
        for value in event:
            if value.type == pygame.KEYDOWN:
                if value.key == pygame.K_UP:
                    self.Player.move_up()
                elif value.key == pygame.K_DOWN:
                    self.Player.move_down()
                elif value.key == pygame.K_LEFT:
                    self.Player.move_left()
                elif value.key == pygame.K_RIGHT:
                    self.Player.move_right()
            if value.type == pygame.KEYUP:
                if value.key == pygame.K_UP:
                    self.Player.stop_player()
                elif value.key == pygame.K_DOWN:
                    self.Player.stop_player()
                elif value.key == pygame.K_LEFT:
                    self.Player.stop_player()
                elif value.key == pygame.K_RIGHT:
                    self.Player.stop_player()
        

    def animate(self, SENEMY, hp, enemy_hp):
        self.hp = enemy_hp
        self.Player.hp = hp
        self.Enemy.x = ENEMY_X
        self.Enemy.y = ENEMY_Y
        self.create()
        time.sleep(3.00)
        while SENEMY:
            clock = pygame.time.Clock() # 時計オブジェクト
            self.check_key()
            self.create()
            self.Player.move_player()
            self.Enemy.move_enemy()
            self.collision()
            self.hp -= 0.25 
            clock.tick(FPS) # 毎秒の呼び出し回数に合わせて遅延をかける
            if self.hp == 0: # 敵の HP が 0 になった場合
                font = pygame.font.SysFont('broadway', 75)
                text = font.render("You Win!!", True, "yellow")
                position = text.get_rect() # 文字の位置を取得
                position.center = screen.get_rect().center # screen の中心に揃える
                screen.blit(text, position) # テキストを画面に転送
                pygame.display.flip() # 描画内容の更新
                self.make_SE('win.wav')
                pygame.mixer.music.stop()
                pygame.mixer.music.load("map_bgm.wav")
                pygame.mixer.music.play(-1)
                SENEMY = False
                return SENEMY, self.Player.hp
            if self.Player.hp <= 0: # プレイヤーがやられた場合
                SENEMY = False
                pygame.mixer.music.stop()
                return SENEMY, self.Player.hp

    def fight_boss(self, SENEMY, hp, enemy_hp): # ボス戦の描画をする関数
        self.hp = enemy_hp
        self.Player.hp = hp
        self.Enemy.x = ENEMY_X
        self.Enemy.y = ENEMY_Y
        self.create_boss()
        time.sleep(3.00)
        while SENEMY:
            clock = pygame.time.Clock() # 時計オブジェクト
            self.check_key()
            self.create_boss()
            self.Player.move_player()
            self.Enemy.move_enemy()
            self.collision()
            self.hp -= 0.25 
            clock.tick(FPS) # 毎秒の呼び出し回数に合わせて遅延をかける
            if self.hp == 0: # 敵の HP が 0 になった場合
                font = pygame.font.SysFont('broadway', 75)
                text = font.render("You Win!!", True, "yellow")
                position = text.get_rect() # 文字の位置を取得
                position.center = screen.get_rect().center # screen の中心に揃える
                screen.blit(text, position) # テキストを画面に転送
                pygame.display.flip() # 描画内容の更新
                self.make_SE('win.wav')
                pygame.mixer.music.stop()
                SENEMY = False
                return SENEMY, self.Player.hp
            if self.Player.hp <= 0: # プレイヤーがやられた場合
                pygame.mixer.music.stop()
                SENEMY = False
                return SENEMY, self.Player.hp
