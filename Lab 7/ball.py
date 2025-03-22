import pygame

pygame.init() 

screen = pygame.display.set_mode((640,480))
done = False

x = 100
y = 100

clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN  and event.key == pygame.K_UP:
           y -= 20
           if y < 20:
              y = 25
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
           y += 20
           if y > 480 - 25:
              y = 480 - 25
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
           x -= 20
           if x < 25:
              x = 25
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
           x += 20
           if x > 640 - 25:
              x = 640 - 25
    
    
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen,'red',(x,y),25)
    pygame.display.flip()
    clock.tick(60)
