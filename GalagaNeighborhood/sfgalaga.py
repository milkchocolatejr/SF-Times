import math
import random
import sys, pygame, time, json

import asyncio
from copy import copy

from pygame.examples import aliens
from pygame.locals import *
from GalagaNeighborhood.Constants import *

settings = json.loads(open('settings.json').read())

pygame.init()

if (not pygame.get_init()):
	sys.exit()

FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = START_SCREEN_WIDTH
SCREEN_HEIGHT = START_SCREEN_HEIGHT
SPEED = 5
SCORE = 0
FPS = TARGET_FPS
inputCooldown = False

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("SFGalaga")

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("""Oh No!""", True, BLACK)
you_win = font.render("Neighborhood Insured!", True, BLACK)

background = pygame.image.load("images/background.png")


class Alien(pygame.sprite.Sprite):
	def __init__(self, image, disaster, scale, damage, minspeed, maxspeed, atkChance, atkBurst, atkWait, atkRounds):
		super().__init__()
		self.image = pygame.transform.scale_by(pygame.image.load(image), scale)
		self.scale = scale
		self.disaster = disaster
		self.rect = self.image.get_rect()
		self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), self.image.get_height() / 2)
		self.minSpeed = minspeed
		self.maxSpeed = maxspeed
		self.damage = damage
		self.currentSpeed = self.minSpeed
		self.atkChance = atkChance
		self.atkBurst = int(atkBurst)
		self.atkWait = atkWait
		self.atkRounds = atkRounds

	def move(self):
		global SCORE

		movex = self.currentSpeed
		movey = 0

		if random.randint(0, 1000) <= self.atkChance * 1000:
			asyncio.run(self.causeDisaster(self.atkRounds))

		if (self.rect.left <= 0):
			self.currentSpeed = random.randint(5, 10)
			movex = abs(movex)
			movey = 2
			SCORE += 1
		if (self.rect.right >= SCREEN_WIDTH):
			self.currentSpeed = -random.randint(5, 10)
			movex = -abs(movex)
			movey = 2
			SCORE += 1

		self.rect.move_ip(movex, movey)

	async def causeDisaster(self, x):
		i = 0
		while i < self.atkBurst:
			disaster = Disaster(self.disaster, self.rect.center, self.scale, self.damage)
			all_sprites.add(disaster)
			disasters.add(disaster)
			i = i + 1

		x = x - 1
		if x > 0:
			await asyncio.sleep(self.atkWait)
			asyncio.run(self.causeDisaster(x))

class Disaster(pygame.sprite.Sprite):
	def __init__(self, image, center, scale, damage):
		super().__init__()
		self.image = pygame.transform.scale_by(pygame.image.load(image), scale)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.damage = damage

	def move(self):
		self.rect.move_ip(0, 5)
		if self.rect.bottom >= SCREEN_HEIGHT:
			self.kill()

class InsurencePolicy(pygame.sprite.Sprite):
	def __init__(self, image, scale, type, health, direction):
		super().__init__()
		self.image = pygame.transform.scale_by(pygame.image.load(image + "_" + type + ".png"), scale)
		self.rect = self.image.get_rect()
		self.health = health
		tmp = math.sqrt(direction[0] * direction[0] + direction[1] * direction[1])
		self.direction = (direction[0] / tmp, -direction[1] / tmp)
		self.isRegistered = False

	def registerPolicy(self, object):
		if not self.isRegistered:
			self.isRegistered = True
			self.rect.center = (object.rect.center[0], object.rect.top - 5)
			self.rect.width = object.rect.width
			self.direction = (0, 0)
			print(self.health)

	def defendNeighbor(self, damage):
		print(self.health)
		self.health -= damage
		if self.health <= 0:
			self.kill()

	def move(self):
		self.rect.move_ip(self.direction[0] * SPEED, self.direction[1] * SPEED)

class PolicyHolder(pygame.sprite.Sprite):
	def __init__(self, image, scale, health, type):
		super().__init__()
		self.image = pygame.transform.scale_by(pygame.image.load(image), scale)
		self.rect = self.image.get_rect()
		self.health = health
		self.type = type

	def setX(self, x):
		self.rect.center = (x, SCREEN_HEIGHT - (self.rect.height / 2))

	def disasterStruck(self, damage):
		self.health -= damage
		if self.health <= 0:
			self.kill()

	def move(self):
		# nah, I'd
		pass


# def draw(self, surface):
# 	if drawColliders:
# 		surface.blit((pygame.Surface(self.rect).fill(GREEN)), self.rect)


class Player(pygame.sprite.Sprite):
	def __init__(self, image, policyPNGs, claimsPNGs, scale, speed):
		super().__init__()
		self.image = pygame.transform.scale_by(pygame.image.load(image), scale)
		self.rect = self.image.get_rect()
		self.scale = scale
		self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - (self.rect.height / 2))
		self.speed = speed
		self.policyPNGs = policyPNGs
		# self.claimsPNGs = claimsPNGs
		self.inventory = { "Home": 0, "Auto": 0 }
		self.currentPolicy = "Home"

	def move(self):
		pressed_keys = pygame.key.get_pressed()
		# if pressed_keys[K_UP]:
		# self.rect.move_ip(0, -5)
		# if pressed_keys[K_DOWN]:
		# self.rect.move_ip(0,5)

		if self.rect.left > 0:
			if pressed_keys[K_LEFT] or pressed_keys[K_a]:
				self.rect.move_ip(-self.speed, 0)
		if self.rect.right < START_SCREEN_WIDTH:
			if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
				self.rect.move_ip(self.speed, 0)

		if pressed_keys[K_SPACE] or pygame.mouse.get_pressed()[0] == True:
			asyncio.run(self.promotePolicy())

	async def promotePolicy(self):
		if (self.inventory[self.currentPolicy] > 0):
			self.inventory[self.currentPolicy] -= 1
			mx, my = pygame.mouse.get_pos()
			player_rect = self.rect
			dx, dy = mx - player_rect.centerx, player_rect.centery - my
			angle = math.degrees(math.atan2(-dy, dx))
			rot_image = pygame.transform.rotate(self.image, angle)
			rot_image_rect = rot_image.get_rect(center=player_rect.center)
			policy = InsurencePolicy(self.policyPNGs, .2, self.currentPolicy, 10, (dx, dy))
			policy.rect.center = self.rect.center
			all_sprites.add(policy)
			policies.add(policy)


