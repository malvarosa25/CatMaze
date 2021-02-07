# 最終課題-メイン: 迷路型ゲームステータス用 Python ソースファイル
# --------------------------
# -*- coding: utf-8 -*-
# --------------------------

import pygame
import random

class Status: # 猫の様子を表すクラス
    def __init__(self, hp):
        self.hp = hp
        self.status = [
            "おなか すいたにゃ～",
            "まだ あるくのにゃ？",
            "てきさんと おはなししたいにゃ",
            "ねこは かいすいのめるんだにゃ",
            "あっ！むし とんでる！",
            "つかれたにゃ・・・",
            "もう ぼろぼろにゃ・・・",
            "おさかなさん どこにゃ？",
            "だるだる だにゃ・・・",
            "おうち かえるにゃ・・・"
            ]
        self.number = 0
        
    def draw_cat(self, screen):
        cat = pygame.image.load("cat_status.PNG") # 敵画像の読み込み
        cat = cat.convert() # 猫の画像変換をする
        cat.set_colorkey(cat.get_at((0, 0))) # 左上の (0, 0) を背景色に指定する
        position = cat.get_rect() # 猫の位置を取得
        position.center = (950, 400)
        screen.blit(cat, position) # 猫を画面に転送

    def decide_number(self):
        if self.hp >= 50:
            self.number = random.randint(0, 4)
        else:
            self.number = random.randint(5, 9)

    def write_dialogue(self, screen):
        font = pygame.font.SysFont('hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体', 20)
        text = font.render(f"{self.status[self.number]}", True, "white")
        position = text.get_rect() # 文字の位置を取得
        position.center = (955, 525)
        screen.blit(text, position) # 文字を画面に転送

    def draw_status(self, screen):
        self.draw_cat(screen)
        self.write_dialogue(screen)
