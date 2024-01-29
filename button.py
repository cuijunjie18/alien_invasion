import pygame.font
class Button:
    """管理按钮的类"""

    def __init__(self,ai_game,msg):
        """初始化按钮资源"""

        #加载屏幕
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width,self.height = 200,50
        self.text_color = (255,255,255)
        self.button_color = (0,135,0)
        self.font = pygame.font.SysFont(None,48)

        #创建按钮的rect的对象并初始化
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        #按钮标签
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """渲染文本为图像"""
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """在屏幕上绘制按钮"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)