import pygame, threading

class player_char:
    def __init__(self, screen):
        self.screen = screen
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.color = "white"
        self.size = 20

        # Physics properties
        self.velocity = pygame.Vector2(0,0)
        self.gravity = 800
        self.jump_speed = -70        
        self.terminal_vel = 1200

        # physics X
        self.move_speed = 20
        self.skid_distance = 23
        

        # double jump properties
        self._can_double_jump = True

        # ground detection
        self.ground_y = screen.get_height()-self.size
        self.on_ground = False

        self.jump_pressed = False



    def update(self, keys, dt, camera_offset = pygame.Vector2(0,0)):
        print(self.velocity)
        self.apply_physics(dt)
        self.controls(keys, dt)
        self.check_ground_collision()
        self.draw_character(camera_offset)
        

    def apply_physics(self, dt):
        if not self.on_ground:
            self.velocity.y += self.gravity*dt

            if self.velocity.y > self.terminal_vel:
                self.velocity.y = self.terminal_vel

        self.player_pos.x += self.velocity.x *dt
        self.player_pos.y += self.velocity.y *dt

    def check_ground_collision(self):
        

        if self.player_pos.y >= self.ground_y:
            self.player_pos.y = self.ground_y
            self.velocity.y = 0
            self.on_ground = True
            self._can_double_jump = True
        else:
            self.on_ground = False

    def draw_character(self, camera_offset):
        screen_pos = self.player_pos - camera_offset
        pygame.draw.circle(self.screen, self.color, screen_pos, self.size)

    def controls(self, keys, dt):
        
        space_pressed = keys[pygame.K_SPACE]
        

        if (space_pressed and not self.jump_pressed and self.on_ground):
            # print("jumped")
                        
            self.player_pos.y -= 1
            self.velocity.y = -300
            self.on_ground = False
        elif (space_pressed and not self.jump_pressed and not self.on_ground and self._can_double_jump):
            self.player_pos.y -= 1
            self.velocity.y = -400
            self.on_ground = False
            self._can_double_jump = False
        
        self.jump_pressed = space_pressed
        
        # when in air less x force on player and further skid
        # when on ground more x force but shorter skid
        # double jump gives x bump

        speed = self.move_speed
        if abs(self.velocity.x) > 10:

            if not self.on_ground:
                skid_distance = self.skid_distance*3
                speed = speed/2.2 if self._can_double_jump else speed*0.7
            else:
                skid_distance = self.skid_distance 

            self.velocity.x -= (self.velocity.x/skid_distance)

        else:
            self.velocity.x = 0



        if keys[pygame.K_a]:
            self.velocity.x -= speed
        elif keys[pygame.K_d]:
            self.velocity.x += speed