from os import supports_bytes_environ, unsetenv
import random
from re import S
import re
import sys
from flask.templating import render_template
from flask import abort, Blueprint, Markup, request

from .commons.icons import get_icon_pngs, silhouette_pixel_art
import sys
class Cell:
    
    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        # Initialize the cell at (x,y) surrounded by walls

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.traversed = False

    def has_all_walls(self):
        # Check if cell has all of its walls

        return all(self.walls.values())

    def remove_wall(self, other, wall):
        # Knock down the wall between cells self and other.

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, grid):
        """Initialize the maze grid.
        The maze consists of nx * ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        # shaped_map = [
        # [1,1,1,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
        # [0,0,0,1,1,1,1,1,0,1,1,1,1,1,1],0, 0
        # [0,0,0,1,1,1,1,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,0,0,1,0,0,0],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,1],
        # [0,0,0,1,1,1,0,0,0,1,1,1,1,1,0]
        # ]

        shaped_map = grid


        # print(image.tolist(), file=sys.stderr)
        # print(shaped_map, file=sys.stderr)
        #shaped_map = image.tolist()

        self.nx, self.ny = len(shaped_map), len(shaped_map[0])
        #self.nx, self.ny = nx, ny
        self.ix, self.iy = -1,-1
        self.end_x, self.end_y = -1,-1
        self.maze_map = [[Cell(x, y) for y in range(self.ny)] for x in range(self.nx)]
        
       
        for x in range(self.nx):
            for y in range(self.ny):
                # Sets cell to be out of bounds if not part of the shaped map
                inBounds = shaped_map[x][y]
                self.maze_map[y][x].inBounds = inBounds
                if inBounds:
                    if(self.ix == -1):
                        self.ix, self.iy = x,y
                    self.end_x, self.end_y = x, y

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

        solution_path = self.solve_maze()
        self.cell_at(self.ix, self.iy).walls['N'] = False
        self.cell_at(self.end_x, self.end_y).walls['S'] = False

        print(self.cell_at(self.end_x, self.end_y).walls['S'])
       
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

        svg +=('line.sol {')
        svg +=('    stroke: #FF0000;\n    stroke-linecap: square;')
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


        sol = svg    
        #Draw solution
        for i in range(len(solution_path) - 1):
           
            x_cell_1, y_cell_1 = solution_path[i].x, solution_path[i].y
            x_cell_2, y_cell_2 = solution_path[i + 1].x, solution_path[i + 1].y

            x1, y1, x2, y2 = (x_cell_1 + 0.5) * scx, (y_cell_1 + 0.5) * scy, (x_cell_2 + 0.5) * scx, (y_cell_2 + 0.5) * scy
            sol += '<line class="sol" x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2)

        svg +=('</svg>')
        sol +=('</svg>')
        return [svg, sol]

    def find_neighbours(self, cell):
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
                neighbours.append((direction, neighbour))
        return neighbours

    def find_valid_neighbours(self, cell):
        """ Return an array of unvisited neighbours to cell """

        valid_neighbours = [(direction, c) for (direction, c) in self.find_neighbours(cell) if c.has_all_walls()]
        
        return valid_neighbours

    def find_traversable_neighbours(self, cell):
        """ Returns neighbours that could be part of a solution path"""
        # delta = [('W', (-1, 0)),
        #          ('E', (1, 0)),
        #          ('S', (0, 1)),
        #          ('N', (0, -1))]
        # neighbours = []
        # for direction, (dx, dy) in delta:
        #     x2, y2 = cell.x + dx, cell.y + dy
        #     if (0 <= x2 < self.nx) and (0 <= y2 < self.ny) and (self.cell_at(x2, y2).inBounds):
        #         #print(f"Neighbour {x2}, {y2}")
        #         neighbour = self.cell_at(x2, y2)
        #         if (not neighbour.walls[direction])
        #         neighbours.append((direction, neighbour))
        neighbours = self.find_neighbours(cell)
        return [neighbouring_Cell for (direction, neighbouring_Cell) in neighbours if ((not cell.walls[direction]) and (not neighbouring_Cell.traversed))]

    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)

        
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            #print(current_cell.x, current_cell.y)
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


    def solve_maze(self):
        path = [self.cell_at(self.ix, self.iy)]

        while(True):
            current_cell = path[-1]
            current_cell.traversed = True
            # Break if found the last cell
            if (current_cell.x == self.end_x and current_cell.y == self.end_y):
                break

            #unvisited = [cell for cell in self.find_traversable_neighbours(current_cell) if not cell.traversed] 
            unvisited = self.find_traversable_neighbours(current_cell)
            if (unvisited):
                path.append(unvisited[0])
            else:
                path.pop()

        return path

bp = Blueprint("maze", __name__, url_prefix="/activities/maze")

@bp.route("/state", methods=["POST"])
def get_state():
  """Returns internal maze state from provided options"""

  body = request.get_json()
  print(body, file=sys.stderr)
  grid_width, grid_height = 30,30
  
  if "width" in body:
      grid_width = int(body["width"])
      grid_height = int(body["height"])
  
  grid = [[False for i in range(grid_width)] for j in range(grid_height)]

  if "grid" in body:
      grid = body["grid"]

  
      

  print(grid_width, file=sys.stderr)
  print(grid_height, file=sys.stderr)
  print(grid, file=sys.stderr)

  maze_svgs = generate_maze(grid_width, grid_height, grid)
  #maze_svgs = generate_shaped_maze(grid_width, grid_height, theme)
  return {
    "description": ["Complete the maze."],
    "svg": maze_svgs[0],
    "sol": maze_svgs[1]
  }

def generate_shaped_maze(grid_width, grid_height, theme):
    """Returns internal nonogram state from provided options"""
    
    # grid_width = int(request.args.get("width", 15))
    # grid_height = int(request.args.get("height", 15))
    #theme = request.args.get("theme")

    images = get_icon_pngs(theme)
    if not images:
        abort(404, f"No suitable images found for theme '{theme}'")
    image_bytes = random.choice(images)
    image = silhouette_pixel_art(image_bytes, (grid_width, grid_height))

    maze = Maze(grid_width, grid_height, image, 0, 0)
    maze.make_maze()
    res = maze.generate_svg()
    return res

def generate_maze(grid_width, grid_height, grid):
    maze = Maze(grid_width, grid_height, grid)
    maze.make_maze()
    res = maze.generate_svg()
    return res

def generate_html(svg, html_data):
    print(html_data)
    print(svg)
    return render_template("maze.html", title=html_data["title"], instructions=html_data["instructions"], svg=Markup(svg))



if __name__ == '__main__':
    res = generate_maze(15,15)
    print(res[0])

    #print()
    