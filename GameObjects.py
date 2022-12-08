import pygame, sys, random, math
import GameManager

class Block(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Player(Block):
    def __init__(self,path,x_pos,y_pos,speed):
        super().__init__(path,x_pos,y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self,ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

class Opponent(Block):
    def __init__(self,path,x_pos,y_pos,speed):
        super().__init__(path,x_pos,y_pos)
        self.speed = speed

    def update(self,ball_group):
        if self.rect.centery < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.centery > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height

class Ball(Block):
    def __init__(self,path,x_pos,y_pos,speed,paddles):
        super().__init__(path,x_pos,y_pos)
        self.angle = random.choice([random.choice([random.randint(10,80), random.randint(100,170)]), random.choice([random.randint(190,260), random.randint(280,350)])])
        self.speed = self.init_speed = speed
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        self.paddles = paddles
        self.active = False
        self.score_time = 0
        self.path = []

    def update(self):
        if self.active:
            self.collisions()
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            print(self.rect.x,self.rect.y, self.speed_x,self.speed_y, self.angle, self.speed)
            self.draw_path()

        else:
            self.restart_counter()
        print("update")
        
    def collisions(self):
        print("collisions")
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.floor_reflection()

        if pygame.sprite.spritecollide(self,self.paddles,False):
            pygame.mixer.Sound.play(plob_sound)
            collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.wall_reflection()
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.wall_reflection()
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.wall_reflection()
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.wall_reflection()

            self.speed *= 1.2

        #def angle after bounce off 90 degree wall
    def wall_reflection(self):
        self.angle = (360 - self.angle) % 360

        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        print("wall_reflection")

    def floor_reflection(self):
        if self.angle == 0 or self.angle == 180:
            self.angle = (180 - self.angle) % 360
        else:
            self.angle = (540 - self.angle) % 360

        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        print("floor_reflection")


    def reset_ball(self):
        self.angle = random.choice([random.choice([random.randint(10,80), random.randint(100,170)]), random.choice([random.randint(190,260), random.randint(280,350)])])
        self.speed = self.init_speed
        self.active = False
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2,screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 0:
            self.active = True

        time_counter = basic_font.render(str(countdown_number),True,accent_color)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2,screen_height/2 + 50))
        pygame.draw.rect(screen,bg_color,time_counter_rect)
        screen.blit(time_counter,time_counter_rect)
        
    def draw_path(self):
        self.path.append(self.rect.center)
        for each in self.path:
            pygame.draw.circle(screen, (255,255,255), each, 3)