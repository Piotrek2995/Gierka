import pygame
from settings import *
import random

# Vector shortcut
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # wrap around the screen? No, we want to go right.
        # But if we fall off bottom, game over (handled in game loop)

        self.rect.midbottom = self.pos


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_time = pygame.time.get_ticks()
        self.dropped_time = 0 # Amount of time spent frozen (not aging)
        self.lifetime = 200000 # Default huge lifetime (forever)
        
    def update(self):
        # Calculate age
        if self.game.powerup_active:
             self.spawn_time += (pygame.time.get_ticks() - (self.spawn_time + self.dropped_time)) - (pygame.time.get_ticks() - self.spawn_time - 16) # Simple hack to pause age: offset spawn time forward?
             # Better way: just shift spawn_time forward by the delta time of this frame?
             pass 
             
        # Actually simplest way to "Freeze" age is to increment spawn_time by the frame duration, effectively keeping (now - spawn) constant.
        # But we don't have dt here easily.
        # Alternative: Game loop sets a flag. If flag is True, we shift spawn_time.
        
        if self.game.powerup_active:
            # We are frozen. Shift spawn_time forward so 'age' doesn't increase.
            # FPS is 60, so each frame is approx 16ms. Random glitches might occur but it's fine.
            self.spawn_time += 1000 / FPS 
            
        now = pygame.time.get_ticks()
        age = now - self.spawn_time
        
        # If lifetime is set to something reasonable (less than 100 seconds)
        if self.lifetime < 100000:
            pct_left = 1 - (age / self.lifetime)
            if pct_left <= 0:
                self.kill()
            else:
                # Fade from Green to Red
                # Green is (0, 255, 0), Red is (255, 0, 0)
                red = 255 * (1 - pct_left)
                green = 255 * pct_left
                try:
                    self.image.fill((int(red), int(green), 0))
                except ValueError:
                    pass # prevent potential color errors


class Trampoline(pygame.sprite.Sprite):
    def __init__(self, platform):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = platform.rect.centerx
        self.rect.bottom = platform.rect.top - 1
        self.platform = platform

    def update(self):
        self.rect.bottom = self.platform.rect.top - 1
        self.rect.centerx = self.platform.rect.centerx
        if not self.platform.alive():
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, platform):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = platform.rect.centerx
        self.rect.bottom = platform.rect.top - 1
        self.platform = platform


    def update(self):
        self.rect.bottom = self.platform.rect.top - 1
        self.rect.centerx = self.platform.rect.centerx
        if not self.platform.alive():
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, platform):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = platform.rect.centerx
        self.rect.bottom = platform.rect.top - 5
        self.platform = platform

    def update(self):
        self.rect.bottom = self.platform.rect.top - 5
        self.rect.centerx = self.platform.rect.centerx
        if not self.platform.alive():
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self, platform):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 255, 255)) # Cyan
        self.rect = self.image.get_rect()
        self.rect.centerx = platform.rect.centerx
        self.rect.bottom = platform.rect.top - 5
        self.platform = platform

    def update(self):
        self.rect.bottom = self.platform.rect.top - 5
        self.rect.centerx = self.platform.rect.centerx
        if not self.platform.alive():
            self.kill()

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.image = self.font.render(text, True, YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = -3
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.vel_y
        if pygame.time.get_ticks() - self.spawn_time > 1000:
            self.kill()

