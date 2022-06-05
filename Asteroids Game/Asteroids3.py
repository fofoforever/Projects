import pygame
import time
import random
import math



#Display
display_width = 800
display_height = 600
FPS = 40
#colors
BLACK = (0,0,0)
WHITE = (250,250,250)
NAVY = (30,33,71)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
gameDisplay = pygame.display.set_mode((display_width,display_height))
star_background= pygame.image.load('star.jpg').convert_alpha()
rocketImg= pygame.image.load('asteroidrocket.png').convert_alpha()
asteroidImg = pygame.image.load('asteroidImg.png').convert_alpha()
puppiesImg = pygame.image.load('PuppiesInSpace.png').convert_alpha()



#Game initiation

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Asteroids')
clock = pygame.time.Clock()

game_notover = False

def text_objects(text, font): #what will text be formated as?
	textSurface = font.render(text, True, WHITE, BLACK)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf',45)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width/2), (display_height/2)) #text position on screen
	screen.blit(TextSurf, TextRect) #blit is drawing one on top of another
	pygame.display.update()

	time.sleep(3)#time that the message show

def crash():
	message_display('Ship Terminated')
	game_notover = False 



class Rocket(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_ori = rocketImg
		self.radius= 30
		self.rect = self.image_ori.get_rect()
		self.image = self.image_ori.copy()
		pygame.draw.circle(self.image_ori, WHITE, self.rect.center, self.radius)
		self.rect.centerx = display_width/2
		self.rect.centery = display_height/2
		self.speedx = 0
		self.speedy = 0
		self.degree = 0
		self.degreef = self.degree #this is so that the degree will not always be reset to 0
		self.turnUD = 10
		self.turnRL = 0
	# def rotate(self):
	# 	keystate = pygame.key.get_pressed()
	# 	if keystate[pygame.K_d]:
	# 		self.rotationfinal = (self.rotationfinal + self.rotation_degree) % 360
	# 		rotated_image = pygame.transform.rotate(self.image_ori, self.rotationfinal)
	# 		initial_center = self.rect.center
	# 		self.image = rotated_image
	# 		self.rect = self.rotated_image.get_rect()
	# 		self.rect.center = initial_center



	#update
	def update(self):
		self.speedx = 0 
		initial_center = self.rect.center
		self.image = pygame.transform.rotate(self.image_ori, self.degree).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = initial_center

		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.rect.centerx -= 8
		if keystate[pygame.K_RIGHT]:
			self.rect.centerx += 8
		# self.rect.x += self.speedx
		# self.speedx = 0 
		if keystate[pygame.K_UP]:
			self.rect.centery -= 8
		if keystate[pygame.K_DOWN]:
			self.rect.centery += 8
		if keystate[pygame.K_r]:
			self.degreef -= 5
			self.degree = self.degreef
			if self.degree > 360:
				self.degreef = 5
				self.degree = self.degreef
			
		if keystate[pygame.K_l]:
			self.degreef += 5
			self.degree = self.degreef
			if self.degree < 0:
				self.degree = 355
				self.degree = self.degreef
		# if self.degree = 0:
		# 	self.turnUD = -10
		# 	self.turnRL = self.rect.centerx

		# if self.degree = 270:
		# 	self.turnUD = -10
		# 	self.turnRL = self.rect.centerx

		# if self.degree = 180
		# if self.degree = 90

					
		# if keystate[pygame.K_d]:
		# 		self.rotationfinal += self.rotation_degree
		# 		self.image = pygame.transform.rotate(self.image_ori, self.rotationfinal)
		# 		self.rect = self.image.get_rect(center=self.rect.center)

		# self.rect.y += self.speedy
		# self.speedy = 0
		if self.rect.centerx > display_width:
			self.rect.centerx = display_width

		if self.rect.centerx < 0:
			self.rect.centerx = 0

		if self.rect.centery < 0:
			self.rect.centery = 0
		if self.rect.centery > display_height:
			self.rect.centery = display_height
	# def rotate_right(self):
	# 	self.degree -= 5
	# 	if self.degree > 360:
	# 		self.degree = 5

	# def rotate_left(self):
	# 	self.degree += 5
	# 	if self.degree < 0:
	# 		self.degree = 355


			
	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.centery, self.degree)
		all_sprites.add(bullet)
		bullets.add(bullet)

