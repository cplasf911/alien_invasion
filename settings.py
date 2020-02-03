class Settings():
    """储存外星人入侵的所有设置类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed_factor = 1.5
        self.ships_limit = 3
        # 外星人的设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction为正时右移为父时左移
        self.fleet_direction = 1

        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_hight = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 10
        
        # 以什么样的速度加速
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.5
        self.alien_speed_factor = 1
        self.alien_points = 50

        # fleet_direction为正时左移，为负时右移
        fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points *= self.score_scale