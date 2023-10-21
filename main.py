import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reality Sim.")

# Constants
PLANET_MASS = 100
ASS_MASS = 5    # ass-teroid
G = 3        # gravitational constant
FPS = 60
PLANET_SIZE = 50    # radius of planet
ASS_SIZE = 15
VEL_SCALE = 100

# import images
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("Eoth.png"), (PLANET_SIZE*2, PLANET_SIZE*2))
ASS = pygame.transform.scale(pygame.image.load("Assteroid.png"), (ASS_SIZE*2, ASS_SIZE*2))

# Colours
#           R    G    B
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
BLUE    = (  0,   0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Assteroid:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        # self.angular_vel = random.randint(0, 100)

    def update(self, planet=None): # move
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / (distance**2)
        acceleration = force / self.mass

        d_x = planet.x - self.x
        d_y = planet.y - self.y
        # theta = tan-1( perp / base )
        angle = math.atan2(d_y,d_x)

        # components of acceleration
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        win.blit(ASS, (int(self.x) - ASS_SIZE, int(self.y) - ASS_SIZE))

def create_assteroid(position, mouse_pos):
    t_x, t_y = position
    m_x, m_y = mouse_pos
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Assteroid(t_x, t_y, -vel_x, -vel_y, ASS_MASS)
    return obj


def main():
    clock = pygame.time.Clock()

    planet = Planet(WIDTH/2, HEIGHT/2, PLANET_MASS)
    objects = []
    temp_object_pos = None

    # Mainloop
    is_running = True
    while is_running:
        clock.tick(FPS)

        # Input
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    is_running = False

                case pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        is_running = False

                case pygame.MOUSEBUTTONDOWN:
                    if temp_object_pos:
                        obj = create_assteroid(temp_object_pos, mouse_pos)
                        objects.append(obj)
                        temp_object_pos = None
                    else:
                        temp_object_pos = mouse_pos
                
                case _:
                    pass

        # Display
        # win.blit(BG, (0, 0))
        BGC = (60,82,145)
        win.fill(BGC)

        if temp_object_pos:
            pygame.draw.line(win, WHITE, temp_object_pos, mouse_pos)
            win.blit(ASS, (temp_object_pos[0] - ASS_SIZE, temp_object_pos[1] - ASS_SIZE))

        for obj in objects[:]:
            obj.update(planet)
            is_off_screen = (obj.x < 0) or (obj.x > WIDTH) or (obj.y < 0) or (obj.y > HEIGHT)

            # Check if assteroid collided with planet
            # check distance b/w them
            is_collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) < PLANET_SIZE

            if is_off_screen or is_collided:
                objects.remove(obj)
            obj.draw()
        planet.draw()

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()