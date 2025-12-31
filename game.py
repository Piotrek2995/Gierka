import pygame
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font('arial')

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.trampolines = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.powerup_active = False
        self.powerup_start = 0
        self.powerup_duration = 5000 # 5 seconds
        
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        # Initial Platforms
        # We will need a way to generate infinite platforms to the right/up
        for plat in PLATFORM_LIST:
             p = Platform(self, *plat, 100, 20) # *plat explodes the tuple into arguments, plus width and height
             self.all_sprites.add(p)
             self.platforms.add(p)
             
        # Add a big ground platform for start
        p = Platform(self, 0, HEIGHT - 40, WIDTH * 2, 40)
        self.all_sprites.add(p)
        self.platforms.add(p)
        
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        # Powerup Logic
        if self.powerup_active:
            now = pygame.time.get_ticks()
            if now - self.powerup_start > self.powerup_duration:
                self.powerup_active = False
        
        # Check for trampoline collision first!
        # This allows the bounce to happen before we snap to the platform
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.trampolines, False)
            if hits:
                self.player.vel.y = -PLAYER_JUMP * 1.3 # Boost jump (reduced from 1.5)
                self.player.rect.bottom = hits[0].rect.top - 1 # Ensure we are above it
                # Important: Do NOT check for platform collisions if we hit a trampoline this frame
                return 

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # snap to top of platform
                lowest = hits[0]
                for hit in hits:
                     if hit.rect.bottom > lowest.rect.bottom:
                         lowest = hit
                
                # prevent falling through if slightly inside
                # Fix: Allow for high velocity penetration (tunneling fix) by adding a buffer
                if self.player.pos.y < lowest.rect.bottom + 50:
                    self.player.pos.y = lowest.rect.top + 1 # +1 to ensure collision detection for jump
                    self.player.vel.y = 0
                    self.player.rect.midbottom = self.player.pos

        # Check for obstacle collision
        hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        if hits:
            self.playing = False 
            
        # Check for coin collision
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        if hits:
             self.score += 100
             for hit in hits:
                 text = FloatingText(hit.rect.centerx, hit.rect.centery, "+100")
                 self.all_sprites.add(text)
             
        # Check for powerup collision
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        if hits:
             self.powerup_active = True
             self.powerup_start = pygame.time.get_ticks()
             # Logic is now handled in Platform.update and Game.update
             # for plat in self.platforms:
             #     plat.lifetime += 3000 # OLD LOGIC REMOVED
                 
        # Check if player fell off screen
        # Relaxed condition: allow falling slightly below checking for bottom platforms
        if self.player.rect.top > HEIGHT + 100:
            self.playing = False

        # Camera scroll (and Score)
        # Move platforms left if player moves right past 1/2 screen
        if self.player.rect.right > WIDTH / 2:
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            scroll = max(abs(self.player.vel.x), 2)
            self.score += int(scroll)
            
            for plat in self.platforms:
                plat.rect.x -= scroll
                if plat.rect.right < 0:
                    plat.kill()
            
            # Scroll items
            for mob in self.obstacles:
                mob.rect.x -= scroll
                if mob.rect.right < 0:
                    mob.kill()
            for tramp in self.trampolines:
                tramp.rect.x -= scroll
                if tramp.rect.right < 0:
                    tramp.kill()
            for coin in self.coins:
                coin.rect.x -= scroll
                if coin.rect.right < 0:
                    coin.kill()
            for pow in self.powerups:
                pow.rect.x -= scroll
                if pow.rect.right < 0:
                    pow.kill()
            
            # Spawn new platforms
            while len(self.platforms) < 6:
                width = random.randrange(50, 100)
                # Find candidates: platforms that are NOT the ground (assume ground is very wide or very low)
                # Ground is at y = HEIGHT - 40 approx.
                candidates = [p for p in self.platforms if p.rect.y < HEIGHT - 60]
                if not candidates:
                    candidates = self.platforms # fallback
                
                # Find the rightmost platform to spawn relative to
                rightmost_plat = max(candidates, key=lambda x: x.rect.right)
                
                new_x = rightmost_plat.rect.right + random.randrange(10, 50)
                new_y = rightmost_plat.rect.y - random.randrange(-20, 100)
                new_y = max(10, min(HEIGHT - 40, new_y)) # Keep in screen bounds for now
                
                p = Platform(self, new_x,
                             new_y,
                             width, 20)
                
                # Enable decay specifically for created platforms?
                # The user said "stare klocki po pewnym czasie sie rozwalają" (old blocks crumble after some time)
                # Let's give them a random lifetime between 3 and 6 seconds?
                # Or just fixed 5 seconds?
                # Progressive difficulty: shorten lifetime based on score
                # Every 1000 points, reduce max lifetime by e.g. 500ms?
                base_lifetime_min = 4000
                base_lifetime_max = 7000
                
                difficulty_reduction = (self.score // 1000) * 500
                # Clamp it so it doesn't become impossible (minimum 1.5 seconds?)
                lifetime_min = max(1500, base_lifetime_min - difficulty_reduction)
                lifetime_max = max(2500, base_lifetime_max - difficulty_reduction)
                
                p.lifetime = random.randrange(lifetime_min, lifetime_max)
                
                self.platforms.add(p)
                self.all_sprites.add(p)
                
                # Chance to spawn items
                if random.randrange(100) < 15 and p.rect.width > 60: # 15% chance for obstacle, only on wider platforms
                    o = Obstacle(p)
                    self.obstacles.add(o)
                    self.all_sprites.add(o)
                elif random.randrange(100) < 10: # 10% chance for trampoline
                    t = Trampoline(p)
                    self.trampolines.add(t)
                    self.all_sprites.add(t)
                elif random.randrange(100) < 10: # 10% chance for Coin (Reduced from 20%)
                    c = Coin(p)
                    self.coins.add(c)
                    self.all_sprites.add(c)
                elif random.randrange(100) < 5: # 5% chance for Powerup (Reduced from 10%)
                    pow = Powerup(p)
                    self.powerups.add(pow)
                    self.all_sprites.add(pow)
                
        # Move platforms down if player moves up past 1/4 screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            scroll_y = max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += scroll_y
                if plat.rect.top >= HEIGHT + 100:
                    plat.kill()
            
            for mob in self.obstacles:
                mob.rect.y += scroll_y
                if mob.rect.top >= HEIGHT + 100:
                    mob.kill()
            for tramp in self.trampolines:
                tramp.rect.y += scroll_y
                if tramp.rect.top >= HEIGHT + 100:
                    tramp.kill()
            
            for coin in self.coins:
                coin.rect.y += scroll_y
                if coin.rect.top >= HEIGHT + 100:
                    coin.kill()
            for pow in self.powerups:
                pow.rect.y += scroll_y
                if pow.rect.top >= HEIGHT + 100:
                    pow.kill()
                    
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        
        if self.powerup_active:
            # Draw Freeze Time Bar
            now = pygame.time.get_ticks()
            time_left = self.powerup_duration - (now - self.powerup_start)
            if time_left < 0: time_left = 0
            
            bar_width = 200
            bar_height = 20
            fill_width = int(bar_width * (time_left / self.powerup_duration))
            
            outline_rect = pygame.Rect(WIDTH / 2 - bar_width / 2, 50, bar_width, bar_height)
            fill_rect = pygame.Rect(WIDTH / 2 - bar_width / 2, 50, fill_width, bar_height)
            
            pygame.draw.rect(self.screen, (0, 255, 255), fill_rect) # Cyan fill
            pygame.draw.rect(self.screen, WHITE, outline_rect, 2) # White outline
        
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
