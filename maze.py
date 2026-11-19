import random


PATTERN_42: list[str] = [
    "#.. ###",
    "#.. ..#",
    "### ###",
    "..# #..",
    "..# ###",
]


class MazeGenerator:
    N: int = 1  # (0001)
    E: int = 2  # (0010)
    S: int = 4  # (0100)
    W: int = 8  # (1000)

    def __init__(
            self, width: int = 5, 
            height: int = 5, 
            seed: int | None = None, 
            entry: tuple[int, int] | None = None, 
            exit: tuple[int, int] | None = None
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.random_gen = random.Random(seed)
        self.entry: tuple[int, int] | None = entry
        self.exit: tuple[int, int] | None = exit
        self.blocked_cells: set[tuple[int, int]] = set()

        self.DX: dict[int, int] = {self.N: 0, self.E: 1, self.S: 0, self.W: -1}
        self.DY: dict[int, int] = {self.N: -1, self.E: 0, self.S: 1, self.W: 0}
        self.OPPOSITE: dict[int, int] = {
            self.N: self.S, self.E: self.W, self.S: self.N, self.W: self.E}

    grid: list[list[int]] = []
    visited: list[list[bool]] = []

    def maze_creator(self) -> list[list[int]]:
        for y in range(self.height):
            current_row: list[int] = []
            visited_row: list[bool] = []
            for x in range(self.width):
                current_row.append(15)
                visited_row.append(False)

            self.grid.append(current_row)
            self.visited.append(visited_row)
        return self.grid

    def draw_42_pattern(self) -> None:
        pattern_height: int = len(PATTERN_42)
        pattern_width: int = len(PATTERN_42[0])

        if self.height < pattern_height + 2 or self.width < pattern_width + 2:
            print("Warning: maze too small to show 42 pattern on the center.")
            return

        center_x = (self.width - pattern_width) // 2
        center_y = (self.height - pattern_height) // 2
        for y in range(pattern_height):
            for x in range(pattern_width):
                if PATTERN_42[y][x] == "#":
                    real_x = center_x + x
                    real_y = center_y + y
                    self.blocked_cells.add((real_x, real_y))

    def radar_for_unvisited(self, currentx: int, currenty: int) -> list[tuple[int, int, int]]:
        unvisited: list[tuple[int, int, int]] = []
        for direction in (self.N, self.E, self.S, self.W):
            nextx: int = currentx + self.DX[direction]
            nexty: int = currenty + self.DY[direction]
            if (
                0 <= nextx < self.width
                and 0 <= nexty < self.height
                and not self.visited[nexty][nextx]
                and (nextx, nexty) not in self.blocked_cells
            ):
                unvisited.append((direction, nextx, nexty))
        return unvisited

    def maze_dfs(self) -> list[list[int]]:
        maze = self.maze_creator()

        currentx: int = 0
        currenty: int = 0
        while (currentx, currenty) in self.blocked_cells:
            currentx += 1

        stack: list[tuple[int, int]] = []

        self.visited[currenty][currentx] = True
        stack.append((currentx, currenty))

        while len(stack) > 0:
            currentx, currenty = stack[-1]

            unvisited = self.radar_for_unvisited(currentx, currenty)

            if unvisited:
                direction, nextx, nexty = self.random_gen.choice(unvisited)
                self.grid[currenty][currentx] &= ~direction
                self.grid[nexty][nextx] &= ~self.OPPOSITE[direction]

                self.visited[nexty][nextx] = True
                stack.append((nextx, nexty))
            else:
                stack.pop()
        return maze

    def validate_coordinates(self) -> None:
      if self.entry == None or self.exit == None:
          return
      entry_x, entry_y = self.entry
      exit_x, exit_y = self.exit

      if self.entry in self.blocked_cells:
          raise ValueError(f"Error: Entry '{self.entry}' is blocked by the 42 pattern")
      elif self.exit in self.blocked_cells:
          raise ValueError(f"Error: Exit '{self.exit}' is blocked by the 42 pattern")
      elif not (0 <= entry_x < self.width and 0 <= entry_y < self.height):
          raise ValueError(f"Error: Entry '{self.entry}' out of maze limits.")
      elif not (0 <= exit_x < self.width and 0 <= exit_y < self.height):
          raise ValueError(f"Error: Exit '{self.exit}' out of maze limits.")
      elif self.entry == self.exit:
          raise ValueError(f"Error: Entry '{self.entry}' and Exit '{self.exit}' values are the same.")

    def rendering_maze(self) -> str:
        result: str = ""
        lines: list = ["+" + "---+" * self.width]
        try:
          self.validate_coordinates()
        except ValueError as e:
            error: str = str(e)
            return error
        for y in range(self.height):
            row = ["|"]
            for x in range(self.width):
                cell: int = self.grid[y][x]
                content: str = "   "
                if self.entry and (x, y) == self.entry:
                    content = " E "
                elif self.exit and (x, y) == self.exit:
                    content = " X "
                if cell & 2:
                    row.append(content + "|")
                else:
                    row.append(content + " ")
            lines.append("".join(row))
            bottom_row = ["+"]
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell & 4:
                    bottom_row.append("---+")
                else:
                    bottom_row.append("   +")
            lines.append("".join(bottom_row))
        for line in lines:
            print(line)
        return result


if __name__ == "__main__":
    maze = MazeGenerator(20, 20, seed=42)
    my_maze = maze.maze_dfs()
    print("matriz final:")
    for line in my_maze:
        print(line)
