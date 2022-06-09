# Conway's Game Of Life; Same structure & logic as Shortest-Path Finding Project
import pygame
from settings import *
pygame.init()


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game Of Life")


# cell array
cell_size = 100


# Game class
class Game:
    def __init__(self):
        self.is_evolving = False
        self.can_clear = True
        self.buttons = {}

        self.cells_grid = CellGrid(cell_size)
        self.last_values_list = []
        for j in range(len(self.cells_grid.list)):
            self.last_values_list.append([])
            for i in range(len(self.cells_grid.list[0])):
                self.last_values_list[j].append(self.cells_grid.list[j][i].value)

    def draw_welcome(self):
        screen.fill(WHITE)

        font = pygame.font.SysFont("Corbel", 60)
        wlcm = font.render("WELCOME TO", True, BLACK)
        prjct_name = font.render(pygame.display.get_caption()[0], True, CYAN)
        project = font.render("PROJECT", True, BLACK)

        for num, txt in enumerate([wlcm, prjct_name, project]):
            screen.blit(txt, ((WIDTH-txt.get_width())/2, (HEIGHT/4)*(num+1)))

        pygame.display.flip()

    def draw_doc(self):
        screen.fill(WHITE)

        font = pygame.font.SysFont("Corbel", 18)
        lines = ["The Game of Life, a cellular automaton devised by the British mathematician John H. Conway in 1970.",
                "It's a zero-player game, its evolution is determined by its initial state, requiring no further input.",
                "You interact with the Game of Life by creating an initial configuration and observing how it evolves.",
                "The universe of the Game of Life is a two-dimensional orthogonal grid of square cells.",
                "Each of the cells is in one of two possible states, live or dead (or populated and unpopulated)",
                "Each one interacts with its eight neighbours, cells that are horizontally, vertically, or diagonally adjacent.",
                '',
                "At each step in time, the following transitions occur:",
                "-Any live cell with fewer than two live neighbours dies, as if by underpopulation.",
                "-Any live cell with two or three live neighbours lives on to the next generation.",
                "-Any live cell with more than three live neighbours dies, as if by overpopulation.",
                "-Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."]

        for num, line in enumerate(lines):
            txt = font.render(line, True, BLACK)
            screen.blit(txt, ((WIDTH-txt.get_width())/2, (HEIGHT/(len(lines)+1))*(num+1)))

        pygame.display.flip()

    def do_buttons(self):
        btn_names = ["Stop"] if self.is_evolving else ["Start"]
        btn_names.append("Clear") if self.can_clear else btn_names.append("Reset")

        self.buttons = {}

        font = pygame.font.SysFont("Corbel", 40)
        for num, btn_name in enumerate(btn_names):
            txt = font.render(btn_name, True, BLACK)
            btn_rect = pygame.Rect([HEIGHT, HEIGHT/(len(btn_names)+1)*(num+1), WIDTH-HEIGHT, HEIGHT/(len(btn_names)+2)])
            btn_rect.y -= btn_rect.h/2
            self.buttons[btn_name] = btn_rect

            pygame.draw.rect(screen, BLACK, btn_rect, width=1)
            screen.blit(txt, (btn_rect.centerx-txt.get_width()/2, btn_rect.y+btn_rect.h/2-txt.get_height()/2))

    def button_pressing(self, ms_x, ms_y):
        for btn_name in self.buttons:
            btn_rect = self.buttons[btn_name]
            if btn_rect.collidepoint(ms_x, ms_y):
                if btn_name == "Start":
                    self.is_evolving = True
                    self.can_clear = False
                    # Get values
                    for j in range(len(self.cells_grid.list)):
                        for i in range(len(self.cells_grid.list[0])):
                            self.last_values_list[j][i] = self.cells_grid.list[j][i].value

                elif btn_name == "Stop":
                    self.is_evolving = False
                elif btn_name == "Clear":
                    self.cells_grid = CellGrid(cell_size)
                    self.is_evolving = False
                elif btn_name == "Reset":
                    self.can_clear = True if not self.is_evolving else self.can_clear
                    # Set values
                    for j in range(len(self.cells_grid.list)):
                        for i in range(len(self.cells_grid.list[0])):
                            self.cells_grid.list[j][i].value = self.last_values_list[j][i]

    def draw(self):
        screen.fill(PSEUDO_WHITE)

        # Draw cells
        self.cells_grid.draw(screen)

        self.do_buttons()

        pygame.display.flip()

    def run(self):
        is_started = False
        is_reading_doc = False
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
                    is_started = True
                    is_reading_doc = True
                elif event.type == pygame.MOUSEBUTTONDOWN and is_reading_doc:
                    is_reading_doc = False
                elif pygame.mouse.get_pressed()[0]:  # For long pressing
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= HEIGHT:
                        self.cells_grid.handle_mouse_down(mouse_x, mouse_y)
                    elif event.type == pygame.MOUSEBUTTONDOWN:  # Unique press
                        self.button_pressing(mouse_x, mouse_y)

            if not is_started:
                self.draw_welcome()
                continue
            if is_reading_doc:
                self.draw_doc()
                continue

            self.draw()

            if self.is_evolving:
                # Set neighbours
                for j in range(cell_size):
                    for i in range(cell_size):
                        self.cells_grid.list[j][i].set_neighbours(self.cells_grid.list)

                # Set values
                for j in range(cell_size):
                    for i in range(cell_size):
                        self.cells_grid.list[j][i].set_value()

game = Game()
game.run()


# Pretty simple; ... Relatively speaking
# Lesson Learnt: Never give up on a project idea, As long as you've set the logic, you can do it.
# The 9/6/2022, at 11:48PM
