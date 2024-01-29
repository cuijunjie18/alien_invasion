import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    """管理外星人的类"""

    def __init__(self,ai_game):
        """初始化外星人资源"""
        
        super().__init__()
        #加载设置
        self.settings = ai_game.settings

        #加载屏幕资源
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #加载外星人资源
        self.image = pygame.image.load('images/my_alien.bmp')
        self.rect = self.image.get_rect()

        #初始化外星人位置信息
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人精确的水平位置
        self.x = float(self.rect.x)

    def update(self):
        """移动外星人"""
        #注意x与rect.x的区别
        self.x += self.settings.alien_speed*self.settings.alien_direction
        self.rect.x = self.x

    def check_edge(self):
        """检查外星人是否到达左右边界"""
        return (self.rect.right >= self.screen_rect.right) or (self.rect.left <= 0)
    
