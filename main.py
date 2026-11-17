

def config_parser(file_path: str) -> dict:
  config: dict = {}
  mandatory_keys = {
    "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
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
        
        
  except FileNotFoundError:
    raise FileNotFoundError(f"Config file '{file_path}' was not found.")
  
  return config