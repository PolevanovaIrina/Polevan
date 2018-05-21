import pygame
import sys
import random
import time

class Game():

    def __init__(self):

        self.screen_width = 500
        self.screen_height = 500

        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 90, 255)
        self.brown = pygame.Color(0, 0, 42)
        self.bonus = pygame.Color(255, 45, 42)
        self.party = pygame.Color(34,67,80)
        self.antonio = pygame.Color(69,6,220)

        self.fps_controller = pygame.time.Clock()

        self.score = 0

    def set_surface_and_title(self):

        self.play_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake')

    def event_loop(self, change_to):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT :
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT :
                    change_to = "LEFT"
                elif event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def replace_screen(self):

        pygame.display.flip()
        game.fps_controller.tick(20)

    def h_score(self, choice=1):

        s_font = pygame.font.SysFont('Arial', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.black)

        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (40, 10)
        else:
            s_rect.midtop = (360, 120)

        self.play_screen.blit(s_surf, s_rect)
    def game_over(self):

        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_screen.blit(go_surf, go_rect)
        self.h_score(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

class Snake():
     def __init__(self, snake_color,snake_party):

         self.snake_head_pos = [100, 50]
         self.snake_body = [[100, 50], [90, 50], [80, 50]]
         self.snake_color = snake_color
         self.snake_party = snake_party
         self.direction = "RIGHT"
         self.change_to = self.direction

     def validate_direction_and_change(self):

         if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                 self.change_to == "LEFT" and not self.direction == "RIGHT",
                 self.change_to == "UP" and not self.direction == "DOWN",
                 self.change_to == "DOWN" and not self.direction == "UP")):
             self.direction = self.change_to

     def change_head_position(self):

         if self.direction == "RIGHT":
             self.snake_head_pos[0] += 10
         elif self.direction == "LEFT":
             self.snake_head_pos[0] -= 10
         elif self.direction == "UP":
             self.snake_head_pos[1] -= 10
         elif self.direction == "DOWN":
             self.snake_head_pos[1] += 10

     def snake_body_mechanism(self, k, score, food_pos, screen_width, screen_height, bonus_pos = (-1,-1)):

         k = k
         self.snake_body.insert(0, list(self.snake_head_pos))

         if (self.snake_head_pos[0] == bonus_pos[0] and
                     self.snake_head_pos[1] == bonus_pos[1]):
             bonus_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]
             k = 101
             score += 10
             self.snake_color = game.party

         if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width/10)*10,
                         random.randrange(1, screen_height/10)*10]
            self.snake_color = game.green
            score += 1


         else:
             self.snake_body.pop()

         return score, food_pos, k, bonus_pos

     def draw_snake(self, play_surface, surface_color):

         play_surface.fill(surface_color)
         for pos in self.snake_body:
             pygame.draw.rect(
                 play_surface, self.snake_color, pygame.Rect(
                     pos[0], pos[1], 10, 10))

     def check_for_boundaries(self, game_over, screen_width, screen_height):

         if any((
             self.snake_head_pos[0] > screen_width-10
             or self.snake_head_pos[0] < 0,
             self.snake_head_pos[1] > screen_height-10
             or self.snake_head_pos[1] < 0
                 )):
             game_over()
         for block in self.snake_body[1:]:

             if (block[0] == self.snake_head_pos[0] and
                     block[1] == self.snake_head_pos[1]):
                game_over()

class Food():

    def __init__(self, food_color, screen_width, screen_height):

        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10,
                        random.randrange(1, screen_height/10)*10]
    def draw_food(self, play_surface):

       pygame.draw.rect(
           play_surface, self.food_color, pygame.Rect(
               self.food_pos[0], self.food_pos[1],
               self.food_size_x, self.food_size_y))
