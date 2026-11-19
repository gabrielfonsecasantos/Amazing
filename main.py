from maze import MazeGenerator

def config_parser(file_path: str) -> dict:
  config: dict = {}
  mandatory_keys = {
    "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"
                    }
  keys_found: set = set()

  try:
    with open(file_path, "r", encoding="utf-8") as file:
      for line_num, line in enumerate(file, 1):
        line = line.strip()

        if not line or line.startswith("#"):
          continue
        if "=" not in line:
          raise ValueError(f"Error on line {line_num}: invalid format '{line}'. Use KEY-")
        parameters: list[str] = line.split("=")
        key: str = parameters[0].strip().upper()
        value: str = parameters[1].strip()
        if key == "WIDTH":
          try:
            config[key] = int(value)
          except ValueError:
            print(f"Error on line '{line_num}': Invalid value for parameter 'WIDTH': {value}.")
        elif key == "HEIGHT":
          try:
            config[key] = int(value)
          except ValueError:
            print(f"Error on line '{line_num}': Invalid value for parameter 'HEIGHT': {value}.")
        elif key in ("ENTRY", "EXIT"):
          try:
            x, y = value.split(",")
            config[key] = (int(x.strip()), int(y.strip()))
          except ValueError:
            print(f"Error on line '{line_num}': Invalid value for entry or exit coordenates: {x}, {y}")
        elif key == "OUTPUT_FILE":
            config[key] = value
        elif key == "PERFECT":
          try:
            if value.capitalize() == "True":
              config[key] = True
            elif value.capitalize() == "False":
              config[key] = False
          except ValueError:
            print(f"Error on line '{line_num}': Invalid boolean value '{value}'. Try 'True' or 'False'.")
        elif key == "SEED":
          try:
            if value.capitalize() == "None":
              config[key] = None
            else:
              config[key] = int(value)
          except ValueError:
            print(f"Error on line '{line_num}': Invalid value for seed '{value}'. Try a number or 'None'.")
        keys_found.add(key)
      missing_keys = mandatory_keys - keys_found
      if missing_keys:
        raise ValueError(f"Error: 'config.txt' file is incomplete. Missing keys: {missing_keys}")
  except FileNotFoundError:
    raise FileNotFoundError(f"Config file '{file_path}' was not found.")
  
  return config


if __name__ == "__main__":
  try:
    config = config_parser("/home/gabriel/42SP/Python/Amazing/config.txt")
  except FileNotFoundError as e:
    print(f"Error reading config file: {e}.")

  maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], config["SEED"], config["ENTRY"], config["EXIT"])
  maze.draw_42_pattern()
  grid = maze.maze_dfs()
  rendered_maze = maze.rendering_maze()
  print(rendered_maze)  

  