# def draw(self, surface):
# 	if drawColliders:
# 		surface.blit((pygame.Surface(self.rect).fill(GREEN)), self.rect)

Players = []
Aliens = []
PolicyHolders = []

for item in settings["players"]:
	key = list(item.keys())[0]
	player = Player("images/" + key, "images/" + item[key][0], "images/" + item[key][1],
	            float(item[key][2]), float(item[key][3]))
	Players.append(player)

for item in settings["aliens"]:
	key = list(item.keys())[0]
	alien = Alien("images/" + key, "images/" + item[key][0], float(item[key][1]),
	        float(item[key][2]), float(item[key][3]), float(item[key][4]),
	        float(item[key][5]), float(item[key][6]), int(item[key][7]),
	        float(item[key][8]))
	Aliens.append(alien)

for item in settings["policyHolders"]:
	key = list(item.keys())[0]
	policyHolder = PolicyHolder("images/" + key, float(item[key][0]),
	                int(item[key][1]), item[key][2])
	x = random.randint(10, SCREEN_WIDTH - 10)
	policyHolder.setX(x)
	while PolicyHolders and pygame.sprite.spritecollideany(policyHolder, PolicyHolders):
		x = random.randint(10, SCREEN_WIDTH - 10)
		policyHolder.setX(x)
	PolicyHolders.append(policyHolder)

#Creating Sprites Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
policyHolders = pygame.sprite.Group()
for p in PolicyHolders:
	all_sprites.add(p)
	policyHolders.add(p)
for e in Aliens:
	enemies.add(e)
	all_sprites.add(e)
players = pygame.sprite.Group()
for p in Players:
	players.add(p)
	all_sprites.add(p)
disasters = pygame.sprite.Group()
policies = pygame.sprite.Group()

#Adding a new User event
INC_DIFF = pygame.USEREVENT + 1
pygame.time.set_timer(INC_DIFF, 10500)
HOME_ADD = pygame.USEREVENT + 2
pygame.time.set_timer(HOME_ADD, 1500)
INPUT_COOLDOWN = pygame.USEREVENT + 3
pygame.time.set_timer(INPUT_COOLDOWN, 500)


running = True

while running:
	for event in pygame.event.get():
		if event.type == INC_DIFF:
			# Aliens.append(copy(Aliens[0]))
			# all_sprites.add(Aliens[len(Aliens) - 1])
			pass
		if event.type == HOME_ADD:
			for player in players:
				player.inventory["Home"] += 1
		if event.type == INPUT_COOLDOWN:
			inputCooldown = False
		if event.type == pygame.QUIT:
			running = False

	DISPLAYSURF.fill(WHITE)
	DISPLAYSURF.blit(background, (0, SCREEN_HEIGHT - background.get_height()))

	# Moves and Re-draws all Sprites
	for entity in all_sprites:
		DISPLAYSURF.blit(entity.image, entity.rect)
		entity.move()

	scores = font_small.render(str(SCORE), True, BLACK)
	DISPLAYSURF.blit(scores, (10, 10))

	# To be run if collision occurs between Player and Enemy
	for player in players:
		if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, disasters):
			# pygame.mixer.Sound('crash.wav').play()
			time.sleep(0.5)

			DISPLAYSURF.fill(RED)
			DISPLAYSURF.blit(game_over, (50, 250))

			pygame.display.update()
			for entity in all_sprites:
				entity.kill()
			time.sleep(2)
			running = False

	for holder in policyHolders:
		col = pygame.sprite.spritecollideany(holder, disasters)
		if col:
			col.kill()
			holder.disasterStruck(col.damage)
		col = pygame.sprite.spritecollideany(holder, enemies)
		if col:
			col.kill()
			holder.kill()
		col = pygame.sprite.spritecollideany(holder, policies)
		if col:
			col.registerPolicy(holder)

	for policy in policies:
		col = pygame.sprite.spritecollideany(policy, disasters)
		if col:
			col.kill()
			policy.defendNeighbor(col.damage)
		col = pygame.sprite.spritecollideany(policy, enemies)
		if col:
			col.kill()
			policy.kill()
		col = pygame.sprite.spritecollideany(policy, policyHolders)
		if col:
			policy.registerPolicy(col)

	if (len(policyHolders) <= 0):
		time.sleep(0.5)

		DISPLAYSURF.fill(RED)
		DISPLAYSURF.blit(game_over, (30, 250))

		pygame.display.update()
		for entity in all_sprites:
			entity.kill()
		time.sleep(2)
		running = False

	if (len(enemies) <= 0):
		time.sleep(0.5)

		DISPLAYSURF.fill(RED)
		DISPLAYSURF.blit(you_win, (50, 250))

		pygame.display.update()
		for entity in all_sprites:
			entity.kill()
		time.sleep(2)
		running = False

	pygame.display.update()
	FramePerSec.tick(FPS)

pygame.quit()
