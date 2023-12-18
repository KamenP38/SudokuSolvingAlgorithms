import csv


class BackTrack:

    def __init__(self, filename):
        self.filename = filename
        self.allValues = [] # I use this to create my initial puzzle 2D array
        self.puzzle = []
        self.nodes = 0
        
        # get the values we are going to work with
        with open(self.filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # we want to keep looping until we exhaust all possible combinations
            i = 0
            for row in reader:
                for value in row:
                    
                    self.allValues.append(value)
                    # print(self.allValues[i])
                    # Do something with the value
                    i += 1
    
        # now that we have the values with "X", we will assign values to them
        # whenever it's not value --> BACKTRACK (RECURSIVELY)
        
        # This is the puzzle that we will work with
        r = 0
        for i in range(0, 9):
            row = []
            for _ in range(0, 9):
                row.append(self.allValues[r])
                r += 1
            self.puzzle.append(row)

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
                # print("ROW")
                return False
        
        
        # II: Check COLS 
        for i in range(9):
            if self.puzzle[i][col] == val:
                # print("COL")
                return False
                
        # III: Check Boxes (3x3)
        boxRow = (row // 3) * 3
        boxCol = (col // 3) * 3
        for i in range(boxRow, boxRow + 3):
            for j in range(boxCol, boxCol + 3):
                if self.puzzle[i][j] == val:
                    return False
        return True  


    # Process:
    # Start by choosing a value from a domain - in my case I don't do constraint propagation
    # Thus, my domain is always {1, 2, 3, 4, 5, 6, 7, 8, 9}
    # keep choosing values until you see a conflict
    # if you see a conflict --> backtrack

    
    def firstEmptySpot(self, puzzle):
        for r in range(9):
            for c in range(9):
                if self.puzzle[r][c] == "X":
                    return r, c
        # if there are no empty spots (aka equal to "X") left return None
        return None
    
    
    # back-track search
    def CSP(self): 
        # print("\033c") # clear the terminal
        # self.print_puzzle_final()
        # call function that chooses first empty spot
        values = self.firstEmptySpot(self.puzzle)
        if values == None:         
            return True
        else:
            row, col = values
        
        for val in range(1, 10):
            if self.is_valid(row, col, str(val)):
                self.puzzle[row][col] = str(val)
                self.nodes += 1
                if self.CSP():
                    return True
                self.puzzle[row][col] = "X"
        return False
        
        
        
        
