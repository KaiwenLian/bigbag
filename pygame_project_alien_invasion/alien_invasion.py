import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("外星人入侵")
	#飞船,子弹编组和外星人编组
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	#创建外星人群
	gf.create_fleet(ai_settings, screen, ship, aliens)
	#开始游戏主循环
	while True:
		#监视鼠标和键盘事件
		gf.check_events(ai_settings, screen, ship, bullets)
		ship.update()
		gf.update_bullets(aliens, bullets)
		gf.update_aliens(ai_settings, aliens)
		#每次循环时都重新绘制屏幕
		#让最近绘制的屏幕可见
		gf.update_screen(ai_settings, screen, ship, aliens, bullets)
run_game()