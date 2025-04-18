import pygame
import random
import sys
import time
import psycopg2
import csv
from config1 import load1_config

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Шрифты
font = pygame.font.Font(None, 30)
large_font = pygame.font.Font(None, 50)

# Подключение к базе данных
def get_db_connection():
    config = load1_config()
    return psycopg2.connect(**config)

# Управление пользователями
class UserManager:
    @staticmethod
    def get_or_create_user(username):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Проверяем существующего пользователя
                cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                user = cur.fetchone()
                
                if user:
                    user_id = user[0]
                    # Получаем текущий уровень пользователя
                    cur.execute("""
                        SELECT MAX(level) FROM user_scores 
                        WHERE user_id = %s
                    """, (user_id,))
                    level = cur.fetchone()[0] or 1
                    return user_id, level
                else:
                    # Создаем нового пользователя
                    cur.execute(
                        "INSERT INTO users (username) VALUES (%s) RETURNING user_id",
                        (username,)
                    )
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    return user_id, 1
        finally:
            conn.close()

    @staticmethod
    def save_game_state(user_id, score, level, snake_body, direction, food_position, food_weight):
        state = {
            "snake_body": snake_body,
            "direction": direction,
            "food_position": food_position,
            "food_weight": food_weight
        }
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO user_scores (user_id, score, level, saved_state)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, score, level, json.dumps(state)))
                conn.commit()
        finally:
            conn.close()

# Уровни игры
class GameLevels:
    LEVELS = {
        1: {"speed": 10, "walls": [], "required_score": 10},
        2: {"speed": 12, "walls": [
            {"x": 200, "y": 200, "width": 400, "height": 20},
            {"x": 200, "y": 400, "width": 400, "height": 20}
        ], "required_score": 25},
        3: {"speed": 15, "walls": [
            {"x": 100, "y": 150, "width": 600, "height": 20},
            {"x": 100, "y": 450, "width": 600, "height": 20},
            {"x": 300, "y": 300, "width": 20, "height": 200}
        ], "required_score": 50}
    }

    @staticmethod
    def get_level(level_num):
        return GameLevels.LEVELS.get(level_num, GameLevels.LEVELS[1])

# Класс игры "Змейка"
class SnakeGame:
    def __init__(self, user_id, level=1):
        self.user_id = user_id
        self.level = level
        level_data = GameLevels.get_level(level)
        
        self.speed = level_data["speed"]
        self.walls = level_data["walls"]
        self.required_score = level_data["required_score"]
        
        self.snake = Snake()
        self.food = Food(self.snake.body, self.walls)
        self.score = 0
        self.paused = False
        
        # Игровое окно
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"Змейка - Уровень {level}")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")
                elif event.key == pygame.K_p:  # Пауза и сохранение
                    self.paused = not self.paused
                    if self.paused:
                        UserManager.save_game_state(
                            self.user_id, self.score, self.level,
                            self.snake.body, self.snake.direction,
                            self.food.position, self.food.weight
                        )
        return True
    
    def update(self):
        if self.paused:
            return True
        
        if not self.snake.move(self.walls):
            return False
        
        # Проверка съедания еды
        if self.snake.body[0] == self.food.position:
            self.snake.grow_snake()
            self.score += self.food.weight
            self.food = Food(self.snake.body, self.walls)
            
            # Переход на новый уровень
            if self.score >= self.required_score:
                self.level += 1
                level_data = GameLevels.get_level(self.level)
                self.speed = level_data["speed"]
                self.walls = level_data["walls"]
                self.required_score = level_data["required_score"]
                pygame.display.set_caption(f"Змейка - Уровень {self.level}")
        
        # Проверка исчезновения еды
        if self.food.should_disappear():
            self.food = Food(self.snake.body, self.walls)
        
        return True
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Рисуем стены
        for wall in self.walls:
            pygame.draw.rect(
                self.screen, GRAY,
                (wall["x"], wall["y"], wall["width"], wall["height"])
            )
        
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Рисуем счет и уровень
        score_text = font.render(f"Счет: {self.score}", True, BLACK)
        level_text = font.render(f"Уровень: {self.level}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH - 120, 10))
        
        if self.paused:
            pause_text = large_font.render("ПАУЗА - Игра сохранена", True, RED)
            self.screen.blit(
                pause_text,
                (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2)
            )
        
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            
            if not self.update():
                break
            
            self.draw()
            clock.tick(self.speed)
        
        return self.score, self.level

# Класс Змейки
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"
        self.grow = False
    
    def move(self, walls):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= CELL_SIZE
        elif self.direction == "DOWN":
            y += CELL_SIZE
        elif self.direction == "LEFT":
            x -= CELL_SIZE
        elif self.direction == "RIGHT":
            x += CELL_SIZE
        
        new_head = (x, y)
        
        # Столкновение со стенами
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return False
        
        # Столкновение с собой
        if new_head in self.body[1:]:
            return False
        
        # Проверка столкновения с препятствиями
        for wall in walls:
            wall_rect = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
            if wall_rect.collidepoint(new_head):
                return False
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def change_direction(self, new_direction):
        opposite_directions = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
    
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Класс Еды
class Food:
    def __init__(self, snake_body, walls):
        self.position = self.generate_food_position(snake_body, walls)
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = time.time()
    
    def generate_food_position(self, snake_body, walls):
        while True:
            x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            
            # Проверяем, чтобы еда не появлялась на змейке или стенах
            valid = True
            if (x, y) in snake_body:
                valid = False
            
            for wall in walls:
                wall_rect = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
                if wall_rect.collidepoint((x, y)):
                    valid = False
                    break
            
            if valid:
                return (x, y)
    
    def should_disappear(self):
        return time.time() - self.spawn_time > 5
    
    def draw(self, screen):
        colors = {1: RED, 2: YELLOW, 3: BLUE}
        pygame.draw.rect(screen, colors[self.weight], 
                         (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

# Главный игровой цикл
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Ввод имени пользователя
    username = ""
    input_active = True
    clock = pygame.time.Clock()
    
    while input_active:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        
        # Рисуем поле ввода
        prompt = large_font.render("Введите ваше имя:", True, BLACK)
        input_text = font.render(username, True, BLACK)
        instruction = font.render("Нажмите ENTER для продолжения", True, BLACK)
        
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(input_text, (SCREEN_WIDTH // 2 - input_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()
        clock.tick(30)
    
    if not username:
        username = "Гость"
    
    # Получаем или создаем пользователя
    user_id, level = UserManager.get_or_create_user(username)
    
    # Показываем уровень пользователя
    screen.fill(WHITE)
    level_text = large_font.render(f"Добро пожаловать, {username}, начинаем с Уровня {level}", True, BLACK)
    start_text = font.render("Нажмите ENTER чтобы начать игру", True, BLACK)
    
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    
    # Запускаем игру
    game = SnakeGame(user_id, level)
    final_score, final_level = game.run()
    
    # Экран завершения игры
    screen.fill(WHITE)
    game_over = large_font.render("Игра Окончена", True, RED)
    score_text = font.render(f"Финальный счет: {final_score}", True, BLACK)
    level_text = font.render(f"Достигнут Уровень: {final_level}", True, BLACK)
    exit_text = font.render("Нажмите ENTER для выхода", True, BLACK)
    
    screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    
    pygame.quit()

if __name__ == "__main__":
    main()