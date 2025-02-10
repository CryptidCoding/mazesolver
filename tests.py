import unittest
from main import Maze, Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_small(self):
        num_cols = 5
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_large(self):
        num_cols = 20
        num_rows = 15
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_min_size(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            maze = Maze(0, 0, 0, 5, 10, 10)

    def test_maze_uneven_maze(self):
        num_cols = 50
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_invalid_cell_size(self):
        with self.assertRaises(ValueError):
            maze = Maze(0, 0, 5, 5, 0, 10)  # zero width
            maze = Maze(0, 0, 5, 5, 10, -5)  # negative height

    def test_maze_negative_start(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(-15, -15, num_rows, num_cols, 10, 10, win=None)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    @unittest.skip("Requires window implementation")
    def test_maze_negative_start_with_window(self):
        pass

    def test_maze_memory_bounds(self):
        with self.assertRaises(ValueError):
            maze = Maze(0, 0, 1000000, 1000000, 10, 10)  # Extremely large maze

    def test_maze_entrance_break(self):
        num_cols = 2
        num_rows = 2
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_entrance_and_exit()
        self.assertEqual(m1._cells[0][0].has_top_wall, False)
        self.assertEqual(m1._cells[num_cols-1][num_rows-1].has_bottom_wall, False)

    def test_reset_cells_visited(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        # Set all cells to True
        for i in range(0, num_cols):
            for j in range(0, num_rows):
                m1._cells[i][j].visited = True

        # Verify cells are True
        for i in range(0, num_cols):
            for j in range(0, num_rows):
                self.assertTrue(m1._cells[i][j].visited)

        # Reset cells
        m1._reset_cells_visited()

        # Verify all cells are False
        for i in range(0, num_cols):
            for j in range(0, num_rows):
                self.assertFalse(m1._cells[i][j].visited)

if __name__ == "__main__":
    unittest.main()
