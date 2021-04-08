import sys
import pygame
from bullet import Bullet
from alien import Alien
def check_keydown_events(event, ai_settings, screen, ship, bullets):
	'''响应按下'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
	'''如果没有到达限制就创建新子弹'''
		#创建一颗子弹，并加入编组bullets
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings, screen, ship)

			bullets.add(new_bullet)
def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
	'''响应按键和鼠标事件'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, aliens, bullets):
	#每次循环时都重新绘制屏幕
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(aliens, bullets):
	'''更新子弹的位置并删除消失的子弹'''
	#更新位置
	bullets.update()
	#删除消失子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	#检查是否击中外星人，并删除
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

def get_number_aliens_x(ai_settings, alien_width):
	'''计算可以容纳多少列'''
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def creat_alien(ai_settings,screen,aliens,alien_number, row_number):
	'''创建一个外星人并且放在当行'''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width+2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height+2 * alien.rect.height * row_number
	aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
	'''计算可以容纳多少行'''
	available_space_y = (ai_settings.screen_height - (3 * alien_height) -
		ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
	'''创建外星人群'''
	#创建一个外星人，并计算每行可容纳多少个外星人
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, 
		alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			creat_alien(ai_settings, screen, aliens, alien_number, row_number)
	#创建第一行外星人
	for alien_number in range(number_aliens_x):
		creat_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, aliens):
	'''更新外星人群中所有外星人的位置，检查是否位于屏幕边缘'''
	check_fleet_edges(ai_settings, aliens)
	aliens.update()




