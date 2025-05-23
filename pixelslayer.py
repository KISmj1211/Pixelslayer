import pygame
import random

# basic settings
pygame.init()

WIDTH, HEIGHT = 500, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Slayer")

# color tools
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ATTACK_COLOR = (255, 100, 100)

# FPS settings
clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.Font(None, 36)

# class for the player
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 40, 40)
        self.speed = 6
        self.attack_range = pygame.Rect(self.rect.x - 30, self.rect.y - 30, 100, 100)
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.attacking = False
        self.attack_timer = 0

    def move(self, dx, dy):
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x + dx *self.speed))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y + dy *self.speed))
        self.attack_range.topleft = (self.rect.x - 30, self.rect.y - 30)
        
    def attack(self, enemies):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = 12 # = 0.2s
            enemies[:] = [enemy for enemy in enemies if not self.attack_range.colliderect(enemy.rect)]
            
            """
            enemies = enemies[:] # copy
            for enemy in enemies:
                if not self.attack_range.colliderect(enemy.rect):
                    enemies.append(enemy) 
            """
    def draw(self):
        pygame.draw.rect(SCREEN, BLUE, self.rect)
        if self.attacking:
            pygame.draw.rect(SCREEN, ATTACK_COLOR, self.attack_range, 2)            
        else:
            pygame.draw.rect(SCREEN, BLACK, self.attack_range, 1)            
        self.draw_lives()
    
    def draw_lives(self):
        for i in range(self.lives):
            pygame.draw.rect(SCREEN, RED, (10 + i * 30, 10, 20, 20))
        
    
    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 60 # 1 second invinciblity
    
    def update(self):
        # if invincible -> infivincible timer-1 -> if invincible timer = 0 Invincibility=False
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        # attacking -> attacking timer -1 -> attacking timer <= 0  attacking timer= False
        if self.attacking: 
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
    
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT- 30), 30, 30)
        self.speed = 1.5

    def move_towards(self, target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed
        
    def draw(self):
        pygame.draw.rect(SCREEN, RED, self.rect)

def spawn_enemies(count):
    return [Enemy() for _ in range(count)]
# lst = []
# for _ in range(count):
#     lst.append(Enemy())
# return lst

def main():
    run = True
    player  = Player()
    stage = 1
    enemies = spawn_enemies(stage * 3)
    
    while run:
        clock.tick(FPS)
        SCREEN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0,0 
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
            
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        player.move(dx, dy)
        
        
        # enemies attacked
        if keys[pygame.K_SPACE]:
            player.attack(enemies)        
        
        # enemies movement
        for enemy in enemies:
            enemy.move_towards(player)

        # colliding system
        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                player.take_damage()
                enemies.remove(enemy)
                
        player.update()

        # checking game over
        if player.lives <= 0:
            print("Game Over!")
            pygame.time.delay(2000)
            run = False

        # stage upgrading
        if not enemies:
            if stage >= 5:  # if all stages end = win
                print("You Win!")
                pygame.time.delay(2000)
                run = False
            else:
                stage += 1
                enemies = spawn_enemies(stage * 3)
                print(f"Stage {stage}!")

        # randering
        player.draw()
        for enemy in enemies:
            enemy.draw()

        # stage showing
        stage_text = FONT.render(f"Stage {stage}", True, BLACK)
        SCREEN.blit(stage_text, (WIDTH // 2 - 50, 10))
        
        pygame.display.update()

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()