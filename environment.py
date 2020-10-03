# environment.py
# Code written by: Ray
# >>> This file runs the environment (game) of snake
#     and returns necessary values for an agent to play
import pygame
from pygame.math import Vector2
import random
import math

class Environment:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Snake Agent")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25)
        
        self.load_data() # TODO: Load in agent data from files
        self.generation = 0
        self.protocol_function = None

    def load_data(self):
        pass # TODO: Load in agent data from files

    def set_protocol(self, protocol_function=None):
        def n_pass():
            pass

        if (protocol_function == None):
            self.protocol_function = n_pass
        else:
            self.protocol_function = protocol_function

    def new(self):
        self.playing = True
        self.freeze = False
        
        # Snake variables
        self.head_location = Vector2(random.randint(1, 18) * 30,  random.randint(1, 18) * 30) # 1-18 so that the snake does not spawn next to a wall
        self.body = [self.head_location]
        self.direction = random.choice( (Vector2(-1,0), Vector2(1,0), Vector2(0,1), Vector2(0, -1)) )
        self.snake_length = 1
        self.turns = 0
        self.generation += 1

        self.food_location = self.head_location
        self.move_food()

    def run(self):
        # game loop - set self.playing = False to end the game
        
        while True:
            while self.playing:
                self.dt = self.clock.tick(3) / 1000
                self.protocol_function(self)
                self.events()
                self.update()
                self.draw()

            while (self.freeze):
                self.dt = self.clock.tick(3) / 1000
                self.protocol_function(self)
                self.events()
                self.draw()

            if ( not self.playing ):
                self.close()

    def close(self):
        pygame.quit()
        quit()

    def update(self):
        # update portion of the game loop

        # Move snake body
        self.body.append( self.body[-1] + (self.direction * 30) )
        self.body.pop(0)
        self.head_location = self.body[-1]

        self.eat_food()
        self.boundaries()
        self.turns += 1

    def eat_food(self):
        if (self.head_location == self.food_location):
            self.move_food()
            if ( len(self.body) == 1 ):
                self.body.insert(0, self.body[0] - self.direction)
                self.snake_length += 1
            else:
                difference = self.body[0] - self.body[1]
                self.body.insert(0, self.body[0] + difference)
                self.snake_length += 1

    def move_food(self):
        while (self.food_location == self.head_location):
            self.food_location = Vector2(random.randint(1,18) * 30,  random.randint(1,18) * 30)

    def boundaries(self):

        for body in self.body[:-1]:
            if (self.head_location == body):
                self.freeze = True
                self.playing = False
                print("Game Frozen")
                return
        
        x = self.head_location.x; y = self.head_location.y

        if ( (x < 0 or y < 0) or (x >= 600 or y >= 600)):
            self.freeze = True
            self.playing = False
            print("Game Frozen")
    
    def get_obstacles(self):
            # True indicates open, False indicates taken
            head = self.head_location
            surroundings = [ head + Vector2(30,0), head + Vector2(-30,0), head + Vector2(0,30), head + Vector2(0,-30) ]
            results = []

            
            for item in surroundings:
                if item not in self.body:
                    if ( (item.x >= 0 and item.y >= 0) and (item.x <= 570 and item.y <= 570)):
                        results.append(True)
                    else:
                        results.append(False)
                else:
                    results.append(False)
            return results # right, left, down, up

    def get_position_apple_to_head(self):
        
        # True indicates shortest path, False indicates not so
        head = self.head_location
        surroundings = [head + Vector2(-30, -30), head + Vector2(0, -30), head + Vector2(30,-30),
                        head + Vector2(-30,0), head + Vector2(30, 0),
                        head + Vector2(-30,30), head + Vector2(0,30), head + Vector2(30,30)]

        def euclidean_distance(vector : pygame.math.Vector2) -> float:
            # Euclidian distance from the vector to the apple location
            return math.sqrt( ( (self.food_location.x - vector.x) ** 2 ) + ( (self.food_location.y - vector.y) ** 2 ) )

        shortest_distance = 999
        shortest_distance_index = 0

        for i in range(len(surroundings)):
            d = euclidean_distance(surroundings[i])
            if (d < shortest_distance):
                shortest_distance = d
                shortest_distance_index = i

        results = []
        for i in range(len(surroundings)):
            results.append(False)
        results[shortest_distance_index] = True

        return results
        
    def draw_gui(self):
            
        def get_obstacle_colors(list_obs):
            results = []

            for item in list_obs:
                if item:
                    results.append((23, 23, 23))
                else:
                    results.append((60,76,85))

            return results
        
        def get_distance_colors(list_obs):
            results = []

            for item in list_obs:
                if item:
                    results.append((110, 197, 135))
                else:
                    results.append((23,23,23))
            return results

        # draw background panel
        pygame.draw.rect(self.screen, (32, 39, 45), (600,0,400,600) )

        # Draw text
        text = self.font.render("Length: " + str(self.snake_length), True, (250, 250, 250))
        self.screen.blit(text, (640,40))

        # Draw text
        text = self.font.render("Generation: " + str(self.generation), True, (250, 250, 250))
        self.screen.blit(text, (640,80))

        # Draw text
        text = self.font.render("State - (obstacles)", True, (250, 250, 250))
        self.screen.blit(text, (640,200))

        # Draw obstacles grid
        obstacles = get_obstacle_colors(self.get_obstacles())

        # Draw visualized obstacles
        pygame.draw.rect(self.screen, obstacles[3], (780, 240, 40, 40)) #top one
        pygame.draw.rect(self.screen, obstacles[2], (780, 320, 40, 40)) #down
        pygame.draw.rect(self.screen,obstacles[0], (820, 280, 40, 40))  #right
        pygame.draw.rect(self.screen,obstacles[1], (740, 280, 40, 40))  #left

        # Draw text
        text = self.font.render("Position of Apple to head", True, (250, 250, 250))
        self.screen.blit(text, (640,380))

        # Draw apple to head grid
        distances = get_distance_colors(self.get_position_apple_to_head())
        pygame.draw.rect(self.screen, distances[0], (735, 420, 40, 40)) # top left
        pygame.draw.rect(self.screen, distances[1], (780, 420, 40, 40)) # top middle
        pygame.draw.rect(self.screen, distances[2], (825, 420, 40, 40)) # top right
        pygame.draw.rect(self.screen, distances[3], (735, 465, 40, 40)) # middle left
        pygame.draw.rect(self.screen, distances[4], (825, 465, 40, 40)) # middle right
        pygame.draw.rect(self.screen, distances[5], (735, 510, 40, 40)) # bottom left
        pygame.draw.rect(self.screen, distances[6], (780, 510, 40, 40)) # bottom middle
        pygame.draw.rect(self.screen, distances[7], (825, 510, 40, 40)) # bottom right


    def draw_grid(self):

        # Draw environment

        # Draw food
        pygame.draw.rect(self.screen, (110, 197, 135), (int(self.food_location.x) + 5, int(self.food_location.y) + 5, 20, 20))

        # Draw snake body
        [ pygame.draw.rect(self.screen, (7, 118, 92), (int(body.x), int(body.y), 30, 30)) for body in self.body if (body != self.head_location) ]
        
        # Draw snake head
        pygame.draw.circle(self.screen, (2, 206, 158), (int(self.head_location.x) + 15, int(self.head_location.y) + 15), 15)


        # Draw actual grid
        x = 0
        for i in range(20):
            pygame.draw.line(self.screen,(52,56,60), (x, 0), (x, 600), 1)
            x += 30
        
        y = 0
        for i in range(20):
            pygame.draw.line(self.screen, (52,56,60), (0, y), (600, y), 1)
            y += 30

    def draw(self):
        self.screen.fill((23, 23, 23)) 
        self.draw_grid()
        self.draw_gui()
        pygame.display.flip()

    def events(self):
        # Pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN:
                new_direction = Vector2(0,0)
                if event.key == pygame.K_RIGHT:
                    new_direction = Vector2(1,0)
                if event.key == pygame.K_LEFT:
                    new_direction = Vector2(-1, 0)
                if event.key == pygame.K_UP:
                    new_direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    new_direction = Vector2(0, 1)
                
                if (not ( new_direction == self.direction * -1 )):
                    self.direction = new_direction

    def reset(self):

        results = {"length" : self.snake_length, "generation" : self.generation, "turns" : self.turns}
        self.new()
        return results

# Needed returnable methods:
# get_obstacles()
# get_position_apple_to_head