import pygame
from settings import *

# Vector shortcut
vec = pygame.math.Vector2

# --- Helper functions to draw nicer sprites ---

def create_player_image_idle(width=32, height=48):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Colors
    skin = (245, 222, 179)
    shirt = (30, 144, 255)
    pants = (25, 25, 112)
    shoes = (60, 60, 60)
    outline = (20, 20, 20)
    # Head
    head_rect = pygame.Rect(10, 2, 12, 12)
    pygame.draw.ellipse(surf, skin, head_rect)
    pygame.draw.ellipse(surf, outline, head_rect, 1)
    # Eyes
    pygame.draw.circle(surf, (0, 0, 0), (16, 7), 1)
    pygame.draw.circle(surf, (0, 0, 0), (20, 7), 1)
    # Body
    body_rect = pygame.Rect(8, 14, 16, 16)
    pygame.draw.rect(surf, shirt, body_rect, border_radius=4)
    pygame.draw.rect(surf, outline, body_rect, 1, border_radius=4)
    # Arms
    pygame.draw.line(surf, skin, (8, 18), (2, 22), 3)
    pygame.draw.line(surf, skin, (24, 18), (30, 22), 3)
    # Legs
    left_leg = pygame.Rect(10, 30, 6, 12)
    right_leg = pygame.Rect(16, 30, 6, 12)
    pygame.draw.rect(surf, pants, left_leg, border_radius=2)
    pygame.draw.rect(surf, pants, right_leg, border_radius=2)
    pygame.draw.rect(surf, outline, left_leg, 1, border_radius=2)
    pygame.draw.rect(surf, outline, right_leg, 1, border_radius=2)
    # Shoes
    pygame.draw.rect(surf, shoes, pygame.Rect(10, 40, 6, 4), border_radius=2)
    pygame.draw.rect(surf, shoes, pygame.Rect(16, 40, 6, 4), border_radius=2)
    return surf.convert_alpha()


def create_player_image_run(width=32, height=48):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Colors
    skin = (245, 222, 179)
    shirt = (30, 144, 255)
    pants = (25, 25, 112)
    shoes = (60, 60, 60)
    outline = (20, 20, 20)
    # Head
    head_rect = pygame.Rect(10, 2, 12, 12)
    pygame.draw.ellipse(surf, skin, head_rect)
    pygame.draw.ellipse(surf, outline, head_rect, 1)
    # Eyes
    pygame.draw.circle(surf, (0, 0, 0), (16, 7), 1)
    pygame.draw.circle(surf, (0, 0, 0), (20, 7), 1)
    # Body
    body_rect = pygame.Rect(8, 14, 16, 16)
    pygame.draw.rect(surf, shirt, body_rect, border_radius=4)
    pygame.draw.rect(surf, outline, body_rect, 1, border_radius=4)
    # Arms swung
    pygame.draw.line(surf, skin, (8, 18), (0, 16), 3)
    pygame.draw.line(surf, skin, (24, 18), (32, 20), 3)
    # Legs in stride
    left_leg = pygame.Rect(8, 32, 6, 12)
    right_leg = pygame.Rect(18, 28, 6, 12)
    pygame.draw.rect(surf, pants, left_leg, border_radius=2)
    pygame.draw.rect(surf, pants, right_leg, border_radius=2)
    pygame.draw.rect(surf, outline, left_leg, 1, border_radius=2)
    pygame.draw.rect(surf, outline, right_leg, 1, border_radius=2)
    # Shoes
    pygame.draw.rect(surf, shoes, pygame.Rect(8, 42, 6, 4), border_radius=2)
    pygame.draw.rect(surf, shoes, pygame.Rect(18, 40, 6, 4), border_radius=2)
    return surf.convert_alpha()


