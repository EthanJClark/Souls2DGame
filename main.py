import pygame, player

pygame.init()


screen = pygame.display.set_mode((1280,720))
char1 = player.player_char(screen)


camera_offset = pygame.Vector2(0,0)

clock = pygame.time.Clock()
running = True

dt = 0

def draw_grid(screen, camera_offset, grid_size = 50, thickness = 1):
    start_x = int(camera_offset.x // grid_size) * grid_size
    start_y = int(camera_offset.y // grid_size) * grid_size
    
    # Draw vertical lines
    for x in range(start_x, start_x + screen.get_width() + grid_size, grid_size):
        screen_x = x - camera_offset.x
        pygame.draw.line(screen, (40, 40, 40), (screen_x, 0), (screen_x, screen.get_height()), width=thickness)
    
    # Draw horizontal lines
    for y in range(start_y, start_y + screen.get_height() + grid_size, grid_size):
        screen_y = y - camera_offset.y
        pygame.draw.line(screen, (40, 40, 40), (0, screen_y), (screen.get_width(), screen_y), width=thickness)

while running:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera_offset.x = char1.player_pos.x - screen.get_width()/2
    camera_offset.y = char1.player_pos.y- (screen.get_height()/2) - 200
        
    draw_grid(screen, camera_offset, 50)

    char1.update(pygame.key.get_pressed(),dt, camera_offset)


    pygame.display.flip()

    dt = clock.tick(60)/1000