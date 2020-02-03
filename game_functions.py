import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_botton, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)            
        if event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_botton(ai_settings, screen, stats, sb, play_botton, ship,
                aliens, bullets, mouse_x, mouse_y)

def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_botton):
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    aliens.draw(screen)
    ship.blitme()

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活跃状态，就绘制Play按钮
    if not stats.game_active:
        play_botton.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的设置，并删除已消失的子弹"""
    # 更新子弹的设置
    bullets.update()

    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果没有达到限制就再射一枚子弹"""
    # 创建新子弹并将其加入到编组中
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建简外星人编队"""
    # 创建一个外星人，并计算一行可容纳多少外星人
    # 外星人的间距为外星人的宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
            alien.rect.height)

    # 创建第一行外星人
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                number_row)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    number_aliens_x -= 1
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并加入当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    number_rows -= 1
    return number_rows

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检测外星人位置并更新"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将外星人整体下移，并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹与外星人碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien in aliens.sprites():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb) 

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        stats.level += 1
        sb.prep_level()

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应外星人撞到飞船"""
    if stats.ships_left > 0:
        # 将ship_left - 1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查外星人是否到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 想飞船被撞一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_play_botton(ai_settings, screen, stats, sb, play_botton, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家点击Play时开始游戏"""
    botton_clicker = play_botton.rect.collidepoint(mouse_x, mouse_y)
    if botton_clicker and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        
        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置积分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空列表里的外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建群新的外星人,并且让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_high_score(stats, sb):
    """检查最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_score()