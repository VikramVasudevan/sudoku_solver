import json

SUDOKU_PUZZLE_SIZE = 9

debug = True

SUBCUBE_CONFIG = [
    [(0, 2), (0, 2)],
    [(0, 2), (3, 5)],
    [(0, 2), (6, 8)],
    [(3, 5), (0, 2)],
    [(3, 5), (3, 5)],
    [(3, 5), (6, 8)],
    [(6, 8), (0, 2)],
    [(6, 8), (3, 5)],
    [(6, 8), (6, 8)],
]


def log(level, message):
    if(level == 'debug' and debug == True):
        print(message)
    elif(level != 'debug'):
        print(message)


def generatePuzzle():
    print("Generating puzzle ...")
    # hard coding for now instead of using a generator function.
    puzzle = [[0, 0, 2, 0, 8, 0, 0, 6, 0],
              [0, 5, 6, 9, 1, 7, 0, 3, 0],
              [0, 4, 0, 0, 5, 0, 8, 7, 1],
              [0, 9, 0, 0, 0, 0, 6, 0, 0],
              [6, 7, 1, 0, 9, 5, 2, 0, 0],
              [0, 0, 0, 0, 2, 0, 1, 0, 0],
              [1, 6, 7, 0, 3, 0, 5, 9, 0],
              [4, 8, 0, 0, 7, 0, 3, 0, 0],
              [0, 2, 5, 4, 6, 0, 0, 0, 0]
              ]
    print("Generated puzzle ...")
    return puzzle


def checkGrid(grid):
    print("Checking if grid is populated ...")
    fineRows = 0
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        rowValidated = False
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            # print("Processing " + str(row) + "," + str(col))
            if(grid[row][col] > 0):
                # print("Row is fine ...")
                rowValidated = True
                break
        if(rowValidated == True):
            fineRows = fineRows + 1
    if(fineRows == SUDOKU_PUZZLE_SIZE):
        print("Grid looks fine")
    else:
        raise Exception('Grid has errors')
    print("Checking if grid is populated ... DONE")


def getSubcubeByRowCol(prmRow, prmCol):
    subcubeNumber = -1
    # print("Getting subcube for", prmRow, prmCol)
    index = 0
    for subcube in SUBCUBE_CONFIG:
        # print("subcube = ", subcube)
        rowDimensions = subcube[0]
        colDimensions = subcube[1]
        if(prmRow >= rowDimensions[0] and prmRow <= rowDimensions[1] and prmCol >= colDimensions[0] and prmCol <= colDimensions[1]):
            subcubeNumber = index
            break
        index = index + 1
    return subcubeNumber

def getCellsBySubcubeNumber(subcubeNumber):
    print("getting cells for subcube", subcubeNumber)
    subcube = SUBCUBE_CONFIG[subcubeNumber]
    cells = []
    for row in range(subcube[0][0],subcube[0][1] + 1):
        for col in range(subcube[1][0],subcube[1][1] + 1):
            cells.append((row,col))
    return cells


