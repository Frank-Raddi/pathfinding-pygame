import pygame, sys, random, math
import GameManager, GameObjects

#region Init
# General setup
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('BurstConnect')

# Global Variables
bg_color = pygame.Color('#2F373F')
accent_color = (27,35,43)
basic_font = pygame.font.Font('freesansbold.ttf', 32)
#plob_sound = pygame.mixer.Sound("BurstConnect\\Pong_in_Pygame\\pong.wav")
#score_sound = pygame.mixer.Sound("BurstConnect\\Pong_in_Pygame\\score.wav")

# Game objects
playerCount = 2
player_group = pygame.sprite.Group()
for each in range(playerCount):
    player = GameObjects.Player('BurstConnect\\Pong_in_Pygame\\Paddle.png',screen_width - 20,screen_height/2,5)
    player_group.add(player)

ball_group = pygame.sprite.Group()
for each in (playerCount * 25):
    ball = GameObjects.Ball('BurstConnect\\Pong_in_Pygame\\Ball.png',screen_width/2,screen_height/2,5,player_group)
    ball_group.add(ball)

game_manager = GameManager(ball_group,player_group)

#endregion


def Main():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.movement -= player.speed
                if event.key == pygame.K_DOWN:
                    player.movement += player.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement += player.speed
                if event.key == pygame.K_DOWN:
                    player.movement -= player.speed

        # Background Stuff
        screen.fill(bg_color)
        pygame.draw.rect(screen,accent_color,middle_strip)

        # Run the game
        game_manager.run_game()

        # Rendering
        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    Main()