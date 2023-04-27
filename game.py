import pygame
from random import randint

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


class Ball(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the ball,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4, 8), randint(-8, 8)]

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    # Move the ball
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Bounce the ball if needed
        if self.rect.top < 0:
            self.velocity[1] = -self.velocity[1]
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.velocity[1] = -self.velocity[1]
            self.rect.bottom = SCREEN_HEIGHT

    # Resets the ball location and velocity
    def reset(self):
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2
        self.velocity = [randint(4, 8), randint(-8, 8)]


class Paddle(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the paddle,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    # Move the paddle
    def move_up(self, pixels):
        self.rect.y -= pixels
        # Keep paddle on the screen
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels
        # Keep paddle on the screen
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height


class Game:
    def __init__(self):
        # initialize pygame and create window
        pygame.init()
        pygame.mixer.init()
        self.screen_width = 800
        self.screen_height = 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("PyPong (read if gay)")
        self.clock = pygame.time.Clock()

        # set up game objects
        self.all_sprites = pygame.sprite.Group()
        self.player1 = Paddle(RED, 10, 100)
        self.player1.rect.x = 20
        self.player1.rect.y = self.screen_height / 2 - self.player1.rect.height / 2
        self.player2 = Paddle(BLUE, 10, 100)
        self.player2.rect.x = self.screen_width - 30
        self.player2.rect.y = self.screen_height / 2 - self.player2.rect.height / 2
        self.ball = Ball(WHITE, 10, 10)
        self.ball.rect.x = self.screen_width / 2
        self.ball.rect.y = self.screen_height / 2
        self.all_sprites.add(self.player1, self.player2, self.ball)

        # set up game variables
        self.game_over = False
        self.score = [0, 0]

    def run(self):
        # game loop
        while not self.game_over:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game_over = True
                    elif event.key == pygame.K_UP:
                        self.player2.move_up(50)
                    elif event.key == pygame.K_DOWN:
                        self.player2.move_down(50)
                    elif event.key == pygame.K_w:
                        self.player1.move_up(50)
                    elif event.key == pygame.K_s:
                        self.player1.move_down(50)

            # update game objects
            self.all_sprites.update()

            # check for collision with walls
            if self.ball.rect.top < 0 or self.ball.rect.bottom > self.screen_height:
                self.ball.velocity[1] = -self.ball.velocity[1]

            # check for collision with paddles
            if pygame.sprite.collide_rect(self.ball, self.player1) or pygame.sprite.collide_rect(self.ball,
                                                                                                 self.player2):
                self.ball.velocity[0] = -self.ball.velocity[0]

            # check if ball goes out of bounds
            if self.ball.rect.left < 0:
                self.score[1] += 1
                self.ball.velocity[0] = -self.ball.velocity[0]
                self.ball.rect.x = self.screen_width / 2
                self.ball.rect.y = self.screen_height / 2
            elif self.ball.rect.right > self.screen_width:
                self.score[0] += 1
                self.ball.velocity[0] = -self.ball.velocity[0]
                self.ball.rect.x = self.screen_width / 2
                self.ball.rect.y = self.screen_height / 2

            # draw objects
            self.screen.fill(BLACK)
            pygame.draw.line(self.screen, WHITE, [self.screen_width / 2, 0],
                             [self.screen_width / 2, self.screen_height], 5)
            self.all_sprites.draw(self.screen)

            # draw scores
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.score[0]), True, WHITE)
            self.screen.blit(text, (self.screen_width / 4, 10))
            text = font.render(str(self.score[1]), True, WHITE)
            self.screen.blit(text, (self.screen_width * 3 / 4, 10))

            # flip display
            pygame.display.flip()

            # pause for a bit
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
