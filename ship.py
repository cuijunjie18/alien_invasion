import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    """管理的飞船类"""

    def __init__(self,ai_game):
        """初始化飞船并设置其在屏幕上的位置"""
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/my_ship.bmp')
        self.rect = self.image.get_rect()

        #每艘新飞船都放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        #飞船的速度属性及浮点数移动坐标
        self.speed = ai_game.settings.ship_speed
        self.x  = float(self.rect.x)

        #飞船的移动状态
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """改变飞船的位置(x坐标)"""
        if self.moving_left and ((self.x + self.speed) > self.screen_rect.left):
            self.x -= self.speed
        elif self.moving_right and ((self.x + self.speed) < self.screen_rect.right-30):
            self.x += self.speed
        self.rect.x = self.x
        
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def center_ship_place(self):
        """将飞船位置重置"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)