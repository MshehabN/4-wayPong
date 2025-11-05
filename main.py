import pygame
import sys
import math

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BALL_SIZE = 15
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_SPEED = 5
FPS = 60
LIVES_PER_PLAYER = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
RED = (255, 100, 100)

class Paddle:
    def __init__(self, x, y, width, height, is_horizontal=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_horizontal = is_horizontal
        self.speed = PADDLE_SPEED
        
    def move_left(self):
        if self.is_horizontal:
            self.x = max(0, self.x - self.speed)
        else:
            self.y = max(0, self.y - self.speed)
    
    def move_right(self):
        if self.is_horizontal:
            self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)
        else:
            self.y = min(WINDOW_HEIGHT - self.height, self.y + self.speed)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.get_rect())

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        angle = math.radians(45 + (pygame.time.get_ticks() % 360))
        self.velocity_x = BALL_SPEED * math.cos(angle)
        self.velocity_y = BALL_SPEED * math.sin(angle)
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def check_wall_collision(self, top_paddle, bottom_paddle, left_paddle, right_paddle):
        ball_rect = self.get_rect()
        
        if ball_rect.colliderect(top_paddle.get_rect()) and self.velocity_y < 0:
            self.velocity_y = abs(self.velocity_y)
            self.adjust_angle_from_paddle(top_paddle)
        
        if ball_rect.colliderect(bottom_paddle.get_rect()) and self.velocity_y > 0:
            self.velocity_y = -abs(self.velocity_y)
            self.adjust_angle_from_paddle(bottom_paddle)
        
        if ball_rect.colliderect(left_paddle.get_rect()) and self.velocity_x < 0:
            self.velocity_x = abs(self.velocity_x)
            self.adjust_angle_from_paddle(left_paddle)
        
        if ball_rect.colliderect(right_paddle.get_rect()) and self.velocity_x > 0:
            self.velocity_x = -abs(self.velocity_x)
            self.adjust_angle_from_paddle(right_paddle)
    
    def adjust_angle_from_paddle(self, paddle):
        ball_center = self.x + BALL_SIZE // 2
        if paddle.is_horizontal:
            paddle_center = paddle.x + paddle.width // 2
            diff = (ball_center - paddle_center) / (paddle.width // 2)
            self.velocity_x += diff * 2
        else:
            paddle_center = paddle.y + paddle.height // 2
            diff = (ball_center - paddle_center) / (paddle.height // 2)
            self.velocity_y += diff * 2
        
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if speed > 0:
            self.velocity_x = (self.velocity_x / speed) * BALL_SPEED
            self.velocity_y = (self.velocity_y / speed) * BALL_SPEED
    
    def check_boundary(self):
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT:
            return True
        return False
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.get_rect())

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("4-Way Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.state = "menu"
        
        self.top_paddle = Paddle(WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, 10, PADDLE_WIDTH, PADDLE_HEIGHT, True)
        self.bottom_paddle = Paddle(WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, WINDOW_HEIGHT - 25, PADDLE_WIDTH, PADDLE_HEIGHT, True)
        self.left_paddle = Paddle(10, WINDOW_HEIGHT // 2 - PADDLE_WIDTH // 2, PADDLE_HEIGHT, PADDLE_WIDTH, False)
        self.right_paddle = Paddle(WINDOW_WIDTH - 25, WINDOW_HEIGHT // 2 - PADDLE_WIDTH // 2, PADDLE_HEIGHT, PADDLE_WIDTH, False)
        
        self.ball = Ball()
        
        self.player1_lives = LIVES_PER_PLAYER
        self.player2_lives = LIVES_PER_PLAYER
        self.winner = None
        
    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state = "playing"
                self.ball.reset()
                self.player1_lives = LIVES_PER_PLAYER
                self.player2_lives = LIVES_PER_PLAYER
                self.winner = None
    
    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "menu"
    
    def handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state = "menu"
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.top_paddle.move_left()
        if keys[pygame.K_d]:
            self.top_paddle.move_right()
        
        if keys[pygame.K_w]:
            self.left_paddle.move_left()
        if keys[pygame.K_s]:
            self.left_paddle.move_right()
        
        if keys[pygame.K_LEFT]:
            self.bottom_paddle.move_left()
        if keys[pygame.K_RIGHT]:
            self.bottom_paddle.move_right()
        
        if keys[pygame.K_UP]:
            self.right_paddle.move_left()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_right()
    
    def update(self):
        if self.state == "playing":
            self.handle_input()
            self.ball.update()
            self.ball.check_wall_collision(self.top_paddle, self.bottom_paddle, self.left_paddle, self.right_paddle)
            
            if self.ball.check_boundary():
                if self.ball.y < WINDOW_HEIGHT // 2 or self.ball.x < WINDOW_WIDTH // 2:
                    self.player1_lives -= 1
                else:
                    self.player2_lives -= 1
                
                if self.player1_lives <= 0:
                    self.winner = "Player 2"
                    self.state = "game_over"
                elif self.player2_lives <= 0:
                    self.winner = "Player 1"
                    self.state = "game_over"
                else:
                    self.ball.reset()
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.big_font.render("4-WAY PONG", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        instructions = [
            "Player 1 Controls:",
            "  Top Paddle: A/D",
            "  Left Paddle: W/S",
            "",
            "Player 2 Controls:",
            "  Bottom Paddle: Left/Right Arrows",
            "  Right Paddle: Up/Down Arrows",
            "",
            "Each player starts with 3 lives",
            "Lose a life when the ball goes out",
            "",
            "Press SPACE to start",
            "Press ESC to return to menu"
        ]
        
        y_offset = 250
        for instruction in instructions:
            text = self.font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40
    
    def draw_game(self):
        self.screen.fill(BLACK)
        
        pygame.draw.line(self.screen, GRAY, (0, WINDOW_HEIGHT // 2), (WINDOW_WIDTH, WINDOW_HEIGHT // 2), 2)
        pygame.draw.line(self.screen, GRAY, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT), 2)
        
        self.top_paddle.draw(self.screen)
        self.bottom_paddle.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        
        self.ball.draw(self.screen)
        
        player1_text = self.font.render(f"Player 1 Lives: {self.player1_lives}", True, BLUE)
        player2_text = self.font.render(f"Player 2 Lives: {self.player2_lives}", True, RED)
        
        self.screen.blit(player1_text, (20, 20))
        self.screen.blit(player2_text, (WINDOW_WIDTH - player2_text.get_width() - 20, WINDOW_HEIGHT - 40))
    
    def draw_game_over(self):
        self.screen.fill(BLACK)
        
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(game_over_text, game_over_rect)
        
        if self.winner:
            winner_text = self.big_font.render(f"{self.winner} WINS!", True, WHITE)
            winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, 350))
            self.screen.blit(winner_text, winner_rect)
        
        player1_final = self.font.render(f"Player 1 Lives: {max(0, self.player1_lives)}", True, BLUE)
        player2_final = self.font.render(f"Player 2 Lives: {max(0, self.player2_lives)}", True, RED)
        
        player1_rect = player1_final.get_rect(center=(WINDOW_WIDTH // 2, 450))
        player2_rect = player2_final.get_rect(center=(WINDOW_WIDTH // 2, 500))
        
        self.screen.blit(player1_final, player1_rect)
        self.screen.blit(player2_final, player2_rect)
        
        instruction_text = self.font.render("Press SPACE to return to menu", True, LIGHT_GRAY)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, 600))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.state == "menu":
                    self.handle_menu_events(event)
                elif self.state == "playing":
                    self.handle_game_events(event)
                elif self.state == "game_over":
                    self.handle_game_over_events(event)
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
