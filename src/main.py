import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics Ball")

# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Ball properties
ball_radius = 50
ball_pos = [width // 2, height // 2]
ball_speed = [0, 0]
gravity = 0.1
bounce_factor = 0.9
ground_height = height - 100
dragging = False
drag_start_pos = [0, 0]
friction = 0.01

# Arrow properties
arrow_length = 50

# Border properties
border_width = 10
border_color = (0, 0, 255)

# Font setup
font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()  # Create a clock object

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not dragging:
                dragging = True
                drag_start_pos = list(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                mouse_pos = pygame.mouse.get_pos()
                # Calculate the direction and speed based on how far the mouse was dragged
                direction = [mouse_pos[0] - drag_start_pos[0], mouse_pos[1] - drag_start_pos[1]]
                speed = math.sqrt(direction[0] ** 2 + direction[1] ** 2) / 10  # Adjust the division value for desired speed
                if speed > 10:  # Limit the maximum speed
                    speed = 10
                ball_speed = [direction[0] / speed, direction[1] / speed]

    # Apply gravity if not dragging
    if not dragging:
        ball_speed[1] += gravity

    # Apply friction when the ball is sliding along the floor
    if abs(ball_speed[0]) > 0:
        ball_speed[0] -= math.copysign(friction, ball_speed[0])

    # Update ball position
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Check for collision with ground
    if ball_pos[1] + ball_radius >= ground_height:
        ball_pos[1] = ground_height - ball_radius
        ball_speed[1] *= -bounce_factor

    # Check for collision with walls
    if ball_pos[0] - ball_radius <= border_width:
        ball_pos[0] = border_width + ball_radius
        ball_speed[0] *= -bounce_factor
    elif ball_pos[0] + ball_radius >= width - border_width:
        ball_pos[0] = width - border_width - ball_radius
        ball_speed[0] *= -bounce_factor
    if ball_pos[1] - ball_radius <= border_width:
        ball_pos[1] = border_width + ball_radius
        ball_speed[1] *= -bounce_factor
    elif ball_pos[1] + ball_radius >= height - border_width:
        ball_pos[1] = height - border_width - ball_radius
        ball_speed[1] *= -bounce_factor

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the ground
    pygame.draw.rect(screen, (0, 255, 0), (0, ground_height, width, height - ground_height))

    # Draw the border
    pygame.draw.rect(screen, border_color, (0, 0, width, border_width))  # Top border
    pygame.draw.rect(screen, border_color, (0, 0, border_width, height))  # Left border
    pygame.draw.rect(screen, border_color, (width - border_width, 0, border_width, height))  # Right border
    pygame.draw.rect(screen, border_color, (0, height - border_width, width, border_width))  # Bottom border

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Draw the arrow
    if dragging:
        pygame.draw.line(screen, BLUE, (ball_pos[0], ball_pos[1]), (ball_pos[0] + direction[0], ball_pos[1] + direction[1]), 2)

    text_Position = font.render(f"Position: ({ball_pos[0]}, {ball_pos[1]})", True, BLACK)
    screen.blit(text_Position, (10, 10))

    text_Speed = font.render(f"Speed: ({ball_speed[0]}, {ball_speed[1]})", True, BLACK)
    screen.blit(text_Speed, (10, 30))

    # Update the display
    pygame.display.flip()

    clock.tick(120)  # Limit the frame rate to 120 FPS
