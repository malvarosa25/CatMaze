# 最終課題-メイン: 迷路型ゲーム
# --------------------------
# -*- coding: utf-8 -*-
# --------------------------

# 注意
# winsound モジュールを使用したため、 Windows プラットフォーム上でないと
# 効果音が聞けません。

# --------------------------

import pygame
import random
import time
from dataclasses import dataclass, field
from maze import Maze
from senemy import Field
from status import Status
import winsound #効果音を鳴らすため

WALL_X = 30 # floormap[0][0]から迷路を描く際の始点x座標
WALL_Y = 30 # floormap[0][0]から迷路を描く際の始点y座標
SIZE = 40 # マスの大きさ
DURATION = 5.00

#ゲーム領域の設定
FIELD_X = 450
FIELD_Y = 400
FIELD_SIZE = 300

# --------------------------

pygame.init() # Pygame のサブモジュールの初期化
screen = pygame.display.set_mode((1200, 800)) # screen の準備
font = pygame.font.SysFont('broadway', 50)

# --------------------------
class Cat: # プレイヤーである猫
    def __init__(self):
        self.hp = 100 # HP(ヒットポイント：体力)
        self.fish = 0 # 回復アイテムである魚の個数

    def draw_hp(self):
        if self.hp >= 50:
            text = font.render(f"HP  {self.hp}", True, "white")
            screen.blit(text, (30, 675))
        else:
            text = font.render(f"HP  {self.hp}", True, "red")
            screen.blit(text, (30, 675))

    def draw_fish(self):
        text = font.render(f"FISH  {self.fish}", True, "white")
        screen.blit(text, (30, 730))

    def get_fish(self):
        self.make_SE("cat.wav")
        self.fish += 1

    def lose_fish(self):
        if self.fish == 0:
            self.make_SE('wall.wav')
        else:
            self.hp += 20
            self.fish -= 1
            self.make_SE('eat.wav')
                    
    def draw_status(self): # プレイヤーのステータスを描画する
        self.draw_hp()
        self.draw_fish()
        
    def make_SE(self, wav):
        with open(wav, 'rb') as file: # wav ファイルの効果音を鳴らす
                    data = file.read()
        winsound.PlaySound(data, winsound.SND_MEMORY)

                    
