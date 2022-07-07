from collections import deque

from pyglet import window, app, clock
from pyglet.graphics import Batch

from config import width, height, fps, rows, cols
from cell import Cell


window = window.Window(width=width, height=height)

grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
starting_cell = grid[0][0]
starting_cell.visited = True
stack = deque([starting_cell])
# starting_cell.recursive_backtrack(grid)


@window.event
def on_draw():
    window.clear()
    batch = Batch()
    to_draw = []
    for row in grid:
        for cell in row:
            to_draw.extend(cell.draw(batch))
    batch.draw()


def update(dt):
    global stack
    if not stack:
        return
    stack.extend(stack.pop().iterative_backtrack(grid))


clock.schedule_interval(update, 1 / fps)

if __name__ == "__main__":
    app.run()
