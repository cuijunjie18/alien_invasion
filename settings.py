class Settings:
    """游戏的设置"""

    def __init__(self):
        """初始化游戏的静态设置"""

        #屏幕设置
        self.screen_width = 1100
        self.screen_height = 700
        self.bg_color = (230,230,230)

        #飞船设置
        self.ship_limit = 3

        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allow = 12

        #外星人设置
        self.alien_drop_speed = 10

        #动态设置
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        #速度相关
        self.ship_speed = 10.0
        self.bullet_speed = 12.0
        self.alien_speed = 1.0
        #方向相关
        self.alien_direction = 1
        #得分相关
        self.alien_score = 50

    def increase_speed(self):
        """提高游戏速度设置的值"""
        self.alien_speed *= self.speedup_scale
        self.alien_score = int(self.score_scale*self.alien_score)