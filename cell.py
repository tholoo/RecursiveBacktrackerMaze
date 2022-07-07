import random

from pyglet.shapes import Line, Rectangle, Circle

from config import cell_size, cols, rows


class Cell:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.x, self.y = self.col * cell_size, self.row * cell_size
        self.walls = [True, True, True, True]  # Up, Right, Down, Left
        self.wall_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
        self.color = (255, 255, 255)
        self.visited = False
        self.mode = "NORMAL"

    def valid_dirs(self):
        dirs = []
        if self.row > 0:
            dirs.append(0)
        if self.row < rows - 1:
            dirs.append(2)
        if self.col > 0:
            dirs.append(3)
        if self.col < cols - 1:
            dirs.append(1)
        return dirs

    def get_neighbor(self, grid, direction):
        row, col = self.wall_dirs[direction]
        return grid[self.row + row][self.col + col]

    def recursive_backtrack(self, grid):
        self.visited = True
        valid_dirs = self.valid_dirs()
        random.shuffle(valid_dirs)
        for direction in valid_dirs:
            neighbor = self.get_neighbor(grid, direction)
            if neighbor.visited:
                continue
            self.walls[direction] = False
            neighbor.walls[(direction + 2) % 4] = False
            neighbor.recursive_backtrack(grid)

    def iterative_backtrack(self, grid):
        self.mode = "NORMAL"
        valid_dirs = self.valid_dirs()
        neighbor_plus_dir = [(self.get_neighbor(grid, direction), direction) for direction in valid_dirs]
        unvisited_neighbors = [(neighbor, direction) for neighbor, direction in neighbor_plus_dir if
                               not neighbor.visited]
        if not unvisited_neighbors:
            return ()
        neighbor, direction = random.choice(unvisited_neighbors)
        self.mode = "HIGHLIGHT"
        self.walls[direction] = False
        neighbor.walls[(direction + 2) % 4] = False
        neighbor.visited = True
        neighbor.mode = "CURRENT"
        return self, neighbor

    def draw_line(self, pos, batch, batch_list):
        x1, y1, x2, y2 = pos
        batch_list.append(
            Line(self.x + x1, self.y + y1, self.x + x2, self.y + y2, color=self.color, width=2, batch=batch))

    def draw_rect(self, x, y, offset_w, offset_h, color, batch, batch_list):
        batch_list.append(
            Rectangle(self.x + x, self.y + y, cell_size - offset_w, cell_size - offset_h, color=color, batch=batch))

    def draw_circle(self, r, color, batch, batch_list):
        batch_list.append(Circle(self.x + cell_size / 2, self.y + cell_size / 2, r, color=color, batch=batch))

    def draw(self, batch):
        batch_list = []

        if self.visited:
            self.draw_rect(0, 0, 0, 0, (25, 25, 50), batch, batch_list)
            # Up
            if self.walls[0]:
                self.draw_line((0, 0, cell_size, 0), batch, batch_list)
            # Right
            if self.walls[1]:
                self.draw_line((cell_size, 0, cell_size, cell_size), batch, batch_list)
            # Down
            if self.walls[2]:
                self.draw_line((cell_size, cell_size, 0, cell_size), batch, batch_list)
            # Left
            if self.walls[3]:
                self.draw_line((0, cell_size, 0, 0), batch, batch_list)

            if self.mode == "CURRENT":
                margin = cell_size / 4
                self.draw_rect(margin, margin, margin * 2, margin * 2, (0, 255, 0), batch, batch_list)

            elif self.mode == "HIGHLIGHT":
                margin = cell_size / 2.5
                self.draw_circle((cell_size - margin * 2) * 0.6, (50, 50, 50), batch, batch_list)

        return batch_list