def create_trampoline_image(width=36, height=14):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Base
    pygame.draw.rect(surf, (30, 30, 30), pygame.Rect(0, height-4, width, 4), border_radius=2)
    # Springs
    for i in range(3):
        x = 4 + i * (width // 3)
        pygame.draw.line(surf, (180, 180, 255), (x, height-4), (x+8, 4), 3)
        pygame.draw.line(surf, (120, 120, 220), (x+8, 4), (x+14, height-4), 3)
    # Top pad
    pygame.draw.rect(surf, BLUE, pygame.Rect(2, 0, width-4, 6), border_radius=3)
    pygame.draw.rect(surf, (10, 50, 160), pygame.Rect(2, 0, width-4, 6), 1, border_radius=3)
    return surf.convert_alpha()


def create_obstacle_image(width=24, height=24):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Spike triangle
    points = [(0, height), (width//2, 0), (width, height)]
    pygame.draw.polygon(surf, RED, points)
    pygame.draw.polygon(surf, (120, 0, 0), points, 2)
    # Shine
    pygame.draw.line(surf, (255, 150, 150), (width//2, 4), (width//2+4, 8), 2)
    return surf.convert_alpha()


def create_coin_image(diameter=18):
    surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    center = (diameter//2, diameter//2)
    pygame.draw.circle(surf, (255, 215, 0), center, diameter//2)
    pygame.draw.circle(surf, (180, 140, 0), center, diameter//2, 2)
    # Highlight
    pygame.draw.arc(surf, (255, 255, 255), pygame.Rect(3, 3, diameter-6, diameter-6), 0.2, 1.0, 2)
    # Inner symbol
    pygame.draw.circle(surf, (240, 180, 0), center, diameter//3, 2)
    return surf.convert_alpha()


def create_powerup_image(size=18):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Star-like spark
    cx, cy = size//2, size//2
    color = (0, 255, 255)
    pygame.draw.line(surf, color, (cx, 0), (cx, size), 2)
    pygame.draw.line(surf, color, (0, cy), (size, cy), 2)
    pygame.draw.line(surf, color, (2, 2), (size-2, size-2), 2)
    pygame.draw.line(surf, color, (size-2, 2), (2, size-2), 2)
    pygame.draw.circle(surf, (180, 255, 255), (cx, cy), 4)
    return surf.convert_alpha()


def draw_shadow_under(surface, width, height, opacity=80):
    # Dodaje prostokątną elipsę jako cień przy spodzie
    shadow = pygame.Surface((width, height//4), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, opacity), shadow.get_rect())
    surface.blit(shadow, (0, height - height//6))


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Anim frames
        self.image_idle = create_player_image_idle()
        self.image_run = create_player_image_run()
        self.image = self.image_idle.copy()
        # add small shadow baked into image
        draw_shadow_under(self.image, self.image.get_width(), self.image.get_height(), opacity=60)
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.anim_timer = 0
        self.anim_interval = 120 # ms per frame when running
        self.anim_toggle = False

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
        
        # Animacja: gdy poruszamy się poziomo, przełączaj klatki run; w przeciwnym razie idle
        now = pygame.time.get_ticks()
        moving_horiz = abs(self.vel.x) > 0.2
        if moving_horiz:
            if now - self.anim_timer > self.anim_interval:
                self.anim_timer = now
                self.anim_toggle = not self.anim_toggle
            # toggle między dwiema klatkami biegu i idla dla efektu
            frame = self.image_run if self.anim_toggle else self.image_idle
        else:
            frame = self.image_idle
        # Odśwież obrazek (i cień)
        self.image = frame.copy()
        draw_shadow_under(self.image, self.image.get_width(), self.image.get_height(), opacity=60)

        self.rect.midbottom = self.pos


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        # Draw a nicer platform with slight gradient and rounded corners
        base = pygame.Rect(0, 0, w, h)
        pygame.draw.rect(self.image, (30, 120, 30), base, border_radius=6)
        pygame.draw.rect(self.image, (20, 80, 20), base, 2, border_radius=6)
        pygame.draw.rect(self.image, (60, 180, 60), pygame.Rect(2, 2, w-4, max(2, h//4)), border_radius=4)
        # cień pod platformą (sprawia wrażenie wysokości)
        shadow_h = max(4, h//3)
        shadow = pygame.Surface((w, shadow_h), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), pygame.Rect(0, 0, w, shadow_h))
        # blitujemy cień lekko poniżej podstawy
        self.image.blit(shadow, (0, h - shadow_h//2))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_time = pygame.time.get_ticks()
        # Accumulated time while frozen (powerup active)
        self.frozen_time_acc = 0
        self.last_update_ticks = pygame.time.get_ticks()
        self.lifetime = 200000 # Default huge lifetime (forever)
        
    def update(self):
        now = pygame.time.get_ticks()
        dt = now - self.last_update_ticks
        self.last_update_ticks = now

        # During active powerup, accumulate freeze time so age doesn't grow
        if getattr(self.game, 'powerup_active', False):
            self.frozen_time_acc += dt

        # Effective age ignores frozen periods
        age = now - self.spawn_time - self.frozen_time_acc

        # If lifetime is set to something reasonable (less than 100 seconds)
        if self.lifetime < 100000:
            pct_left = 1 - (age / self.lifetime)
            if pct_left <= 0:
                self.kill()
            else:
                # Fade from Green to Red
                red = max(0, min(255, int(255 * (1 - pct_left))))
                green = max(0, min(255, int(255 * pct_left)))
                # Re-draw base with color shift
                self.image.fill((0, 0, 0, 0))
                base = pygame.Rect(0, 0, self.rect.width, self.rect.height)
                pygame.draw.rect(self.image, (red, green, 0), base, border_radius=6)
                pygame.draw.rect(self.image, (max(0, red-50), max(0, green-50), 0), base, 2, border_radius=6)
                pygame.draw.rect(self.image, (min(255, red+30), min(255, green+30), 30), pygame.Rect(2, 2, self.rect.width-4, max(2, self.rect.height//4)), border_radius=4)
                # odtwórz cień
                w, h = self.rect.width, self.rect.height
                shadow_h = max(4, h//3)
                shadow = pygame.Surface((w, shadow_h), pygame.SRCALPHA)
                pygame.draw.ellipse(shadow, (0, 0, 0, 60), pygame.Rect(0, 0, w, shadow_h))
                self.image.blit(shadow, (0, h - shadow_h//2))


class Trampoline(pygame.sprite.Sprite):
    def __init__(self, platform):
        pygame.sprite.Sprite.__init__(self)
        # ...existing code...
        surf = pygame.Surface((36, 14), pygame.SRCALPHA)
        pygame.draw.rect(surf, (30, 30, 30), pygame.Rect(0, 10, 36, 4), border_radius=2)
        for i in range(3):
            x = 4 + i * (36 // 3)
            pygame.draw.line(surf, (180, 180, 255), (x, 10), (x+8, 2), 3)
            pygame.draw.line(surf, (120, 120, 220), (x+8, 2), (x+14, 10), 3)
        pygame.draw.rect(surf, BLUE, pygame.Rect(2, 0, 32, 6), border_radius=3)
        pygame.draw.rect(surf, (10, 50, 160), pygame.Rect(2, 0, 32, 6), 1, border_radius=3)
        self.image = surf.convert_alpha()
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
        # ...existing code...
        surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        points = [(0, 24), (12, 0), (24, 24)]
        pygame.draw.polygon(surf, RED, points)
        pygame.draw.polygon(surf, (120, 0, 0), points, 2)
        pygame.draw.line(surf, (255, 150, 150), (12, 4), (16, 8), 2)
        self.image = surf.convert_alpha()
        # Shrink hitbox a bit to be fair
        self.rect = self.image.get_rect().inflate(-6, -6)
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
        # ...existing code...
        diameter = 18
        surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (diameter//2, diameter//2)
        pygame.draw.circle(surf, (255, 215, 0), center, diameter//2)
        pygame.draw.circle(surf, (180, 140, 0), center, diameter//2, 2)
        pygame.draw.arc(surf, (255, 255, 255), pygame.Rect(3, 3, diameter-6, diameter-6), 0.2, 1.0, 2)
        pygame.draw.circle(surf, (240, 180, 0), center, diameter//3, 2)
        self.image = surf.convert_alpha()
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
        # ...existing code...
        size = 18
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size//2, size//2
        color = (0, 255, 255)
        pygame.draw.line(surf, color, (cx, 0), (cx, size), 2)
        pygame.draw.line(surf, color, (0, cy), (size, cy), 2)
        pygame.draw.line(surf, color, (2, 2), (size-2, size-2), 2)
        pygame.draw.line(surf, color, (size-2, 2), (2, size-2), 2)
        pygame.draw.circle(surf, (180, 255, 255), (cx, cy), 4)
        self.image = surf.convert_alpha()
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
