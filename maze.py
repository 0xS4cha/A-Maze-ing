#!/usr/bin/env python3

class ConfigException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Config:
    @staticmethod
    def get_error_line_format(i: int, config_path: str) -> str:
        return f"\tFile \"{config_path}\", line {i}\n"

    def __init__(self, config_path: str) -> None:
        self.WIDTH = 0
        self.HEIGHT = 0
        self.ENTRY = [0, 0]
        self.EXIT = [0, 0]
        self.OUTPUT_FILE = ""
        self.PERFECT = False

        with open(config_path, "r") as f:
            for i, line in enumerate(f.readlines()):
                if line.strip().startswith("#"):
                    continue # skip comments
                separator_idx = line.find("=")
                if separator_idx == -1:
                    raise ConfigException(f"Entry is not a definition: {line}.\n{self.get_error_line_format(i+1, config_path)}")
                left_arg = line[:separator_idx].strip()
                right_arg = line[separator_idx+1:].strip()
                try:
                    if left_arg == "WIDTH" and int(right_arg) > 0:
                        self.WIDTH = int(right_arg)
                    elif left_arg == "HEIGHT" and int(right_arg) > 0:
                        self.HEIGHT = int(right_arg)
                    elif (left_arg == "ENTRY" or left_arg == "EXIT") and right_arg.find(",") != -1:
                        entry = right_arg.split(",")
                        if (len(entry) != 2):
                            raise
                        if left_arg == "ENTRY":
                            self.ENTRY[0] = entry[0].strip()
                            self.ENTRY[1] = entry[1].strip()
                        else:
                            self.EXIT[0] = entry[0].strip()
                            self.EXIT[1] = entry[1].strip()
                    elif left_arg == "OUTPUT_FILE":
                        self.OUTPUT_FILE = right_arg
                    elif left_arg == "PERFECT":
                        self.PERFECT = right_arg
                    else:
                        raise ValueError(f"Unknown entry: {line}.")
                except ValueError as e:
                    raise ConfigException(f"Invalid config entry: {e.args[0]}.\n{self.get_error_line_format(i+1, config_path)}")

FULL_CHAR = '█'
EMPTY_CHAR = ' '

def print_maze(maze: list[list[str]]):
    for line in maze:
        print("".join(line))

def generate_maze(config: Config):
    maze = [[EMPTY_CHAR] * config.WIDTH for _ in range(config.HEIGHT)]
    for i in range(config.HEIGHT):
        maze[i][i] = FULL_CHAR
    print_maze(maze)

def main():
    config = Config("./config.txt")
    generate_maze(config)

if __name__ == "__main__":
	main()