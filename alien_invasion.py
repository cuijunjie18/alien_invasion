#导入必要模块
import pygame
import sys
import json
import random
from time import sleep
#导入游戏对象
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
#导入设置
from settings import Settings
#导入统计信息
from game_stats import GameStats
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self):
        """初始化游戏并创建环境资源"""
        pygame.init()
        #创建时钟及初始化设置
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        #创建游戏屏幕
        self.screen = pygame.display.set_mode(
        (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #创建游戏的物品
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.before = 0
        self.before_alien = 1100
        self.alien_number = 0
        self.alien_kill = 0

        #创建统计信息
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #创建游戏状态
        self.game_active = False

        #创建Play按钮
        self.play_button = Button(self,"Play")

    def run_game(self):
        """游戏主循环"""
        while True:
            self._check_event()
            if self.game_active:
                self._create_alien()
                self.ship.update()
                self ._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)


    def _check_event(self):
        """事件侦测"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_down()
    
    def _check_mouse_down(self):
        """检查鼠标按下的事件"""
        mouse_pos = pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)

    def _check_key_down(self,event):
        """检查键盘按下事件"""
        if event.key == pygame.K_RIGHT and self.game_active:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT and self.game_active:
            self.ship.moving_left = True
        elif event.key == pygame.K_p and self.game_active == False:
            self._start_game()
        elif event.key == pygame.K_SPACE and self.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_key_up(self,event):
        """检查键盘松开事件"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_play_button(self,mouse_pos):
        """检查鼠标是否按在Play处"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game_active == False:
            self._start_game()
    
    def _fire_bullet(self):
        """新建子弹"""
        #如果还未超过屏幕的限制
        if len(self.bullets) < self.settings.bullet_allow:
            new_bullet = Bullet(self)
            self.before = new_bullet.rect.y
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """操作屏幕上的子弹"""
        #更新所有已发射子弹的位置
        self.bullets.update()
        self.before -= self.settings.bullet_speed
        #无限火力
        if self.before <= 600:
            self._fire_bullet()
        #删除已经失效的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #检查子弹碰撞
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """检查子弹与外星人的碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for value in collisions.values():
                self.stats.score += len(value)*self.settings.alien_score
                self.alien_kill += len(value)
            self.sb.prep_score()
            self._check_high_score()
        if  self.alien_kill == self.settings.alien_number_limit:
            #提高游戏难度
            self.settings.increase_level()
            self.stats.level += 1
            self.sb.prep_level()
            #清空全部子弹
            self.bullets.empty()
            #进入新关卡
            self._new_level()
    
    def _check_high_score(self):
        """检查最高分是否被打破"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            temp = json.dumps(self.stats.high_score)
            self.stats.path.write_text(temp)
            self.sb.prep_high_score()

    def _create_alien(self):
        """创建单个外星人"""
        if self.before_alien >= 100 and self.alien_number < self.settings.alien_number_limit:
            self.alien_number += 1
            new_alien = Alien(self)
            #这里要特殊处理alien.x!!!!
            new_alien.x = random.randint(0,self.settings.screen_width - new_alien.rect.width)
            new_alien.rect.x = new_alien.x
            self.before_alien = new_alien.rect.y
            self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外星人"""
        self._check_fleet_edge()
        self.aliens.update()
        #更新最后生成的外星人的高度
        self.before_alien += self.settings.alien_speed_y
        #检测外星人与飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #检测外星人是否到达基地
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
    
    def _check_fleet_edge(self):
        """在有外星人到达边界时做出反应"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction(alien)
                
    
    def _change_fleet_direction(self,alien):
        """改变外星人的移动方向"""
        alien.direction *= -1

    def _ship_hit(self):
        """响应飞船与外星人的碰撞"""
        if self.stats.ships_left > 1:
            #飞船数减1
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #清空外星人与子弹
            self.aliens.empty()
            self.bullets.empty()
            #重置飞船位置
            self.ship.center_ship_place()
            #视觉暂停
            sleep(0.5)
            #重新开始当前等级的关卡
            self._new_level()
        else:
            self._end_game()
    
    def _start_game(self):
        """重置游戏并开始"""
        #重置游戏的统计信息
        self.stats.reset_stats()
        self.sb.prep_image()
        self.game_active = True
        #还原游戏设置
        self.settings.initialize_dynamic_settings()
        #清空当前屏幕上物品
        self.aliens.empty()
        self.bullets.empty()
        #重置飞船位置
        self._new_level()
        self.ship.center_ship_place()
        #隐藏光标
        pygame.mouse.set_visible(False)

    def _end_game(self):
        """结束游戏"""
        self.game_active = False
        pygame.mouse.set_visible(True)

    def _new_level(self):
        """进入新关卡或重新当前关卡"""
        self.alien_kill = 0
        self.alien_number = 0

    def _update_screen(self):
        """更新屏幕"""
        #设置背景,同时将原屏幕上的图像全部覆盖
        self.screen.fill(self.settings.bg_color)
        #绘制飞船
        self.ship.blitme()
        #绘制全部子弹(此处为对sprites操作)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #绘制全部外星人
        self.aliens.draw(self.screen)
        #绘制得分,等级,飞船数
        self.sb.show_score()
        #如果游戏处于非活动状态,就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()



if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

