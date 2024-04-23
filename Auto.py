import sys
from MineSweeperBoard import MineSweeperBoard
# ANSI escape codes for color formatting
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

# Resolver el juego de buscaminas utilizando probabilidades
class MineSweeperProbabilitySolver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        while not self.board.have_won() and not self.board.have_lose():
            probabilities = self.calculate_probabilities()
            sorted_cells = sorted(probabilities, key=lambda x: x[2])

            safe_found = False
            for cell in sorted_cells:
                i, j, probability = cell
                if probability == 0:
                    self.board.click(i, j)
                    safe_found = True
                    break

            if not safe_found:
                # No safe cells found, reveal the cell with the lowest probability
                i, j, _ = sorted_cells[0]
                self.board.click(i, j)

    # Calcular probabilidad dependiendo de las celdas adyacentes
    def calculate_probabilities(self):
        probabilities = []
        for i in range(self.board.width()):
            for j in range(self.board.height()):
                if not self.board.m_Patches[i][j]:
                    probability = self.calculate_probability(i, j)
                    probabilities.append((i, j, probability))
        return probabilities

    # Calcular la probabilidad de una celda específica
    def calculate_probability(self, i, j):
        adjacent_unrevealed = 0
        adjacent_mines = self.board.m_Mines[i][j]
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = i + dx
                y = j + dy
                if 0 <= x < self.board.width() and 0 <= y < self.board.height():
                    if not self.board.m_Patches[x][y]:
                        adjacent_unrevealed += 1
        if adjacent_unrevealed == 0:
            return 0
        elif adjacent_unrevealed == adjacent_mines:
            return 1
        else:
            return adjacent_mines / adjacent_unrevealed


def smart_play(board):
    solver = MineSweeperProbabilitySolver(board)
    solver.solve()

    if board.have_won():
            print(Color.GREEN + "You won!" + Color.END)
    elif board.have_lose():
            print(Color.RED + "You lose :-(" + Color.END)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3", sys.argv[0], "width height mines")
        sys.exit(1)
    w = int(sys.argv[1])
    h = int(sys.argv[2])
    m = int(sys.argv[3])
    board = MineSweeperBoard(w, h, m)
    print("Initial board state:")
    print(board)  # Show the initial state of the board
    smart_play(board)
    print("Final board state:")
    print(board)  # Show the final state of the board