@dataclass
class MazeGame:
    maze: Maze = field(init = False, default = None)
    player: tuple = field(init=False, default = None)
    cat: Cat = field(init = False, default = None)
    senemy: Field = field(init = False, default = None)
    status: Status = field(init = False, default = None)

    def __init__(self):
        self.LOOP = True
        self.TITLE = True # タイトルを表示するかどうか
        self.EXAMINATION = True # 説明を表示するかどうか
        self.SENEMY = False # シューティング戦の画面へ移動するかどうか
        self.BOSS = False # ボス戦の画面へ移動するかどうか
        self.BGM = False # BGM を流すかどうか
        self.ENDING = False # ゲームクリアかどうか
        self.KEY = False # 鍵を持っているかどうか

    def draw_title(self):
        title = pygame.image.load("title.PNG")
        screen.blit(title, (0, 0)) # screen に背景ごと画像を転送する
        pygame.display.flip() # 描画内容の更新
        event = pygame.event.get()
        for value in event:
            if value.type == pygame.KEYDOWN:
                if value.key == pygame.K_RETURN:
                    self.make_SE("enter.wav")
                    self.TITLE = False

    def draw_examination(self):
        examin = pygame.image.load("examination.PNG")
        screen.blit(examin, (0, 0)) # screen に背景ごと画像を転送する
        pygame.display.flip() # 描画内容の更新
        event = pygame.event.get()
        for value in event:
            if value.type == pygame.KEYDOWN:
                if value.key == pygame.K_RETURN:
                    self.make_SE("enter.wav")
                    self.BGM = True
                    self.EXAMINATION = False

    def draw_floormap(self):
        princess = pygame.image.load("princess.PNG") # ゴールにいる姫猫画像の読み込み
        princess = princess.convert() # 姫猫の画像変換をする
        princess.set_colorkey(princess.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する
        fish = pygame.image.load("fish.PNG") # 回復アイテム（魚）の画像読み込み
        fish = fish.convert() # 魚の画像変換をする
        fish.set_colorkey(fish.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する
        key = pygame.image.load("key.PNG") # 鍵の画像読み込み
        key = key.convert() # 鍵の画像変換をする
        key.set_colorkey(key.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する        
        for row in range(len(self.maze.floormap)):
            for row in range(len(self.maze.floormap)):
                for column in range(len(self.maze.floormap[row])):
                    if self.maze.floormap[row][column] == 1: # マス目が壁だったら
                        pygame.draw.rect(screen, (117, 70, 152),
                                         (WALL_X+SIZE*column, WALL_Y+SIZE*row,
                                         SIZE, SIZE))
                    if self.maze.floormap[row][column] == 2: # マス目が魚獲得マスだったら
                        screen.blit(fish, (WALL_X+SIZE*column, WALL_Y+SIZE*row))
                    if self.maze.floormap[row][column] == 5: # マス目が鍵マスだったら
                        screen.blit(key, (WALL_X+SIZE*column, WALL_Y+SIZE*row))
                    if self.maze.floormap[row][column] == 6: # マス目が扉だったら
                        pygame.draw.rect(screen, (192, 26, 65),
                                         (WALL_X+SIZE*column, WALL_Y+SIZE*row,
                                         SIZE, SIZE))
                    if self.maze.floormap[row][column] == 9: # マス目がゴールだったら
                        screen.blit(princess, (WALL_X+SIZE*column, WALL_Y+SIZE*row))


    def set_player(self, i, j):
        self.player = (i, j) # (row, column)

    def draw_player(self):
        x = WALL_X + SIZE * self.player[1] # プレイヤーがいるマスの左上の x 座標
        y = WALL_Y + SIZE * self.player[0] # プレイヤーがいるマスの左上の y 座標
        player = pygame.image.load("player.PNG") # プレイヤー画像の読み込み
        player = player.convert() # プレイヤーの画像変換をする
        player.set_colorkey(player.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する
        screen.blit(player, (x, y))

    def draw_itembutton(self): # 魚を使用するためのボタンを作成する
        fish_button = pygame.Rect(375, 675, 127.5, 75) # button となる四角形を作成
        fish_text = font.render("FISH", True, "blue")
        pygame.draw.rect(screen, (142, 209, 224), fish_button)
        screen.blit(fish_text, (380, 685))
        return fish_button
    
    def redraw(self):
        self.draw_floormap()
        self.draw_player()
        self.cat.draw_status()
        self.status.draw_status(screen)
        pygame.display.flip() # 描画内容の更新
        screen.fill((0, 0, 0))
        
    def make_SE(self, wav):
        with open(wav, 'rb') as file: # wav ファイルの効果音を鳴らす
                    data = file.read()
        winsound.PlaySound(data, winsound.SND_MEMORY)

    def player_up(self): # プレイヤーを上へ移動させる
        while True:
            i = self.player[0] # 現在プレイヤーがいる行
            j = self.player[1] # 現在プレイヤーがいる列
            if self.maze.floormap[i-1][j] == 6: # 移動先が扉の場合
                self.make_SE('wall.wav')
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont('hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体', 50)
                text = font.render("鍵が必要だにゃ", True, "white")
                position = text.get_rect() # 文字の位置を取得
                position.center = screen.get_rect().center # screen の中心に揃える
                screen.blit(text, position) # テキストを画面に転送
                pygame.display.flip() # 描画内容の更新
                time.sleep(3.00)
                break
            elif self.maze.floormap[i-1][j] != 1 : # 移動先が、壁ではない場合
                self.set_player(i-1, j)
                self.status = Status(self.cat.hp)
                self.status.decide_number()
                self.redraw()
                self.make_SE('move.wav')
                self.maze.floormap[i-1][j] = self.check_mass(i-1, j)
                break
            else:
                self.make_SE('wall.wav')
                break

    def player_down(self): # プレイヤーを下へ移動させる
        while True:
            i = self.player[0] # 現在プレイヤーがいる行
            j = self.player[1] # 現在プレイヤーがいる列
            if self.maze.floormap[i+1][j] == 6: # 移動先が扉の場合
                self.make_SE('wall.wav')
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont('hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体', 50)
                text = font.render("鍵が必要だにゃ", True, "white")
                position = text.get_rect() # 文字の位置を取得
                position.center = screen.get_rect().center # screen の中心に揃える
                screen.blit(text, position) # テキストを画面に転送
                pygame.display.flip() # 描画内容の更新
                time.sleep(3.00)
                break
            elif self.maze.floormap[i+1][j] != 1: # 移動先が、壁ではない場合
                self.set_player(i+1, j)
                self.status = Status(self.cat.hp)
                self.status.decide_number()
                self.redraw()
                self.make_SE('move.wav')
                self.maze.floormap[i+1][j] = self.check_mass(i+1, j)
                break
            else:
                self.make_SE('wall.wav')
                break

    def player_left(self): # プレイヤーを左へ移動させる
        while True:
            i = self.player[0] # 現在プレイヤーがいる行
            j = self.player[1] # 現在プレイヤーがいる列
            if self.maze.floormap[i][j-1] == 6: # 移動先が扉の場合
                self.make_SE('wall.wav')
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont('hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体', 50)
                text = font.render("鍵が必要だにゃ", True, "white")
                position = text.get_rect() # 文字の位置を取得
                position.center = screen.get_rect().center # screen の中心に揃える
                screen.blit(text, position) # テキストを画面に転送
                pygame.display.flip() # 描画内容の更新
                time.sleep(3.00)
                break
            elif self.maze.floormap[i][j-1] != 1 : # 移動先が、壁ではない場合
                self.set_player(i, j-1)
                self.status = Status(self.cat.hp)
                self.status.decide_number()
                self.redraw()
                self.make_SE('move.wav')
                self.maze.floormap[i][j-1] = self.check_mass(i, j-1)
                break
            else:
                self.make_SE('wall.wav')
                break

    def player_right(self): # プレイヤーを右へ移動させる
        while True:
            i = self.player[0] # 現在プレイヤーがいる行
            j = self.player[1] # 現在プレイヤーがいる列
            if self.maze.floormap[i][j+1] == 6: # 移動先が扉の場合
                self.make_SE('wall.wav')
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont('hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体', 50)
                text = font.render("鍵が必要だにゃ", True, "white")
                position = text.get_rect() # 文字の位置を取得
                position.center = screen.get_rect().center # screen の中心に揃える
                screen.blit(text, position) # テキストを画面に転送
                pygame.display.flip() # 描画内容の更新
                time.sleep(3.00)
                break
            elif self.maze.floormap[i][j+1] != 1 : # 移動先が、壁ではない場合
                self.set_player(i, j+1)
                self.status = Status(self.cat.hp)
                self.status.decide_number()
                self.redraw()
                self.make_SE('move.wav')
                self.maze.floormap[i][j+1] = self.check_mass(i, j+1)
                break
            else:
                self.make_SE('wall.wav')
                break

    def check_key(self):
        if self.SENEMY == False:
            event = pygame.event.get()
            fish_button = self.draw_itembutton()
            for value in event:
                if value.type == pygame.KEYDOWN:
                    if value.key == pygame.K_UP:
                        self.player_up()
                    elif value.key == pygame.K_DOWN:
                        self.player_down()
                    elif value.key == pygame.K_LEFT:
                        self.player_left()
                    elif value.key == pygame.K_RIGHT:
                        self.player_right()
                pos = pygame.mouse.get_pos()
                if value.type == pygame.MOUSEBUTTONDOWN:
                    if fish_button.collidepoint(pos):
                        self.cat.lose_fish()

    def get_fish(self, i, j):
        if self.maze.floormap[i][j] == 2: # プレイヤーの行先が魚獲得マスの場合
            self.cat.get_fish()
            return 0

    def encount(self, i, j):
        if self.maze.floormap[i][j] == 3: # プレイヤーの行先が敵の場合
            self.make_SE("encount.wav")
            self.SENEMY = True
            return 0

    def get_key(self, i, j):
        if self.maze.floormap[i][j] == 5: # プレイヤーの行先が鍵の場合
            self.make_SE("key.wav")
            self.KEY = True
            return 0
    
    def encount_boss(self, i, j):
        if self.maze.floormap[i][j] == 7: # プレイヤーの行先がボスの場合
            pygame.mixer.music.stop()
            self.make_SE("encount_boss.wav")
            self.BOSS = True
            return 0

    def goal(self, i, j):
        if self.maze.floormap[i][j] == 9: # プレイヤーの行先がゴールの場合
            self.ENDING = True
            
    def check_mass(self, i, j): #行先のマス目を調べる関数
        self.get_fish(i, j)
        self.get_key(i, j)
        self.encount(i, j)
        self.encount_boss(i, j)
        self.goal(i, j)
    
    def start(self):
        self.maze = Maze()
        self.cat = Cat()
        self.senemy = Field(FIELD_X, FIELD_Y, FIELD_SIZE)
        self.status = Status(self.cat.hp)
        self.maze.from_file(r"maze.txt")
        for row in range(len(self.maze.floormap)):
            for column in range(len(self.maze.floormap[row])):
                if self.maze.floormap[row][column] == 8:
                    start_x = row # スタート地点の行
                    start_y = column # スタート地点の列
        self.set_player(start_x, start_y) # プレイヤーをスタート地点の座標にセット
        self.redraw()
        # イベント処理の登録
        self.check_key()

    def go(self):
        self.redraw()
        # イベント処理の登録
        self.check_key()
        self.gameover()

    def gameover(self):
        if self.cat.hp == 0:
            pygame.mixer.music.stop()
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('broadway', 50)
            text = font.render("GAME OVER", True, "red")
            position = text.get_rect() # 文字の位置を取得
            position.center = screen.get_rect().center # screen の中心に揃える
            screen.blit(text, position) # テキストを画面に転送
            pygame.display.flip() # 描画内容の更新
            self.make_SE("gameover.wav")
            time.sleep(3.00)
            self.LOOP = False
            
# --------------------------
# main routine
game = MazeGame()
game.start()
pygame.mixer.init(frequency = 44100)
pygame.mixer.music.load("opening.wav")
pygame.mixer.music.play(-1)

while game.EXAMINATION:
    if game.TITLE == True:
        game.draw_title()
    elif game.TITLE == False and game.EXAMINATION == True:
        game.draw_examination()

if game.BGM == True:
    pygame.mixer.music.stop()
    pygame.mixer.music.load("map_bgm.wav")
    pygame.mixer.music.play(-1)

while game.LOOP: # 描画のルール
    for event in pygame.event.get():
        # Pygame の「閉じる」ボタン処理
        if event.type == pygame.QUIT:
            game.LOOP = False
    if game.SENEMY == True:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("buttle.wav")
        pygame.mixer.music.play(-1)
        game.SENEMY, game.cat.hp = game.senemy.animate(game.SENEMY, game.cat.hp, 100)
    elif game.BOSS == True:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("buttle.wav")
        pygame.mixer.music.play(-1)
        game.BOSS, game.cat.hp = game.senemy.fight_boss(game.BOSS, game.cat.hp, 500)
    elif game.ENDING == True:
        ending = pygame.image.load("ending.PNG")
        screen.blit(ending, (0, 0)) # screen に背景ごと画像を転送する
        pygame.display.flip() # 描画内容の更新
        game.make_SE("goal.wav")
        game.LOOP = False
    else:
        for row in range(len(game.maze.floormap)):
            for column in range(len(game.maze.floormap[row])):
                if game.maze.floormap[row][column] == 6:
                    if game.KEY == True:
                        game.maze.floormap[row][column] = 0
        game.go()
pygame.quit() # 画面を閉じる

