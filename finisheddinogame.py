#Code based on a Dino Game workshop by Kurius
from Kurius
import pygame, random

pygame.init()

sh = 300
sl = 600

win = pygame.display.set_mode((sl, sh))
pygame.display.set_caption('No Internet')

clock = pygame.time.Clock()

class Dinosaur(object):
	def __init__(self):
		self.w = 35
		self.h = 50
		self.x = 100
		self.y = sh-150
		self.jump_inc = 0
		self.jumping = False
		self.crouching = False
		self.run_img = [pygame.image.load("walk1.png"), pygame.image.load("walk2.png")]
		self.crouch_img = [pygame.image.load("crouch1.png"), pygame.image.load("crouch2.png")]
		self.jump_img = pygame.image.load("jump.png")
		self.run_inc = 0
		self.crouch_inc = 0

	def draw(self):
		#pygame.draw.rect(win, (125,125,125), (self.x, self.y, self.w, self.h))
		#pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.w, self.h), 1)

		if self.jumping:
			win.blit(self.jump_img, (self.x, self.y))

		elif self.crouching:
			win.blit(self.crouch_img[self.crouch_inc//5], (self.x, self.y))

			if self.crouch_inc == 9:
				self.crouch_inc = -1
			self.crouch_inc += 1

		else:
			win.blit(self.run_img[self.run_inc//5], (self.x, self.y))

			if self.run_inc == 9:
				self.run_inc = -1
			self.run_inc += 1


	def move(self):
		keys = pygame.key.get_pressed()

		if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not self.jumping and not self.crouching:
			self.jumping = True

		if keys[pygame.K_DOWN] and not self.jumping:
			self.crouching = True
			self.w = 50
			self.h = 25
			self.y = sh - 125
		elif not self.jumping:
			self.crouching = False
			self.y = sh - 150
			self.w = 35
			self.h = 50

		if self.jumping:
			if self.jump_inc <= 20:
				self.y -= (10 - self.jump_inc)*2
				self.jump_inc += 1
			else:
				self.jump_inc = 0
				self.jumping = False
			



class Cactus(object):
	def __init__(self):
		self.image = pygame.image.load("cactus.png")
		if random.randint(1,2) == 1:
			self.w = 25
			self.h = 50
			self.big = True
		else:
			self.w = 48
			self.h = 25
			self.big = False
			self.image = pygame.transform.scale(self.image, (12, self.h))

		self.y = (sh-100) - self.h
		self.x = sl

	def draw(self):
		#pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.w, self.h))
		#pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.w, self.h), 1)

		if self.big:
			win.blit(self.image, (self.x, self.y))
		else:
			win.blit(self.image, (self.x, self.y))
			win.blit(self.image, (self.x+12, self.y))
			win.blit(self.image, (self.x+24, self.y))
			win.blit(self.image, (self.x+36, self.y))


	def hit(self):
		if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
			return True
		return False



class Bird(object):
	def __init__(self):
		self.w = 50
		self.h = 25
		self.y = (sh - 100) - (self.h + 10) * random.randint(1,3)
		self.x = sl
		self.flying = [pygame.image.load("bird1.png"), pygame.image.load("bird2.png")]
		self.fly_inc = 0

	def draw(self):
		#pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.w, self.h))
		#pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.w, self.h), 1)
		win.blit(self.flying[self.fly_inc//10], (self.x, self.y))

		if self.fly_inc == 19:
			self.fly_inc = -1
		self.fly_inc += 1


	def hit(self):
		if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x, player.y, player.w, player.h)):
			return True
		return False 
			

player = Dinosaur()


enemies = []
inc = 0
game_speed = 1
score = 0
score_inc = 0


#MAINLOOP
run = True
end = True
while run:
	win.fill((255,255,255))
	pygame.draw.rect(win, (0,0,0), (0, sh-100, sl, 100))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end = False
			run = False

	inc += 1 * game_speed
	if inc >= 100:
		if random.randint(1,2) == 1 and score >= 100:
			enemies.append(Bird())
		else:
			enemies.append(Cactus())
		game_speed += 0.1
		inc = 0
	

	if score_inc <= 5:
		score_inc += 1 * game_speed
	else:
		score_inc = 0
		score += 1

	for enemy in enemies:
		enemy.x -= 5 * game_speed
		enemy.draw()
		if enemy.hit():
			run = False
		if enemy.x + enemy.w == 0:
			enemies.remove(enemy)

	player.draw()
	player.move()


	font = pygame.font.SysFont('comicsans', 50)
	text = font.render(str(score), 1, (0,0,0))
	win.blit(text,(sl - text.get_width() - 10, 10))


	pygame.display.update()
	clock.tick(30)


while end:
	win.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end = False


	font = pygame.font.SysFont('comicsans', 50)
	final_score = font.render("Your score: " + str(score), 1, (255,255,255))
	exit_game = font.render("Click anywhere to exit", 1, (255,255,255))
	win.blit(final_score, (sl/2 - final_score.get_width()/2, sh/4))
	win.blit(exit_game, (sl/2 - exit_game.get_width()/2, sh* 2/3))


	if pygame.mouse.get_pressed()[0]:
		end = False

	pygame.display.update()
