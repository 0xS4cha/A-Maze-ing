from mazegen import MazeGenerator

# Use backtracking algorithm
gen = MazeGenerator(width=31, height=31, algo="backtracking")
gen.generate()
gen.solve()

# Display in a window (requires mlx installed)
gen.display_window()