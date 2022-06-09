import pygame


WIDTH, HEIGHT = 800, 620

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
PSEUDO_WHITE = (240, 240, 240)


# Cell class
class Cell:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.value = 0
        self.rect = pygame.Rect([self.x*w, self.y*h, w, h])

    def set_neighbours(self, c_array):
        self.neighbour_values = []
        for j in range(self.y-1, self.y+2):
            for i in range(self.x-1, self.x+2):
                if (self.x != i or self.y != j) and 0 <= i < len(c_array[0]) and 0 <= j < len(c_array):
                    self.neighbour_values.append(c_array[j][i].value)
    
    def set_value(self):
        nb1 = self.neighbour_values.count(1)
        if self.value == 0:
            if nb1 == 3:
                self.value = 1
        elif self.value == 1:
            if nb1 < 2 or 4 <= nb1:
                self.value = 0

    def switch(self):
        # If 1 -> 0; 0 -> 1
        self.value = int(not self.value)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK if self.value else WHITE, self.rect)


# Cell Grid
class CellGrid:
    def __init__(self, cell_size):
        self.list = [[Cell(i, j, HEIGHT/cell_size, HEIGHT/cell_size) for i in range(cell_size)] for j in range(cell_size)]

    def handle_mouse_down(self, ms_x, ms_y):
        for j in range(len(self.list)):
            if self.list[j][0].rect.y <= ms_y <= self.list[j][0].rect.y + self.list[j][0].rect.h:
                y = j
                break

        for i in range(len(self.list[0])):
            if self.list[y][i].rect.x <= ms_x <= self.list[y][i].rect.x + self.list[y][i].rect.w:
                x = i
                break

        self.list[y][x].switch()

    def draw(self, screen):
        for j in range(len(self.list)):
            for i in range(len(self.list[0])):
                self.list[j][i].draw(screen)
