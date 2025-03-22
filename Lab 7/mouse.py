import pygame
from datetime import datetime

pygame.init()
done = False
clock = pygame.time.Clock()

image1 = pygame.image.load('clock.png')
image2 = pygame.image.load('sec_hand.png')
image3 = pygame.image.load('min_hand.png')

mickey = pygame.transform.scale(image1,(500,500))
size= mickey.get_size()
screen = pygame.display.set_mode(size)

sec_hand = pygame.transform.scale(image2, (150, 10))  # Adjust width & height
min_hand = pygame.transform.scale(image3, (120, 12))


def blit_rotate_center(surf, image, angle, pos):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=pos)
    surf.blit(rotated_image, new_rect.topleft)

while not done:
        now = datetime.now()
        sec_ang = -now.second * 6
        min_ang = -now.minute * 6
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        done = True
         
        screen.fill((255, 255, 255))
        
        
        screen.blit(mickey,(0,0))

        center_pos = (size[0] // 2,size[1] // 2)
        
        blit_rotate_center(screen, image2, sec_ang, center_pos)  # Adjust pivot point
        blit_rotate_center(screen, image3, min_ang, center_pos)

       
     

        pygame.display.flip()
        clock.tick(60)

pygame.quit()        
