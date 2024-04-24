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
                return (i, j)
        return None

    def update_cell(self, i, j):
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
