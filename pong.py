import pygame
pygame.init()       # initializes some basic stuffs
pygame.mixer.init()

WIDTH, HEIGHT = 700, 500    # setting up width and height for our game


pygame.mixer.music.load('sounds/pong_music.wav')
pygame.mixer.music.play()
miss_sound = pygame.mixer.Sound('sounds/wrongSound.wav')
bg_image = pygame.image.load('images/black-bg-1.jpg')

# pygame.display - module to control the display window and screen

WIN = pygame.display.set_mode((WIDTH, HEIGHT))     # used to initialize a window or screen for display
pygame.display.set_caption("PONG")

FPS = 60        # frames per second
clock = pygame.time.Clock()

# OBJ DETAILS

# -- PADDLE DETAILS
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

# -- BALL DETAILS
BALL_RADIUS = 7

# Colors - tupple rgb values for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --------------
WINNING_SCORE = 5


FONT = pygame.font.SysFont("chalkduster.ttf", 100)

class Paddle:
    COLOR = WHITE
    VEL = 5         # vel for velocity

    def __init__(self, x, y, width, height):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
         
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y




class Ball:
    COLOR = WHITE
    VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.radius = radius
        self.x_vel = self.VEL   # initially ball will only have x vel
        self.y_vel = 0

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.y_vel = 0
        self.x_vel *= -1



def draw(win, objects, left_score, right_score):
    win.fill(BLACK)
    win.blit(bg_image, (0, 0))
    for obj in objects:         # obj will contain objects like paddle, ball and other objects in screen
        obj.draw(win)
    
    left_score_text = FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    pygame.display.update()

def reset_board(obj, left_score, right_score):
    for i in obj:
        i.reset()
    draw(WIN, obj, left_score, right_score)
    

def draw_win_board(win, left_won = True):
    win.fill(BLACK)
    if (left_won):
        text = FONT.render("Left Player Won", 1, WHITE)
        WIN.blit(text, (WIDTH //2 - text.get_width() // 2, HEIGHT//2))
    else:
        text = FONT.render("Right Player Won", 1, WHITE)
        WIN.blit(text, (WIDTH //2 - text.get_width() // 2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(2000)
    

def move_paddle(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:        # if it is key w & checking if the paddle is not going out of screen
        left_paddle.move()
    if keys[pygame.K_s] and left_paddle.y + PADDLE_HEIGHT + left_paddle.VEL <= HEIGHT:
        left_paddle.move(False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move()
    if keys[pygame.K_DOWN] and right_paddle.y + PADDLE_HEIGHT + right_paddle.VEL <= HEIGHT:
        right_paddle.move(False)


def handle_collision(ball, left_paddle, right_paddle):
    # if it touches ceil make the y vel opposite 
    # ceil
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # paddle
    if ball.x_vel < 0:      # if it collides with left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x + ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

                               

    else:                   # means right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel




    
def main():
    run = True

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0
    obj = [left_paddle, right_paddle, ball]         # contains objects

    while run:
        clock.tick(FPS)
        
        draw(WIN, obj, left_score, right_score)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        move_paddle(keys, left_paddle, right_paddle)  
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:      # left missed
            right_score += 1
            pygame.mixer.music.stop()
            miss_sound.play()
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            pygame.time.delay(500)
            pygame.mixer.music.play()
        elif ball.x > WIDTH:        # right missed
            left_score += 1
            pygame.mixer.music.stop()
            miss_sound.play()
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            pygame.time.delay(500)
            pygame.mixer.music.play()

        if left_score >= WINNING_SCORE:
            draw_win_board(WIN)
            reset_board(obj, left_score, right_score)
        elif right_score >= WINNING_SCORE:
            draw_win_board(WIN, False)
            reset_board(obj, left_score, right_score)

    pygame.quit()


if __name__ == "__main__":
    main()

    

 

