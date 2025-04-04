import pygame
import math


pygame.init()

width,height = 600,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Paint")
icon = pygame.image.load('Images/apple.png')
pygame.display.set_icon(icon)

BLACK = (0, 0, 0)        
WHITE = (255, 255, 255)   
RED = (255, 0, 0) 
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

brush_size = 5
brush_color = BLACK

clock = pygame.time.Clock()

#Buttons
color_buttons = [
    {"rect": pygame.Rect(10, 10, 30, 30), "color": BLACK},
    {"rect": pygame.Rect(50, 10, 30, 30), "color": RED},
    {"rect": pygame.Rect(90, 10, 30, 30), "color": BLUE},
    {"rect": pygame.Rect(130, 10, 30, 30), "color": GREEN},
    {"rect": pygame.Rect(170, 10, 30, 30), "color": WHITE}, 
]
shapes = [
  {"var": pygame.Rect(210,10,30,30), "sh": "circ"},
  {"var": pygame.Rect(250,10,40,30), "sh": "rect"},
  {"var": pygame.Rect(290,10,30,30), "sh": "sqr"},
  {"var": pygame.Rect(330,10,40,30), "sh": "r_tr"},
  {"var": pygame.Rect(370,10,50,30), "sh": "eq_tr"},
  {"var": pygame.Rect(420,10,60,30), "sh": "rhomb"},
  {"var": pygame.Rect(490,10,60,30), "sh": "brush"},
  {"var": pygame.Rect(530,10,50,30), "sh": "clean"},
]                                                            

#Functions
current_tool = "brush"
drawing = False
start_pos = None
end_pos = None

def handle_events():
    global brush_size,brush_color,drawing,current_tool,start_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                brush_size += 2
            elif event.key == pygame.K_DOWN and brush_size >= 3:
                brush_size -= 2
        elif event.type == pygame.MOUSEBUTTONDOWN:
          for btn in color_buttons:
            if btn["rect"].collidepoint(event.pos):
              pygame.mixer.Sound('Sounds/select.wav').play()
              brush_color = btn["color"]
          
          for btn1 in shapes:
            if btn1["var"].collidepoint(event.pos):
                pygame.mixer.Sound('Sounds/select.wav').play()
                current_tool = btn1["sh"]


          if event.button == 1:
              start_pos = event.pos
              drawing = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
         end_pos = event.pos
         if drawing:
          if  current_tool == "circ":
           
           radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
           pygame.draw.circle(screen, brush_color, start_pos, radius)
         
          elif current_tool == "rect":
            x = min(start_pos[0], end_pos[0])
            y = min(start_pos[1], end_pos[1])
            width = abs(end_pos[0] - start_pos[0])
            height = abs(end_pos[1] - start_pos[1])
            pygame.draw.rect(screen, brush_color, (x, y, width, height))
          elif current_tool == "brush":
             mouse_pressed = pygame.mouse.get_pressed()
             mouse_pos = pygame.mouse.get_pos() 
          elif current_tool == "clean":
             screen.fill(WHITE)          
          elif current_tool == "sqr":
            size = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
            x = min(start_pos[0], end_pos[0])
            y = min(start_pos[1], end_pos[1])
            pygame.draw.rect(screen, brush_color, (x, y, size, size))
          elif current_tool == "r_tr":
             x1, y1 = start_pos
             x2, y2 = end_pos
             pygame.draw.polygon(screen, brush_color, [(x1, y1), (x1, y2), (x2, y2)])
          elif current_tool == "eq_tr":
            x1, y1 = start_pos
            x2, y2 = end_pos
            base = abs(x2 - x1)
            height = int((math.sqrt(3) / 2) * base)
            pygame.draw.polygon(screen, brush_color, [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)])

          elif current_tool == "rhomb":
            x1, y1 = start_pos
            x2, y2 = end_pos
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            width = abs(x2 - x1) // 2
            height = abs(y2 - y1) // 2
            pygame.draw.polygon(screen, brush_color, [(cx, y1), (x2, cy), (cx, y2), (x1, cy)])

def draw_col():
    for btn in color_buttons:
        pygame.draw.rect(screen,btn["color"], btn["rect"])
        pygame.draw.rect(screen, BLACK, btn["rect"],2)
    for btn1 in shapes:
        pygame.draw.rect(screen, WHITE, btn1["var"])  # Fill shape button with white
        pygame.draw.rect(screen, BLACK, btn1["var"], 2)  # Black border
        font2 = pygame.font.SysFont("Verdana", 15)
        txt = font2.render(btn1["sh"], True, BLACK)
        screen.blit(txt, (btn1["var"].x + 2, btn1["var"].y + 5))
def draw():
  if current_tool == "brush":  
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_pressed[0]:
        pygame.draw.circle(screen,brush_color,mouse_pos,brush_size)

rect = pygame.Surface((350,50))  #For score frame
rect.fill(GREEN)

def show_sc():
    global brush_color,brush_size
    screen.blit(rect,(30,55))
    font1 = pygame.font.SysFont('Verdana',20)
    txt = font1.render(str(f'Your current brush size : {brush_size}'), True, WHITE)
    screen.blit(txt, (30,55))


screen.fill(WHITE)
while True:
    handle_events()
    show_sc()
    draw()
    draw_col()

    pygame.display.flip()
    clock.tick(60)


