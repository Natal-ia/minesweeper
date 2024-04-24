import sys
import heapq
from MineSweeperBoard import MineSweeperBoard

class Player_H1:

    def __init__(self, w, h, m):
        self.m_Width = w
        self.m_Height = h
        self.m_NumberOfMines = m
        self.m_Mines = [[False for j in range(h)] for i in range(w)]
        self.m_Count = [[9 for j in range(h)] for i in range(w)]
        self.m_Probabilities = [(float(m) / (w * h), (i, j)) for i in range(w) for j in range(h)]
        heapq.heapify(self.m_Probabilities)

    def next_play(self):
        while self.m_Probabilities:
            p, (i, j) = heapq.heappop(self.m_Probabilities)
            if not self.m_Mines[i][j] and self.m_Count[i][j] == 9:
                has_unmarked_neighbor = False
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x != 0 or y != 0:
                            nx = i + x
                            ny = j + y
                            if 0 <= nx < self.m_Width and 0 <= ny < self.m_Height:
                                if self.m_Count[nx][ny] == 9:
                                    has_unmarked_neighbor = True
                                    break
                    if has_unmarked_neighbor:
                        break
                if has_unmarked_neighbor and self.m_Count[i][j] > 0:
                    return (i, j)
                elif not has_unmarked_neighbor:
                    return (i, j)
                # Si la celda contiene una mina, establecer su probabilidad en 1 y continuar
                else:
                    self.m_Probabilities.append((1.0, (i, j)))
        return None

    def update_cell(self, i, j):
        if self.m_Count[i][j] == 1:
            # Verificar si la celda está en una esquina y solo hay una celda no marcada en el vecindario
            corner_cells = [(0, 0), (0, self.m_Height - 1), (self.m_Width - 1, 0), (self.m_Width - 1, self.m_Height - 1)]
            if (i, j) in corner_cells:
                unmarked_neighbors = 0
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        nx = i + x
                        ny = j + y
                        if (x != 0 or y != 0) and 0 <= nx < self.m_Width and 0 <= ny < self.m_Height:
                            if self.m_Count[nx][ny] == 9:
                                unmarked_neighbors += 1
                if unmarked_neighbors == 1:
                    for x in [-1, 0, 1]:
                        for y in [-1, 0, 1]:
                            nx = i + x
                            ny = j + y
                            if (x != 0 or y != 0) and 0 <= nx < self.m_Width and 0 <= ny < self.m_Height:
                                if self.m_Count[nx][ny] == 9:
                                    self.m_Mines[nx][ny] = True
                                    self.m_NumberOfMines -= 1
                                    return
        elif 1 < self.m_Count[i][j] < 9:
            # Verificar si hay x celdas no marcadas adyacentes y el número de minas restantes es igual a x
            unmarked_neighbors = []
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    nx = i + x
                    ny = j + y
                    if (x != 0 or y != 0) and 0 <= nx < self.m_Width and 0 <= ny < self.m_Height:
                        if self.m_Count[nx][ny] == 9:
                            unmarked_neighbors.append((nx, ny))
            if len(unmarked_neighbors) == self.m_Count[i][j]:
                for nx, ny in unmarked_neighbors:
                    self.m_Mines[nx][ny] = True
                    self.m_NumberOfMines -= 1
                    return
        # Actualización de celdas como antes
        m = 9
        n = 8
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    nx = i + x
                    ny = j + y
                    if 0 <= nx < self.m_Width and 0 <= ny < self.m_Height:
                        if self.m_Count[nx][ny] < m:
                            m = self.m_Count[nx][ny]
                        if self.m_Count[nx][ny] < 9:
                            n -= 1
        if n > 0:
            p = float(m) / float(n)
        else:
            p = float(0)
        if p < 1:
            heapq.heappush(self.m_Probabilities, (p, (i, j)))
        else:
            self.m_Mines[i][j] = True
            self.m_NumberOfMines -= 1

    def update(self, n):
        if n < 9:
            (i, j) = self.m_Play
            self.m_Count[i][j] = n
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:
                        nx = i + x
                        ny = j + y
                        if 0 <= nx < self.m_Width and 0 <= ny < self.m_Height:
                            self.update_cell(nx, ny)

    def next_play_with_probabilities(self):
        min_prob = 1.1
        min_cell = None
        for prob, (i, j) in self.m_Probabilities:
            if not self.m_Mines[i][j] and self.m_Count[i][j] == 9:
                if prob < min_prob:
                    min_prob = prob
                    min_cell = (i, j)
        return min_cell

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3", sys.argv[0], "width height mines")
        sys.exit(1)
    w = int(sys.argv[1])
    h = int(sys.argv[2])
    m = int(sys.argv[3])
    board = MineSweeperBoard(w, h, m)

    player = Player_H1(w, h, m)

    while not board.have_won() and not board.have_lose():
        next_play = player.next_play()
        if next_play is not None:
            (i, j) = next_play
            print(board)
            print("Current probabilities heap:", player.m_Probabilities)  # Imprimir el heap de probabilidades
            input('Next click on (' + chr(i + ord('A')) + ',' + chr(j + ord('A')) + ')')
            player.m_Play = (i, j)
            player.update(board.click(i, j))
        else:
            break

    print(board)
    if board.have_won():
        print("You won!")
    elif board.have_lose():
        print("You lose :-(")