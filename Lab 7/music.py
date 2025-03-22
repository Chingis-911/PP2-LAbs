import pygame



pygame.init()

songs = ["song1.mp3",'song2.mp3','song3.mp3',"song4.mp3",'song5.mp3','song6.mp3']
images =['p1.jpeg','p2.jpeg','p3.jpeg','p4.jpeg','p5.jpeg','p6.png']

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Music Player")



running = True
current_song_index = 0
current_pic_index = 0
showim = pygame.image.load(images[current_pic_index])


font = pygame.font.Font(None, 30)
instructions = [
    "SPACE - Play",
    "LSHIFT - Pause",
    "RSHIFT - Resume",
    "UP - Next Song",
    "DOWN - Previous Song",
    "ESC - Quit"
]


while running:
 screen.fill((0, 0, 0))  # Clear screen (Black background)
 screen.blit(showim,(200,200))
 
 y = 20  
 for instruction in instructions:
    text_surface = font.render(instruction, True, (255, 255, 255))
    screen.blit(text_surface, (20, y)) 
    y += 30 

 pygame.display.flip() 


 for event in pygame.event.get():

  if event.type ==  pygame.KEYDOWN and event.key ==  pygame.K_SPACE:
       showim = pygame.image.load(images[current_pic_index])
       pygame.mixer.music.load(songs[current_song_index])
       pygame.mixer.music.play()
  
  if event.type ==  pygame.KEYDOWN and event.key ==  pygame.K_RSHIFT:
     pygame.mixer.music.unpause()


  if event.type ==  pygame.KEYDOWN and event.key ==  pygame.K_LSHIFT:
     pygame.mixer.music.pause()
 
  if event.type ==  pygame.KEYDOWN and event.key ==  pygame.K_UP:
          current_song_index = (current_song_index + 1) % len(songs)
          current_pic_index = (current_pic_index + 1) % len(images)
          pygame.mixer.music.load(songs[current_song_index])
          pygame.mixer.music.play()
          showim = pygame.image.load(images[current_pic_index])
          
  if event.type ==  pygame.KEYDOWN and event.key == pygame.K_DOWN:
          current_song_index = (current_song_index - 1) % len(songs)
          current_pic_index = (current_pic_index - 1) % len(images)
          pygame.mixer.music.load(songs[current_song_index])
          pygame.mixer.music.play()
          showim = pygame.image.load(images[current_pic_index])
  if event.type ==  pygame.KEYDOWN and  event.key == pygame.K_ESCAPE:
      running = False

pygame.quit()