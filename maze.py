import random


class MazeGenerator:
  N: int = 1 #(0001)
  E: int = 2 #(0010)
  S: int = 4 #(0100)
  W: int = 8 #(1000)

  def __init__(self, width: int = 5, height: int = 5, seed: int | None = None) -> None:
          self.width: int = width
          self.height: int = height
          self.random_gen = random.Random(seed)
          
          self.DX: dict[int, int] = {self.N: 0, self.E: 1, self.S: 0, self.W: -1}
          self.DY: dict[int, int] = {self.N: -1, self.E: 0, self.S: 1, self.W: 0}
          self.OPPOSITE: dict[int, int] = {self.N: self.S, self.E: self.W, self.S: self.N, self.W: self.E}

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

  def radar_for_unvisited(self, currentx: int, currenty: int ) -> list[tuple[int, int, int]]:
    unvisited: list[tuple[int, int, int]] = []
    for direction in (self.N, self.E, self.S, self.W):
      nextx: int = currentx + self.DX[direction]
      nexty: int = currenty + self.DY[direction]
      if 0 <= nextx < self.width and 0 <= nexty < self.height and not self.visited[nexty][nextx]:
        unvisited.append((direction, nextx, nexty))
    return unvisited
      
  def maze_dfs(self) -> list[list[int]]:
    maze = self.maze_creator()

    currentx: int = 0
    currenty: int = 0
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

  def rendering_maze(self) -> str:
    result: str = ""
    lines: list = ["+" + "---+" * self.width]

    for y in range(self.height):
      row = ["|"]
      for x in range(self.width):
        cell: int = self.grid[y][x]
        content: str = "   "
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
  maze = MazeGenerator(20,20,seed=42)
  my_maze = maze.maze_dfs()
  print("matriz final:")
  for line in my_maze:
    print(line)

  
