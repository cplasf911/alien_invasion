import sys

import pygame
from pygame.sprite import Group


import bullet
import game_functions as gf
from alien import Alien
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_botton = Button(ai_settings, screen, "play".title())
    
    # 创建储存游戏统计信息的实例，并创建计分板
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船,子弹,外星人编队
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_botton, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_botton)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

run_game()
