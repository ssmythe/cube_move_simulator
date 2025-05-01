# Cube Move Simulator

A command-line tool for parsing, visualizing, and manipulating Rubik's Cube states, built on the [magiccube](https://pypi.org/project/magiccube/) library.

## Features

- **Solved Cube Initialization**: Start with a solved cube in any notation (`-n` / `--notation-order`) and color scheme (`-c` / `--color-order`).
- **Facelet Import**: Load any 54-character facelet string (`-f` / `--facelet-notation`) in your chosen notation order.
- **Scramble Support**: Apply a sequence of scramble moves (`-s` / `--scramble`) to the solved cube before further operations.
- **Step-by-Step Moves**: Execute moves (`-m` / `--moves`) one by one, viewing the cube, edge map, and corner map after each step.
- **Edge & Corner Visualization**: Compact, readable display of all edge and corner pieces at any stage.

## Installation

```bash
# Clone this repository
git clone https://github.com/ssmythe/cube_move_simulator.git
cd cube_move_simulator

# Install runtime dependencies
pip install -r requirements.txt

# (Optional) Install development dependencies
git checkout main
pip install -r requirements-dev.txt
```

## Usage

After installation, you have two primary launch methods:

### 1. `bin/cube` shim

```bash
# Show help
./bin/cube --help

# Initialize solved cube and display state
./bin/cube

# Import a facelet string (default solved cube)
#   U:W*9, L:O*9, F:G*9, R:R*9, B:B*9, D:Y*9 becomes
#   "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY"
./bin/cube -f "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY"

# Scramble then view state
./bin/cube -s "R U R' U'"

# Scramble then apply moves interactively
./bin/cube -s "R U" -m "F R U'"
```

### 2. Direct Python call

```bash
PYTHONPATH=src python src/cms/main.py [OPTIONS]
```

## Command‑line Options

| Flag                   | Description |
|------------------------|-------------|
| `-f, --facelet-notation` | 54-character facelet string (optional) |
| `-n, --notation-order`   | Permutation of `U L F R B D` (default: `ULFRBD`) |
| `-c, --color-order`      | Permutation of `W O G R B Y` (default: `WOGRBY`) |
| `-s, --scramble`         | Space-separated scramble moves to apply first |
| `-m, --moves`            | Space-separated moves to execute step-by-step |
| `-h, --help`             | Show this help and exit |

## Development

This project uses pytest for testing and coverage reporting.

```bash
# Run tests
make test

# Coverage report
make coverage
```

## Makefile Targets

| Target       | Action                                      |
|--------------|---------------------------------------------|
| `make`      | Default → Run coverage tests                |
| `make install`   | Install runtime dependencies                |
| `make install-dev` | Install runtime + dev dependencies         |
| `make test`      | Run pytest                                 |
| `make coverage`  | Run pytest with coverage & HTML report     |
| `make run`       | Launch via `bin/cube` shim                 |
| `make code-run`  | Launch via Python module                   |
| `make code-help` | Show CLI help                              |
| `make clean`     | Remove caches and coverage artifacts       |

## Contributing

Contributions, issues, and feature requests are welcome! Please open an issue or submit a pull request.

