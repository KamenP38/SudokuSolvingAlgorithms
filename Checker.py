class Checker:
    def __init__(self, puzzle):
        self.puzzle = puzzle
    
    def get_box(self, puzzle, start_row, start_col):
        box = []
        for row in range(start_row, start_row + 3):
            box_row = []
            for col in range(start_col, start_col + 3):
                box_row.append(puzzle[row][col])
            box.append(box_row)
        return box
    
    def print_puzzle(self):
        for i in range(len(self.puzzle)):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(len(self.puzzle[i])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                print(str(self.puzzle[i][j]) + " ", end="")
                if j == len(self.puzzle[i]) - 1:
                    print("")
            
    
    def is_valid(self):
        checklst = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        #print(self.puzzle)
        # I: Check ROWS
        lst = checklst.copy()
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] in lst:
                    lst.remove(self.puzzle[i][j])
                else:
                    # print("Repetition! Puzzle is wrong ROW!")
                    # print(self.puzzle[i][j], ', ROW #', i+1)
                    return False
            lst = checklst.copy()
        
        
        # II: Check COLS 
        
        lst = checklst.copy()
        for i in range(9):
            for j in range(9):
                if self.puzzle[j][i] in lst:
                    lst.remove(self.puzzle[j][i])
                else:
                    # print("Repetition! Puzzle is wrong COL!")
                    # print(self.puzzle[j][i], ', COL #', i+1)
                    return False
            lst = checklst.copy()
                
        # III: Check Boxes (3x3)
        lst = checklst.copy()
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                box = self.get_box(self.puzzle, row, col)
                for rows in box:
                    for value in rows:
                        if value in lst:
                            lst.remove(value)
                        else:
                            # print("Repetition! Puzzle is wrong BOX!")
                            # print(value)
                            return False 
                lst = checklst.copy()
        return True          
            
                        