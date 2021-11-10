import random
from re import S

from flask.templating import render_template
from flask import Blueprint, Markup, request
class Cell:
    
    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        # Initialize the cell at (x,y) surrounded by walls

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        # Check if cell has all of its walls

        return all(self.walls.values())

    def remove_wall(self, other, wall):
        # Knock down the wall between cells self and other.

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx * ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        shaped_map = [
        [1,1,1,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,0,0,1,1,1,1,1,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,1,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1]
        ]

        self.nx, self.ny = len(shaped_map), len(shaped_map[0])
        #self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]
        
       
        for x in range(self.nx):
            for y in range(self.ny):
                # Sets cell to be out of bounds if not part of the shaped map
                self.maze_map[y][x].inBounds =  shaped_map[x][y] == 1

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze_map[x][y]

    def __str__(self):
        """Return a string representation of the maze."""

        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def generate_svg(self) -> str:
        """Generate a svg of the maze"""

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        svg = ""
    
       
        # SVG preamble and styles.
        # svg +='<?xml version="1.0" encoding="utf-8"?>'
        svg +=('<svg xmlns="http://www.w3.org/2000/svg"')
        svg +=('    xmlns:xlink="http://www.w3.org/1999/xlink"')
        svg +=('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                .format(width + 2 * padding, height + 2 * padding,
                        -padding, -padding, width + 2 * padding, height + 2 * padding))
        svg +=('<defs>\n<style type="text/css"><![CDATA[')
        svg +=('line {')
        svg +=('    stroke: #000000;\n    stroke-linecap: square;')
        svg +=('    stroke-width: 5;\n}')
        svg +=(']]></style>\n</defs>')
        # Draw the "South" and "East" walls of each cell, if present (these
        # are the "North" and "West" walls of a neighbouring cell in
        # general).
        for x in range(self.nx):
            for y in range(self.ny):
                if (self.cell_at(x,y).inBounds):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        
                        # Write a wall to svg 
                        svg += '<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        # Write a wall to svg
                        svg += '<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2)

                    if self.cell_at(x, y).walls['N']:
                        x1, y1, x2, y2 = x * scx, y * scy, (x + 1) * scx, y * scy
                        # Write a wall to svg
                        svg += '<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2)  

                    if self.cell_at(x, y).walls['W']:
                        x1, y1, x2, y2 = x * scx, y * scy, x * scx, (y + 1) * scy
                        # Write a wall to svg
                        svg += '<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2)        

        # Draw the North and West maze border
        # svg +=('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width))
        # svg +=('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height))
        svg +=('</svg>')

        return svg

    def find_valid_neighbours(self, cell):
        """ Return an array of unvisited neighbours to cell """

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny) and (self.cell_at(x2, y2).inBounds):
                #print(f"Neighbour {x2}, {y2}")
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        
        # Total number of visited cells during maze construction.
        nv = 1

        print(current_cell)
        while nv < n:
            print(current_cell.x, current_cell.y)
            if (current_cell.inBounds):
            
                neighbours = self.find_valid_neighbours(current_cell)

                if not neighbours:
                    # We've reached a dead end: backtrack.
                    if cell_stack:
                        current_cell = cell_stack.pop() 
                    else:
                        break
                    continue

                # Choose a random neighbouring cell and move to it.
                direction, next_cell = random.choice(neighbours)
                current_cell.remove_wall(next_cell, direction)
                cell_stack.append(current_cell)
                current_cell = next_cell
            nv += 1


bp = Blueprint("maze", __name__, url_prefix="/activities/maze")

@bp.route("/state")
def get_state():
  """Returns internal maze state from provided options"""
  grid_width = int(request.args.get("width", 15))
  grid_height = int(request.args.get("height", 15))

  return {
    "description": ["Complete the maze."],
    "svg": generate_maze(grid_width, grid_height)
  }

def generate_maze(grid_width, grid_height):
    maze = Maze(grid_width, grid_height, 0, 0)
    maze.make_maze()
    svg = maze.generate_svg()
    return svg

def generate_html(svg, html_data):
    print(html_data)
    print(svg)
    return render_template("maze.html", title=html_data["title"], instructions=html_data["instructions"], svg=Markup(svg))



if __name__ == '__main__':
    generate_maze(15,15)

    #print()
    