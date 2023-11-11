import pygame
import random
import sys

pygame.init()
pygame.font.init()

# Sizes
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_SIZE = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 5
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PONG")

# Game Variables
MAIN_MENU, GAME_RUN, EXIT = 0, 1, 2
game_state = MAIN_MENU
difficulty = "Normal"

# Player and Computer
player_paddle_y = SCREEN_HEIGHT / 2
computer_paddle_y = SCREEN_HEIGHT / 2

# Ball
ball_x, ball_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
ball_direction_x, ball_direction_y = random.choice([-1, 1]), random.choice([-1, 1])

# Score
player_score, computer_score = 0, 0

# Timer
clock = pygame.time.Clock()

def main_menu():
    global game_state, difficulty, SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SPEED_X, BALL_SPEED_Y, PADDLE_SPEED, screen


    menu_font = pygame.font.SysFont(None, 50)
    easy_text = menu_font.render("Press 1: Easy Mode", True, (255, 255, 255))
    normal_text = menu_font.render("Press 2: Normal Mode", True, (255, 255, 255))
    hard_text = menu_font.render("Press 3: Hard Mode", True, (255, 255, 255))
    extreme_text = menu_font.render("Press 4: Extreme Mode", True, (255, 255, 255))

    while game_state == MAIN_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    BALL_SPEED_X, BALL_SPEED_Y = 3, 3
                    PADDLE_SPEED = 7
                    pygame.display.set_caption("PONG - Mode: Easy /\n Press Q to Quit")
                    game_state = GAME_RUN

                elif event.key == pygame.K_2:
                    difficulty = "Normal"
                    pygame.display.set_caption("PONG - Mode: Normal /\n Press Q to Quit")
                    game_state = GAME_RUN

                elif event.key == pygame.K_3:
                    difficulty = "Hard"
                    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("PONG - Mode: Hard /\n Press Q to Quit")
                    PADDLE_SPEED = 5
                    BALL_SPEED_X, BALL_SPEED_Y = 8, 8
                    game_state = GAME_RUN

                elif event.key == pygame.K_4:
                    difficulty = "Extreme"
                    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 300
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("PONG - Mode: Extreme /\n Press Q to Quit")
                    PADDLE_SPEED = 10
                    BALL_SPEED_X, BALL_SPEED_Y = 10, 10
                    game_state = GAME_RUN

        screen.fill(BLACK)
        screen.blit(easy_text, (100, 100))
        screen.blit(normal_text, (100, 200))
        screen.blit(hard_text, (100, 300))
        screen.blit(extreme_text, (100, 400))
        pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == GAME_RUN and event.key == pygame.K_m:
                game_state = MAIN_MENU
            elif game_state == GAME_RUN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    if game_state == MAIN_MENU:
        main_menu()
    elif game_state == GAME_RUN:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Player Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_paddle_y -= PADDLE_SPEED
            if keys[pygame.K_DOWN]:
                player_paddle_y += PADDLE_SPEED
            # Back to Menu
            if keys[pygame.K_m]:
                main_menu()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
            """if keys[pygame.K_m]:
                main_menu()"""

            # Computer Movement
            if computer_paddle_y < ball_y:
                computer_paddle_y += PADDLE_SPEED
            else:
                computer_paddle_y -= PADDLE_SPEED

            ball_x += BALL_SPEED_X * ball_direction_x
            ball_y += BALL_SPEED_Y * ball_direction_y

            if ball_y <= 0 or ball_y >= SCREEN_HEIGHT:
                ball_direction_y *= -1
            if ball_x <= PADDLE_WIDTH:
                if player_paddle_y <= ball_y <= player_paddle_y + PADDLE_HEIGHT:
                    ball_direction_x *= -1
                else:
                    computer_score += 1
                    ball_x, ball_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
            elif ball_x >= SCREEN_WIDTH - PADDLE_WIDTH:
                if computer_paddle_y <= ball_y <= computer_paddle_y + PADDLE_HEIGHT:
                    ball_direction_x *= -1
                else:
                    player_score += 1
                    ball_x, ball_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

            # Render screen black
            screen.fill(BLACK)

            # Render ball and paddles
            pygame.draw.rect(screen, WHITE, [0, player_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT])
            pygame.draw.rect(screen, WHITE,
                             [SCREEN_WIDTH - PADDLE_WIDTH, computer_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT])
            pygame.draw.ellipse(screen, WHITE, [ball_x, ball_y, BALL_SIZE, BALL_SIZE])

            # Render score
            font = pygame.font.SysFont(None, 36)
            player_score_text = font.render(f"Player: {player_score}", True, WHITE)
            computer_score_text = font.render(f"Computer: {computer_score}", True, WHITE)
            screen.blit(player_score_text, (50, 20))
            screen.blit(computer_score_text, (SCREEN_WIDTH - 200, 20))

            # Render locations of ball and paddles
            """font_print = pygame.font.SysFont(None, 15)
            print_text = font_print.render(
                f"Player Paddle: {player_paddle_y}, Computer Paddle: {computer_paddle_y}, Ball: ({ball_x}, {ball_y})",
                True, WHITE)
            screen.blit(print_text, (SCREEN_WIDTH - 580, 10))"""

            # Updating display
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    elif game_state == EXIT:
        pygame.quit()
        sys.exit()