class Bonus():

    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 12
        self.food_size_y = 12
        self.bonus_pos = [random.randrange(1, screen_width/10)*10,
                        random.randrange(1, screen_height/10)*10]

    def draw_bonus(self, play_surface, k):

        if k % 200 > 0 and k % 200 < 100:
            if k % 10 > 0 and k % 10 < 5:
                pygame.draw.rect(play_surface, self.food_color, pygame.Rect(
                    self.bonus_pos[0], self.bonus_pos[1],
                    self.food_size_x, self.food_size_y))
            else :
                pygame.draw.rect(play_surface, self.food_color, pygame.Rect(
                    self.bonus_pos[0], self.bonus_pos[1] - 5,
                    self.food_size_x + 5, self.food_size_y ))
        else:
            pass
class Antogonist():

    def __init__(self, a_color):
        self.a_color = a_color
        self.a_size = 15
        self.a_pos = [0,0]


    def a_run(self, food_pos):
        if m % 100 > 0 and m % 100 < 50:
            if self.a_pos[0] == food_pos[0] and self.a_pos[1] == food_pos[1] :
                zvx = 1
                zvy = 1
            elif self.a_pos[0] == food_pos[0]:
                zvx = 1
                zvy = int((- self.a_pos[1] + food_pos[1]) / ((- self.a_pos[1] + food_pos[1]) ** 2) ** 0.5)
            elif self.a_pos[1] == food_pos[1]:
                zvy = 1
                zvx = int((- self.a_pos[0] + food_pos[0]) / ((- self.a_pos[0] + food_pos[0]) ** 2) ** 0.5)
            else:
                zvx = int((- self.a_pos[0] + food_pos[0])/((- self.a_pos[0] + food_pos[0])**2)**0.5)
                zvy = int((- self.a_pos[1] + food_pos[1])/((- self.a_pos[1] + food_pos[1])**2)**0.5)
            self.a_pos[0] += 5 * zvx
            self.a_pos[1] += 5 * zvy
        return self.a_pos


    def a_win(self, score, food_pos, screen_width, screen_height, m):
        score = score
        food_pos = food_pos
        m = m
        if m % 400 > 0 and m % 400 < 200:
            if (self.a_pos[0] > food_pos[0] - 20) and (self.a_pos[1] < food_pos[1] + 20) and (self.a_pos[1] > food_pos[1] - 20) and (self.a_pos[0] < food_pos[0] + 20):
                food_pos = [random.randrange(1, screen_width / 10) * 10,
                            random.randrange(1, screen_height / 10) * 10]
                score -= 10
                m = 201
            if pygame.mouse.get_pressed()[0]:
                w, g = pygame.mouse.get_pos()
                if  (self.a_pos[0] > w - 20) and (self.a_pos[1] < g + 20) and (self.a_pos[1] > g - 20) and (self.a_pos[0] < w + 20):
                    score += 5
                    m = 201
        return score, food_pos, m



    def draw_a(self, play_surface,m, food_pos):
        self.a_pos = self.a_run(food_pos)
        if m % 400 > 0 and m % 400 < 200:
            pygame.draw.circle(play_surface, self.a_color,(
                self.a_pos[0], self.a_pos[1]), self.a_size)
        else:
            pass



game = Game()
snake = Snake(game.green, game.party)
antonio = Antogonist(game.antonio)
food = Food(game.brown, game.screen_width, game.screen_height)
bonus = Bonus(game.bonus, game.screen_width, game.screen_height)
pygame.font.init()
game.set_surface_and_title()
k = 0
m = 0
while True:
    m += 1
    k += 1
    snake.change_to = game.event_loop(snake.change_to)
    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos, k, bonus.bonus_pos = snake.snake_body_mechanism(k,
        game.score, food.food_pos,game.screen_width, game.screen_height, bonus.bonus_pos)
    snake.draw_snake(game.play_screen, game.white)
    food.draw_food(game.play_screen)
    bonus.draw_bonus(game.play_screen, k)
    game.score, food.food_pos, m = antonio.a_win( game.score, food.food_pos,game.screen_width, game.screen_height, m)
    antonio.draw_a(game.play_screen, m, food.food_pos)
    snake.check_for_boundaries(
    game.game_over, game.screen_width, game.screen_height)
    game.h_score()
    game.replace_screen()