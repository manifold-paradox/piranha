import pygame
import os
import random

pygame.init()

# Setup
pygame.font.init()
score = 0
WIDTH, HEIGHT = 1200, 950
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Eater")

# Load Images
player_img = pygame.image.load(os.path.join("assets/fish_eater", "Player_fish.png"))
blue_fish = pygame.image.load(os.path.join("assets/fish_eater", "blue_fish.svg"))
yellow_fish = pygame.image.load(os.path.join("assets/fish_eater", "yellow_fish.svg"))
green_fish = pygame.image.load(os.path.join("assets/fish_eater", "green_fish.svg"))

# Maintain ratio from original image
player_img_w = player_img.get_rect().width
player_img_h = player_img.get_rect().height

# Scale Images
player_img = pygame.transform.scale(player_img, (player_img_w * 0.1, player_img_h * 0.1))
blue_fish = pygame.transform.scale(blue_fish, (25, 25))
yellow_fish = pygame.transform.scale(yellow_fish, (100, 75))
green_fish = pygame.transform.scale(green_fish, (200, 200))


# Background
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets/fish_eater", "underwater.png")), (WIDTH, HEIGHT))

# Fonts / Messages
small_font = pygame.font.SysFont('Corbel', 35)
game_over_msg = small_font.render("Game Over", True, "red")
game_over_msg_2 = small_font.render("Click to play again", True, "red")


# Classes
class Fish:

   def __init__(self, x, y):
       self.x = x
       self.y = y
       self.fish_img = None

   def draw(self, window):
       window.blit(self.fish_img, (self.x, self.y))

   def get_width(self):
       return self.fish_img.get_width()

   def get_height(self):
       return self.fish_img.get_height()


class Player(Fish):
   def __init__(self, x, y, width, height):
       super().__init__(x, y)
       self.fish_img = player_img
       self.height = height
       self.width = width
       self.mask = pygame.mask.from_surface(self.fish_img)

   def increase_size(self, width, height):
       self.width += width * player_img_w
       self.height += height * player_img_h
       self.fish_img = pygame.transform.scale(player_img, (self.width, self.height))
       self.mask = pygame.mask.from_surface(self.fish_img)

   def decrease_size(self, width, height):
       self.width -= width * player_img_w
       self.height -= height * player_img_h
       self.fish_img = pygame.transform.scale(player_img, (self.width, self.height))
       self.mask = pygame.mask.from_surface(self.fish_img)


class Enemy_Fish(Fish):
   IMAGE_MAP = [yellow_fish, green_fish, blue_fish]

   def __init__(self, x, y, img):
       super().__init__(x, y)
       self.fish_img = self.IMAGE_MAP[img]
       self.mask = pygame.mask.from_surface(self.fish_img)

   def move(self, vel):
       self.x += vel


def collide(obj1, obj2):
   offset_x = obj2.x - obj1.x
   offset_y = obj2.y - obj1.y
   return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


# Declaration
running = True
lost = False
FPS = 60
clock = pygame.time.Clock()
player_size_w = player_img_w * 0.1
player_size_h = player_img_h * 0.1
player = Player(300, 630, player_size_w, player_size_h)
player_speed = 5
enemies = []
wave_length = 3
enemy_start_pos = [0, WIDTH]

#Player Start Position
player.x = WIDTH / 2
player.y = HEIGHT / 2


def redraw_window():
   global lost
   # Add background image
   screen.blit(bg, (0, 0))
   # Draw enemies
   for enemy in enemies:
       enemy.draw(screen)
   # Place ship on screen
   player.draw(screen)

   # Check for game over
   if lost:
       screen.fill((0, 0, 0))
       screen.blit(game_over_msg, (WIDTH / 2, HEIGHT / 2)   )
       screen.blit(game_over_msg_2, (WIDTH / 2, HEIGHT / 4))
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               quit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               lost = False
   # Update screen
   pygame.display.update()


# Game Loop
while running:
   clock.tick(FPS)
   redraw_window()
   if len(enemies) == 0:
       # Spawn enemies
       for i in range(wave_length):
           enemy = Enemy_Fish(0, random.randrange(0, HEIGHT - 100), random.randint(0, 2))
           enemies.append(enemy)
   # Check for window close
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           quit()
   # Player Controls
   keys = pygame.key.get_pressed()
   if keys[pygame.K_RIGHT] and player.get_width() + player.x < WIDTH:
       player.x += player_speed
       player.fish_img = player_img
   if keys[pygame.K_LEFT] and player.x - player_speed >= 0:
       player.x -= player_speed
       player.fish_img = pygame.transform.flip(player_img, True, False)
   if keys[pygame.K_UP] and player.y - player_speed >= 0:
       player.y -= player_speed
   if keys[pygame.K_DOWN] and player.y + player.get_height() < HEIGHT:
       player.y += player_speed

   # Move enemies
   for enemy in enemies[:]:
       enemy.move(random.randint(2, 10))
       # Remove enemies from screen / wave
       if collide(enemy, player):
           # Check if fish is bigger than enemy fish
           if player.get_width() > enemy.get_width():
               # Prevent player from getting too large
               if player.get_width() < 400:
                   # Increase player size
                   player.increase_size(0.1, 0.1)
                   # Update image
                   player_img = player.fish_img
               enemies.remove(enemy)
           # Enemy fish is larger than player
           else:
               if player.fish_img.get_width() > (player_img_w * 0.1):
                   # Decrease player size
                   player.decrease_size(0.1, 0.1)
                   # Update image
                   player_img = player.fish_img
                   enemies.remove(enemy)
               else:
                   # Game Over
                   lost = True
       if enemy.x + enemy.get_height() > WIDTH:
           enemies.remove(enemy)