def isPossibleValue(prmPossibleValue, prmSolvedGrid, prmRow, prmCol):
    log("debug", "Checking possible value %s for (%s,%s)" %
        (prmPossibleValue, prmRow, prmCol))
    endAlgorithm = False
    outcome = (True, 0)
    # Return a tuple containing
    # # - a boolean saying whether or not it is a possible value
    # # - a number indicating confidence level

    log("debug", "Checking all cells in the row ...")
    # Check if this value is already present in the entire row
    for y in range(0, SUDOKU_PUZZLE_SIZE):
        solvedGridIndex = (prmRow * SUDOKU_PUZZLE_SIZE) + y
        matched = prmSolvedGrid[solvedGridIndex]['value'] == prmPossibleValue
        log("debug", ("solvedGrid[]", solvedGridIndex,
                      prmSolvedGrid[solvedGridIndex]['value'], prmPossibleValue, matched))
        if(y != prmCol and matched == True):
            outcome = (False, 100)
            endAlgorithm = True
            break

    if(endAlgorithm):
        return outcome

    log("debug", "Checking all cells in the column ...")
    # Check if this value is already present in the entire column
    for x in range(0, SUDOKU_PUZZLE_SIZE):
        solvedGridIndex = (x * SUDOKU_PUZZLE_SIZE) + prmCol
        matched = prmSolvedGrid[solvedGridIndex]['value'] == prmPossibleValue
        log("debug", ("solvedGrid[]", solvedGridIndex,
                      prmSolvedGrid[solvedGridIndex]['value'], prmPossibleValue, matched))
        if(x != prmRow and matched == True):
            outcome = (False, 100)
            endAlgorithm = True
            break

    if(endAlgorithm):
        return outcome

    # Find the subcube for this row and col
    subcubeNumber = getSubcubeByRowCol(prmRow, prmCol)
    cells = getCellsBySubcubeNumber(subcubeNumber)
    # Check if this value is already present in the entire subcube.
    for cell in cells:
        solvedGridIndex = (cell[0] * SUDOKU_PUZZLE_SIZE) + cell[1]
        matched = prmSolvedGrid[solvedGridIndex]['value'] == prmPossibleValue
        if(matched == True):
            outcome = (False, 100)
            endAlgorithm = True
            break

    if(endAlgorithm):
        return outcome
    
    return outcome

def solve(unsolvedGrid):
    print("Solving ...", unsolvedGrid)
    solvedGrid = []
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            obj = {
                "possibleValues": [],
                "impossibleValues": [],
                "value": unsolvedGrid[row][col],
                "finalized": False
            }
            solvedGrid.append(obj)

    # print("solvedGrid", json.dumps(list(solvedGrid), indent=1))

    for row in range(0, SUDOKU_PUZZLE_SIZE):
        # print("Processing row ...", row)
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            # print("Processing column ...", col)
            solvedGridIndex = (row * SUDOKU_PUZZLE_SIZE) + col
            # row == 8 and col == 7 and
            if(unsolvedGrid[row][col] == 0):
                log('debug', ("solvedGridIndex = ", solvedGridIndex))
                # Unsolved cell. Solve it.
                # print("This cell is unsolved. solving it ...", row, col)
                for possibleValue in range(1, SUDOKU_PUZZLE_SIZE + 1):
                    # print("Checking if " + str(possibleValue) +
                    #      " would fit here ...")
                    outcome = isPossibleValue(
                        possibleValue, solvedGrid, row, col)
                    if(outcome[0] == True):
                        if(outcome[1] == 100):
                            # this is a possible value with 100% confidence. just update the cell
                            solvedGrid[solvedGridIndex]["value"] = possibleValue
                            solvedGrid[solvedGridIndex]["finalized"] = True
                        elif(outcome[1] > 0):
                            if possibleValue not in solvedGrid[solvedGridIndex]['possibleValues']:
                                solvedGrid[solvedGridIndex]['possibleValues'].append(
                                    possibleValue)
                    elif(outcome[0] == False and outcome[1] == 100):
                        # this is an impossible value with 100% confidence. just add to array
                        if (possibleValue not in solvedGrid[solvedGridIndex]['impossibleValues']):
                            solvedGrid[solvedGridIndex]['impossibleValues'].append(
                                possibleValue)
                # print("impossibleValues = ",
                #      solvedGrid[solvedGridIndex]['impossibleValues'])

    print("Solved ...", json.dumps(solvedGrid, indent=1))

def test():
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            print("subcube of ", row, col, "=",getSubcubeByRowCol(row, col))

    print(getCellsBySubcubeNumber(5))

print("Starting Sudoku Solver ...")
puzzle = generatePuzzle()
print(puzzle)
checkGrid(puzzle)
# test()
solve(puzzle)