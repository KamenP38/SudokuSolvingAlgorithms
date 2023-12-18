import copy
import csv


class MRV:

    def __init__(self, filename):
        self.filename = filename
        self.allValues = [] 
        self.domains = {} 
        self.missing = []
        self.puzzle = [] # 2d array of the puzzle
        self.constraints = {} # dictionary that contains all the neighbors of current cell
        self.nodes = 0
        
        # get the values we are going to work with
        with open(self.filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # we want to keep looping until we exhaust all possible combinations
            i = 0
            for row in reader:
                for value in row:
                    
                    self.allValues.append(value)
                    # Do something with the value
                    i += 1
        
        # This is the puzzle that we will work with
        r = 0
        for i in range(0, 9):
            row = []
            for _ in range(0, 9):
                row.append(self.allValues[r])
                r += 1
            self.puzzle.append(row)
            
        # prepare the constraints dictionary
        row_constraints = set()
        col_constraints = set()
        row_col = set()
        # Row and column
        for i in range(9):
            for j in range(9):
                cellNum = (i, j)
                row_constraints = set([(i, col) for col in range(9) if col != j])
                col_constraints = set([(row, j) for row in range(9) if row != i]) 
                row_col = row_constraints.union(col_constraints)
                self.constraints[cellNum] = row_col
        
        # Box
        for i in range(9):
            for j in range(9):
                r = i // 3
                c = j // 3
                box = set([(m, n) for m in range(r * 3, r * 3 + 3) for n in range(c * 3, c * 3 + 3)])
                cellNum = (i, j)
                box.discard(cellNum)
                self.constraints[cellNum].update(box)
               
                
                
        
        # initialize the domains               
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == "X":
                    # self.domains.update({(i, j): [str(x) for x in range(1, 10)]})
                    self.missing.append((i, j))
                else:
                    self.domains[(i, j)] = [self.puzzle[i][j]]
    
        self.initial_domains()
        # Up to here everything works fine!
        
        
        
    
    def initial_domains(self):
        for cell in self.missing:
            lst = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            for neighbor in self.constraints[cell]:
                if neighbor not in self.missing:
                    row, col = neighbor
                    if self.puzzle[row][col] in lst:
                        lst.remove(self.puzzle[row][col])
            self.domains.update({cell: lst})
        
    # print function to see the puzzle/sudoku at the end
    def print_puzzle_final(self):
        for i in range(len(self.puzzle)):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(len(self.puzzle[i])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                print(str(self.puzzle[i][j]) + " ", end="")
                if j == len(self.puzzle[i]) - 1:
                    print("")
    
    # this function is essentially the constraint 
    # Is the current value valid for the row, col and current box?
    # if everything is okay, assign the value
    def is_valid(self, row, col, val):
        # I: Check ROWS
        for i in range(9):
            if self.puzzle[row][i] == val:
                return False
        
        
        # II: Check COLS 
        for i in range(9):
            if self.puzzle[i][col] == val:
                return False
                
        # III: Check Boxes (3x3)
        boxRow = (row // 3) * 3
        boxCol = (col // 3) * 3
        for i in range(boxRow, boxRow + 3):
            for j in range(boxCol, boxCol + 3):
                if self.puzzle[i][j] == val:
                    return False
        return True 
    
    def mrv_heuristic(self, todo):
        min_cell = None
        min_cell_value = float('inf')
        for cell in self.missing:
            if len(todo[cell]) > 0 and len(todo[cell]) < min_cell_value:  # we do len because the "value" that is connected to the key is actually a list
                min_cell = cell
                min_cell_value = len(todo[cell])
        # convert to row | cell
        return min_cell

    def forward_checking(self, cell, value): 
            row, col = cell
            self.puzzle[row][col] = value
            self.missing.remove(cell)
            self.domains[(row, col)] = [value]
            # Check constraints with neighbors
            # iterate over all of the neighborss in order to update their domains
            for neighbor in self.constraints[cell]:
                if neighbor in self.missing:
                    if value in self.domains[neighbor]:
                        # update domain
                        self.domains[neighbor].remove(value)
                        # if any of the domains becomes 0, it's wrong
                    if len(self.domains[neighbor]) == 0:
                        return False
            return True

    def restore(self, cell, value, domains):
        row, col = cell
        self.puzzle[row][col] = "X"
        self.missing.append(cell)
        self.domains= domains.copy()
        self.domains[cell].remove(value)
        return True
        
        
    
    # back-track search
    def MRV(self):
        # print("\033c") # clear the terminal
        # self.print_puzzle_final()
        values = self.mrv_heuristic(self.domains)
        if values == None:
            return True
        else:
            row, col = values
        
        # Try values in the order of the domain
        for val in sorted(self.domains[(row, col)]): 
            if self.is_valid(row, col, str(val)):
                domains_copy = copy.deepcopy(self.domains)
                                
                # Forward checking to reduce domain of other variables
                if self.forward_checking((row, col), str(val)):
                    self.nodes += 1
                    if self.MRV():
                        return True

                # Restore domain and backtrack if assignment is invalid
                # We need a rollback function
                self.restore((row, col), str(val), domains_copy)
                
        # Return False if puzzle cannot be solved
        return False
        
        
        
        
