import pygame.font
from pygame.sprite import Sprite
from ship import Ship
class Scoreboard:
    """显示得分的类"""

    def __init__(self,ai_game):
        """初始化计分板"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #加载显示得分的颜色及字体
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,28)

        #加载图像
        self.prep_image()
    
    def prep_image(self):
        """加载文本图像"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分渲染为图像"""
        round_score = round(self.stats.score,-1)
        score_str = f"Score:{round_score:,}"
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()

        #初始化得分板的位置
        self.score_rect.right = self.screen_rect.right - 30
        self.score_rect.top = 10

    def prep_high_score(self):
        """加载最高分"""
        #获取最高分图像
        high_score = round(self.stats.high_score,-1)
        high_score_str = f"High score:{high_score:,}"
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
        
        #设置最高分显示位置
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = 10
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        """加载游戏等级"""
        #渲染等级图像
        level_str = f"Level:{self.stats.level}"
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)

        #设置等级位置
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom
        self.level_rect.right = self.screen_rect.right - 30

    def prep_ships(self):
        """加载飞船剩余数"""
        self.ships = pygame.sprite.Group()
        for number in range(self.stats.ships_left):
            #注意这里
            ship = Ship(self.ai_game)
            ship.rect.x = number*ship.rect.width + 10
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """展示得分及等级"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)