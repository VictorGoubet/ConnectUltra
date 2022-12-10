import time
import typing
import numpy as np



CRED = '\33[41m'
CBLUE = '\33[44m'
CYEL = '\33[36m'
CEND = '\033[0m'




class ConnectUltra():
    """Implementation of a connect4
    """

    def __init__(self) -> None:
        """Initialize the game
        """
        # max depth start at 1 and increase according to the processing time
        self.max_depth = 1
        self.max_time = 5
        self.min_time = 0.5



    def launch(self) -> None:
        """Launch an instance of the game
        """

        j = input(' Who start ?\n 1: AI \n 2: You \n\n ')
        j = 1 if j not in ["1", "2"] else int(j)

        names = ['AI', 'You']
        self.grid, list_t = np.zeros((6, 12)), []
        self.display()

        rounds, finished = 0, False
        while not finished:

            if j == 2:
                print(' It\'s your turn, where do you want to play ▶️')
                t = time.time()
                action = self.secure()
                dt = time.time() - t
            else:
                print(" AI has a deep reflexion..")
                t = time.time()
                action = self.min_max()
                dt = time.time() - t 
                list_t.append(dt)
                rounds += 1
            
            if dt < self.min_time:
                self.max_depth += 1

            if dt > self.max_time:
                self.max_depth -= 1

            print(f" 💡 {names[j-1]} thought {CYEL}{round(dt, 1)}{CEND} sc and plays {CYEL}{action[1]+1}{CEND}")
            self.grid[action[0], action[1]] = j
            j = 1 if j == 2 else 2
            self.display()
            finished, _ = self.get_terminal_utility(self.grid)
            
            
        print(" ✅ Game is finished!")
        t_mean = round(np.array(list_t).mean(), 4)
        print(f" AI thought in average {t_mean}sc/round")
        
        
        _, final_score = self.get_terminal_utility(self.grid)
        if final_score == 99999:
            print(" 💡 AI won!")
        elif final_score == -99999:
            print(" 💡 You won!")
        else:
            print(" 💡 Equality!")
                
    
    
    def display(self) -> None:
        """Display the board of the game
        """

        print('\n| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 | \n', '-' * 49)
        for i in self.grid:
            print('| ', end='')
            for j in i:
                if j == 0:
                    print('. | ', end='')           
                elif j == 1:
                    print(f"{CRED}X{CEND} | ", end='') 
                else:
                    print(f"{CBLUE}O{CEND} | ", end='')
            print('\n')
        print('\n')



    def get_terminal_utility(self, grid:np.array) -> typing.Tuple[bool, int]:
        """Compute the terminal utility (score) of the current state of the 
        board and if the game is finished
        :param np.array grid: A state of the board
        :return typing.Tuple[bool, int]: The finish boolean and the score of the state
        """

        # Search for horizontal alignment
        for i in grid:
            for n in range(9):
                if i[n] == i[1+n] == i[2+n] == i[3+n] != 0:
                    # game is finished and return a huge/negative score
                    return [True, 99999] if i[n] == 1 else [True, -99999]

        # Search for horizontal alignment       
        for j in range(12):   
            x = grid[:, j]
            for n in range(3):
                if x[n] == x[1+n] == x[2+n] == x[3+n] != 0:
                    return [True, 99999] if x[n] == 1 else [True, -99999]
        
        # Search for diagonal aligment
        for k in range(-2, 9):
            # All right and left diagonals
            d1, d2 = self.get_diag(grid, k)
            for n in range(len(d1)-3): 
                if d1[n] == d1[1+n] == d1[2+n] == d1[3+n] != 0:
                    return [True, 99999] if d1[n] == 1 else [True, -99999]
                if d2[n] == d2[1+n] == d2[2+n] == d2[3+n] != 0:
                    return [True, 99999] if d2[n] == 1 else [True, -99999]
        
        # The board is full -> equality
        if np.sum(grid == 0) == 30:
            return [True, 50]

        return [False, 0]



    def get_diag(self, grid:np.array, k:int) -> typing.Tuple[list, list]:
        """Return the left and right diagonal of length k

        :param int k: The length of the diagonal to search for
        :param np.array grid: A state of the grid
        :return typing.Tuple[list, list]: A list of the diagonal of length k
        """
        d1, d2 = [], []
        i, j = (0, k) if k > 0 else (-k, 0)
        while i and j >0:
            i, j = i - 1, j - 1 
        while i < len(grid) and j < len(grid[0]):
            d1.append(grid[i, j])
            d2.append(grid[i, len(grid[0]) - j - 1])
            i, j = i + 1, j + 1
        return d1, d2



    def secure(self) -> typing.Tuple[int, int]:
        """Securize the action input of a player

        :return typing.Tuple[int, int]: The x and y index where the
        coins has to go
        """
        c = input(" columns n° : ")
        while not (c.isdigit() and 0 <= int(c) - 1 < 12 and 0 in self.grid[:, int(c) - 1]):
            c = input(" colonne n° : ")
        i, j = 0, int(c) - 1

        for x in range(6):
            if self.grid[x, j] != 0:
                i = x - 1
                break  
            if x == 5 and self.grid[x, j] == 0:            
                i = x
                break 
        return [i, j]



    def min_max(self) -> typing.Tuple[int, int]:
        """Compute the optimal response
        according to the current state of the 
        board using min max optimisation

        :return typing.Tuple[int, int]: The optimal action to play
        """

        act, value = [None], -9999999
        
        for a in self.actions(self.grid):
            self.depth = 0
            res = self.min_value(self.apply_action(self.grid, a, 1), -9999999, 9999999)
            if res > value:
                value = res
                act = [[a, self.depth]]
            elif res == value:
                act.append([a, self.depth])
        # if same scores, keep the actions which is the less deep
        return min(act, key=lambda x:x[1])[0]



    def actions(self, grid:np.array) -> typing.List[typing.Tuple[int, int]]:
        """Compute and return all the possible actions
        of the current state
        
        :param np.array grid: A state of the grid
        :return typing.List[typing.Tuple[int, int]]: A list of possible actions
        """
        actions = []
        for k in range(len(grid[0])):
            i, tab = 1, grid[:, k]
            n = len(tab)
            while i <= n and tab[-i] != 0:
                i += 1   
            if i <= n:
                actions.append([n-i, k])
        return actions 



    def apply_action(self, grid:np.array, a:typing.Tuple[int, int], j:int) -> np.array:
        """Apply an action a from a player j to the current board
        and return the resulted state of this action

        :param np.array grid: A state of the grid on which apply the action
        :param typing.Tuple[int, int] a: The action to apply (x, y indexes)
        :param int j: The player's number `[0|1]`
        :return np.array: The new board
        """
        res = np.copy(grid)
        res[a[0], a[1]] = j
        return res



    def min_value(self, grid:np.array, A:int, B:int) -> int:
        """Minimized the score of the ennemy using alpha and beta 
        optimizations

        :param np.array grid: A state of the board
        :param int A: The minimal score (alpha cut)
        :param int B: The maximal score (beta cut)
        :return int: The maximal scorefor player 1
        """

        self.depth += 1  
        finished, term = self.get_terminal_utility(grid)

        if finished:
            return term
        elif self.depth > self.max_depth :
            return self.heuristic(grid)
        else:
            v = 9999999
            for a in self.actions(grid):
                max_val = self.max_value(self.apply_action(grid, a, 2), A, B)
                v = min(v, max_val)
                self.depth -= 1

                # alpha beta cut
                if v <= A:return v
                B = min(v, B)
            return v



    def heuristic(self, grid:np.array) -> float:
        """Compute an approximation of the score for a player 
           and for the current state using an heuristic

        :param np.array grid: A state of the board
        :return float: The approximated score
        """
        score = 0
        for a in self.actions(grid):
            fitness = self.eval_action(grid, a)
            score += 1.7 * fitness[0] # apply a weight to encourage intiatives
            score -= fitness[1]
        return round(score, 1)



    def eval_action(self, grid:np.array, a:typing.Tuple[int, int]) -> typing.Tuple[float, float]:
        """Return a performance score for the given action for the two players

        :param np.array grid: A state of the board
        :param typing.Tuple[int, int] a: The played action
        :return typing.Tuple[float, float]: The score of the action for the player
        who played the action and the ennemy
        """
                
        local_fitness, ennemy_fitness = 0, 0

        # Compute score fitness for column
        info = self.eval_crd(grid[a[0]], a[1])
        local_fitness += info[0]
        ennemy_fitness += info[1]

        # Compute score fitness for row
        info = self.eval_crd(grid[:, a[1]], a[0])
        local_fitness += info[0]
        ennemy_fitness += info[1]
        
        # Compute score fitness for diagonals (left and right)
        d1 = []
        i, j = a
        while i >= 0 and j >= 0:
            d1.append(grid[i, j])
            i, j = i-1, j-1 
            
        d1.reverse()
        i1 = len(d1)-1
        i, j = a[0]+1, a[1]+1
        
        while i < len(grid) and j < len(grid[0]):
            d1.append(grid[i,j])
            i, j = i+1, j+1
                
        d2 = []
        i, j = a
        while i < len(grid) and j >= 0:
            d2.append(grid[i, j])
            i, j = i+1, j-1
            
        d2.reverse()
        i2 = len(d2)-1
        i, j = a[0]-1, a[1]+1
        
        while 0 <= i and j < len(grid[0]):
            d2.append(grid[i, j])
            i, j= i-1, j+1

        if len(d1) > 3:
            info = self.eval_crd(d1, i1)
            local_fitness += info[0]
            ennemy_fitness += info[1]
        
        if len(d2) > 3:
            info = self.eval_crd(d2, i2)
            local_fitness += info[0]
            ennemy_fitness += info[1]

        return local_fitness, ennemy_fitness



    def eval_crd(self, crd:list, index:int) -> typing.Tuple[float, float]:
        """Get the local fitness for a column|row|diagonal and a given
        action of this rcd at a specific index

        :param list crd: A subportion of the grid representing the rcd 
        :param int index: The index on the rcd of the action
        :return typing.Tuple[float, float]: A fitness score for the current
                                            player and the ennemy
        """
        # select the 4 nearest neighbours of the index on the rcd
        tab1 = crd[index:] if len(crd) - 1 - index < 4 else crd[index:index + 4]
        tab2 = crd[:index] if index < 4 else crd[index - 3:index]     
        tab = np.concatenate([tab2, tab1])

        local_fitness, ennemy_fitness = 0, 0
        
        # for each 4-cells subset in the crd, check what is the benefit of this action
        for k in range(len(tab) - 3):
            check = self.check_crd(tab[k:4+k])
            if check[0][0]:
                local_fitness += 3 ** check[0][1]
            if check[1][0]:
                ennemy_fitness += 3 ** check[1][1]       
        return local_fitness, ennemy_fitness



    def check_crd(self, tab:list) -> typing.Tuple[typing.Tuple[bool, int], typing.Tuple[bool, int]]:
        """Check a 4-set of cells and associate a score
        for each player 

        :param list tab: A 4-cell subset of a crd
        :return typing.Tuple[typing.Tuple[bool, int], typing.Tuple[bool, int]]: For each player, a boolean to 
        know if the player wins and a score for the given cell subset
        """
        local_fitness, ennemy_fitness = [True, 0], [True, 0]
        
        # The score is the number of cells belonging to each player
        for k in tab:
            if k == 2:
                local_fitness[0] = False
                ennemy_fitness[1] += 1
            elif k == 1:                
                ennemy_fitness[0] = False
                local_fitness[1] += 1
        return local_fitness, ennemy_fitness
    


    def max_value(self, grid:np.array, A:int, B:int) -> int:
        """Maximized the score of the ennemy using alpha and beta 
        optimizations

        :param np.array grid: A state of the board
        :param int A: The minimal score (alpha cut)
        :param int B: The maximal score (beta cut)
        :return int: The maximal score for player 2
        """

        self.depth += 1
        finished, term = self.get_terminal_utility(grid)

        if finished:
            return term
        elif self.depth > self.max_depth:
            return self.heuristic(grid)
        else:
            v = -9999999
            for a in self.actions(grid):
                min_value = self.min_value(self.apply_action(grid, a, 1), A, B)
                v = max(v, min_value)
                self.depth -= 1  
                if v >= B:return v
                A = max(v, A)    
            return v




if __name__ == "__main__":

    connect_ultra = ConnectUltra()
    connect_ultra.launch()