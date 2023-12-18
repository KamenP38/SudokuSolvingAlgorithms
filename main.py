import sys
import csv
import os
import time
from Checker_A20464521 import Checker
from MRV_A20464521 import MRV
from BruteForce_A20464521 import BruteForceRec
from Backtrack_A20464521 import BackTrack

def main():
    if len(sys.argv) == 3:
        fileName = sys.argv[1]
        fileNameSolution = fileName.replace('.csv', '_SOLUTION.csv')
        mode = sys.argv[2]
        if ((mode != "1" and mode != "2" and mode != "3" and mode != "4") or os.path.exists(fileName) == False):
           print('ERROR: Illegal input arguments.')
           exit() 
    else:
        print('ERROR: Not enough or too many input arguments.')
        exit()

    print("Petkov, Kamen, A20464521 solution: ")
    print("Input file: ", fileName)  
    if mode == "1":
        print("Algorithm: Brute Force Search")
    elif mode == "2":
        print("Algorithm: Constraint Satisfaction Problem back-tracking search")
    elif mode == "3":
        print("Algorithm: CSP with forward-checking and MRV heuristics")
    elif mode == "4":
        print("Algorithm: TEST")
    print("Input puzzle: \n")
    
    # Open the CSV file
    vals = []
    
    allValues = []
    with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # we want to keep looping until we exhaust all possible combinations
            i = 0
            for row in reader:
                for value in row:
                    allValues.append(value)
    puzzle = []
    r = 0
    for i in range(0, 9):
            row = []
            for _ in range(0, 9):
                row.append(allValues[r])
                r += 1
            puzzle.append(row)

    for i in range(len(puzzle)):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(len(puzzle[i])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                print(str(puzzle[i][j]) + " ", end="")
                if j == len(puzzle[i]) - 1:
                    print("")

    # adding print() for better spacing
    print()
    
    if mode == "1":
        BF = BruteForceRec(fileName)
        start_time = time.time()
        BF.BruteForce()
        end_time = time.time()
        totalTime = end_time - start_time
        print("Number of search tree nodes generated: ", BF.nodes)
        print("Search time: ", totalTime, "\n")
        print("Solved puzzle: ")
        BF.print_puzzle_final()
        with open(fileNameSolution, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in BF.puzzle:
                writer.writerow(row)
    elif mode == "2": 
        backtrack = BackTrack(fileName)
        start_time = time.time()
        backtrack.CSP()
        end_time = time.time()
        backtrack.print_puzzle_final()
        totalTime = end_time - start_time
        print("Number of search tree nodes generated: ", backtrack.nodes)
        print("Search time: ", totalTime, "\n")
        print("Solved puzzle: ")
        backtrack.print_puzzle_final()
        with open(fileNameSolution, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in backtrack.puzzle:
                writer.writerow(row)
    elif mode == "3":
        mrv = MRV(fileName)
        start_time = time.time()
        mrv.MRV()
        end_time = time.time()
        mrv.print_puzzle_final()
        totalTime = end_time - start_time
        print("Number of search tree nodes generated: ", mrv.nodes)
        print("Search time: ", totalTime, "\n")
        print("Solved puzzle: ")
        mrv.print_puzzle_final()
        with open(fileNameSolution, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in mrv.puzzle:
                writer.writerow(row)
                
    elif mode == "4":   
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # we want to keep looping until we exhaust all possible combinations
            i = 0
            for row in reader:
                for value in row:
                    vals.append(value)
        puzzle = []
        r = 0
        for i in range(0, 9):
                row = []
                for _ in range(0, 9):
                    row.append(vals[r])
                    r += 1
                puzzle.append(row)
        
        print("Sudoku from last algorithm: \n")
        
        for i in range(len(puzzle)):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(len(puzzle[i])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                print(str(puzzle[i][j]) + " ", end="")
                if j == len(puzzle[i]) - 1:
                    print("") 
        
        checker = Checker(puzzle)
        valid = checker.is_valid()
        if valid:
            print("\nThis is a valid, solved, Sudoku puzzle.")
        else:
            print("\nERROR: This is NOT a solved Sudoku puzzle.")

    
    
main()