class Asteroids(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = asteroidImg
		self.radius= 30
		self.image=pygame.transform.scale(asteroidImg, (100,100))
		self.rect = self.image.get_rect()
		# pygame.draw.circle(self.image, BLUE, self.rect.center, self.radius)
		self.rect.x = random.randrange(display_width - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > display_height + 10 or self.rect.left < -200 or self.rect.right > display_width + 200:
			self.rect.x = random.randrange(display_width - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

def restart():
	image = pygame.transform.scale(puppiesImg, (800,600))
	gameDisplay.blit(image,(0,0))
	message_display( 'YEEE!!! PRESS Anything to Restart')
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				waiting = False


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image_ori = pygame.Surface((10, 20))
		self.image_ori.fill(WHITE)
		self.rect = self.image_ori.get_rect()
		self.image = self.image_ori
		speed = 10
		self.image = pygame.transform.rotate(self.image_ori, angle)
		self.rect.bottom = y
		self.rect.centerx = x
		self.velocity_x = math.cos(math.radians(-angle)) * speed
		self.velocity_y = math.sin(math.radians(-angle)) * speed
		# self.speedy = turnUD
		# self.speedx= turnRL
		# self.degree = degree
		

	def update(self): #if it  it hits the screen it disappears
		self.rect.y += 	self.velocity_y
		self.rect.x += 	self.velocity_x
		self.center = self.rect.center
		
		# pygame.transform.rotate(self.ori_image, self.degree)
		if self.rect.bottom < 0 or self.rect.bottom > display_height:
			self.kill()
		if self.rect.centerx < 0 or self.rect.centerx > display_width:
			self.kill()
def restart():
	image = pygame.transform.scale(puppiesImg, (800,600))
	gameDisplay.blit(image,(0,0))
	message_display( 'YEEE!!! PRESS Anything to Start')
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				waiting = False
		

game_over = True
game_notover = True
	# all_sprites = pygame.sprite.Group()
	# rocks = pygame.sprite.Group()
	# bullets = pygame.sprite.Group()
	# player = Rocket()
	# all_sprites.add(player)
	# for i in range(8):
	# 	m = Asteroids()
	# 	all_sprites.add(m)
	# rocks.add(m)

while game_notover:
	if game_over:
		restart()
		game_over = False
		all_sprites = pygame.sprite.Group()
		rocks = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		player = Rocket()
		all_sprites.add(player)
		for i in range(8):
			m = Asteroids()
			all_sprites.add(m)
			rocks.add(m)	
	# continue_or_not()
		
	#keep loop running at the right speed
	clock.tick(FPS)
	# process input (events)
	for event in pygame.event.get():
		#check for closing window
		if event.type == pygame.QUIT:
			game_notover = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
			# if event.key == pygame.K_r:
			# 	player.rotate_right()
			# if event.key == pygame.K_l:
			# 	player.rotate_left()		




	# update
	all_sprites.update()

	#check if bullet hit asteroids
	hits = pygame.sprite.groupcollide(rocks, bullets, True, True, pygame.sprite.collide_circle)
	for hit in hits:
		m = Asteroids()
		all_sprites.add(m)
		rocks.add(m)

	# check if mob hits rocket
	hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
	if hits:
		crash()
		#gameExit = True
		# game_notover = True
		# gameloop()
		game_over = True

	#draw 
	gameDisplay.blit(star_background,(0,0))
	all_sprites.draw(screen)
	#AFTER drawing everything, flisp the display
	pygame.display.flip()

# else:
# 	game_notover=True


# gameloop()
pygame.quit()
quit()