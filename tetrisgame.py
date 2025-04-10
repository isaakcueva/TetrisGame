import pygame
import random

pygame.init()

# Constantes
block_size = 30
block_width = 10
block_height = 20
screen_width = block_width * block_size + 150  # Espacio adicional para info
screen_height = block_height * block_size

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
blue = (0, 0, 255)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 128, 0)
purple = (128, 0, 128)
red = (255, 0, 0)
gray = (128, 128, 128)

# Formas de las piezas
Shapes = [
    [[1, 1, 1, 1]],              # I
    [[1, 0, 0], [1, 1, 1]],      # J
    [[0, 0, 1], [1, 1, 1]],      # L
    [[1, 1], [1, 1]],            # O
    [[0, 1, 1], [1, 1, 0]],      # S
    [[0, 1, 0], [1, 1, 1]],      # T
    [[1, 1, 0], [0, 1, 1]]       # Z
]

Colors = [cyan, blue, orange, yellow, green, purple, red]


class Tetromino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(Shapes) - 1)
        self.shape = [row[:] for row in Shapes[self.shape_idx]]
        self.color = Colors[self.shape_idx]
        self.x = block_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape))] 
                      for x in range(len(self.shape[0]) - 1, -1, -1)]


class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.grid = [[black for _ in range(block_width)] for _ in range(block_height)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500  # milisegundos

    def valid_move(self, piece, x, y):
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j]:
                    if (x + j < 0 or x + j >= block_width or
                        y + i >= block_height or
                        (y + i >= 0 and self.grid[y + i][x + j] != black)):
                        return False
        return True

    def lock_piece(self):
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    if self.current_piece.y + i < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

        if not self.game_over:
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = Tetromino()

        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for i in range(block_height):
            if all(cell != black for cell in self.grid[i]):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [black for _ in range(block_width)])
        if lines_cleared:
            self.score += 100 * lines_cleared

    def draw_grid(self):
        for i in range(block_height):
            for j in range(block_width):
                pygame.draw.rect(self.screen, self.grid[i][j],
                                 (j * block_size, i * block_size, block_size, block_size))
                pygame.draw.rect(self.screen, gray,
                                 (j * block_size, i * block_size, block_size, block_size), 1)

        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    pygame.draw.rect(
                        self.screen, self.current_piece.color,
                        ((self.current_piece.x + j) * block_size,
                         (self.current_piece.y + i) * block_size,
                         block_size, block_size)
                    )

    def draw_next_piece(self):
        label = self.font.render('Next:', True, white)
        self.screen.blit(label, (block_width * block_size + 20, 60))

        for i in range(len(self.next_piece.shape)):
            for j in range(len(self.next_piece.shape[i])):
                if self.next_piece.shape[i][j]:
                    pygame.draw.rect(
                        self.screen, self.next_piece.color,
                        (block_width * block_size + 20 + j * block_size,
                         100 + i * block_size,
                         block_size, block_size)
                    )

    def draw_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, white)
        self.screen.blit(score_text, (block_width * block_size + 20, 10))

    def draw_game_over(self):
        game_over_text = self.font.render('GAME OVER', True, white)
        score_text = self.font.render(f'Your Score: {self.score}', True, white)  
        restart_text = self.font.render('Press R to Restart', True, white)
        
    
        self.screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 40))
        self.screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 60))  
        self.screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 20))
        


    def run(self):
        running = True
        while running:
            self.screen.fill(black)
            time_passed = self.clock.tick(60)
            self.fall_time += time_passed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece.x - 1, self.current_piece.y):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                            self.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        original_shape = self.current_piece.shape
                        self.current_piece.rotate()
                        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
                            self.current_piece.shape = original_shape
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            if not self.game_over:
                if self.fall_time > self.fall_speed:
                    self.fall_time = 0
                    if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                        self.current_piece.y += 1
                    else:
                        self.lock_piece()

                self.draw_grid()
                self.draw_score()
                self.draw_next_piece()
            else:
                self.draw_game_over()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
