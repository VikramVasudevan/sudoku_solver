import json
from time import monotonic
import config

SUDOKU_PUZZLE_SIZE = config.SUDOKU_PUZZLE_SIZE
debug = config.debug
SUBCUBE_CONFIG = config.SUBCUBE_CONFIG


def log(level, message):
    if(level == 'debug' and debug == True):
        print(message)
    elif(level != 'debug'):
        print(message)


def generatePuzzle():
    print("Generating puzzle ...")
    # hard coding for now instead of using a generator function.
    puzzle = config.expert_puzzle
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
    # print("getting cells for subcube", subcubeNumber)
    subcube = SUBCUBE_CONFIG[subcubeNumber]
    cells = []
    for row in range(subcube[0][0], subcube[0][1] + 1):
        for col in range(subcube[1][0], subcube[1][1] + 1):
            cells.append((row, col))
    return cells


def isPuzzleSolved(grid):
    solved = len([x for x in grid if x['value'] == 0]) == 0
    return solved


def calculatePercentComplete(grid):
    unsolved = len([x for x in grid if x['value'] == 0])
    totalGridCount = SUDOKU_PUZZLE_SIZE * SUDOKU_PUZZLE_SIZE
    percent = (totalGridCount-unsolved)/totalGridCount * 100
    print("unsolved = ", unsolved, "total = ",
          totalGridCount, "percent = ", percent)
    return percent


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


def formatGrid(unsolvedGrid):
    formattedGrid = []
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            obj = {
                "possibleValues": [],
                "impossibleValues": [],
                "value": unsolvedGrid[row][col],
                "finalized": False
            }
            formattedGrid.append(obj)

    return formattedGrid


def solve(unsolvedGrid, level):
    print("Solving attempt %d [completion percent = %f]..." % (
        level, calculatePercentComplete(unsolvedGrid)))
    solvedGrid = unsolvedGrid

    # print("solvedGrid", json.dumps(list(solvedGrid), indent=1))

    for row in range(0, SUDOKU_PUZZLE_SIZE):
        # print("Processing row ...", row)
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            # print("Processing column ...", col)
            gridIndex = (row * SUDOKU_PUZZLE_SIZE) + col
            # row == 8 and col == 7 and
            if(unsolvedGrid[gridIndex]['value'] == 0):
                log('debug', ("solvedGridIndex = ", gridIndex))
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
                            solvedGrid[gridIndex]["value"] = possibleValue
                            solvedGrid[gridIndex]["finalized"] = True
                        elif(outcome[1] > 0):
                            if possibleValue not in solvedGrid[gridIndex]['possibleValues']:
                                solvedGrid[gridIndex]['possibleValues'].append(
                                    possibleValue)
                    elif(outcome[0] == False and outcome[1] == 100):
                        # this is an impossible value with 100% confidence. just add to array
                        if (possibleValue not in solvedGrid[gridIndex]['impossibleValues']):
                            solvedGrid[gridIndex]['impossibleValues'].append(
                                possibleValue)
                # print("impossibleValues = ",
                #      solvedGrid[solvedGridIndex]['impossibleValues'])
                if(len(solvedGrid[gridIndex]['impossibleValues']) == SUDOKU_PUZZLE_SIZE - 1):
                    # these are  having exactly 8 impossible values indicating that only one possible value is there
                    # find that value and set it directly
                    possibleValues = [x for x in range(
                        1, SUDOKU_PUZZLE_SIZE + 1) if x not in solvedGrid[gridIndex]['impossibleValues']]
                    # print("Possible Values = ", solvedGrid[gridIndex]['impossibleValues'], range(1, SUDOKU_PUZZLE_SIZE + 1), possibleValues)
                    if(len(possibleValues) >= 1):
                        solvedGrid[gridIndex]['value'] = possibleValues[0]
                        solvedGrid[gridIndex]['finalized'] = True
    if(isPuzzleSolved(solvedGrid)):
        print("Solved ...", [cell['value'] for cell in solvedGrid])
        print("*****SOLVED*****")
    else:
        if(level < config.MAX_ATTEMPTS - 1):
            print("Attempting again ...", calculatePercentComplete(solvedGrid))
            solve(solvedGrid, level + 1)
        else:
            print(json.dumps(solvedGrid,indent=1))
            print("****COULD NOT SOLVE IN %d ATTEMPTS****" %
                  (config.MAX_ATTEMPTS))


def test():
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            print("subcube of ", row, col, "=", getSubcubeByRowCol(row, col))

    print(getCellsBySubcubeNumber(5))


def diff():
    list1 = [1, 2, 3, 4, 5, 6, 8, 9]
    list2 = range(1, 10)
    print(list1, list2)
    value = [x for x in list2 if x not in list1]
    print(value)


print("Starting Sudoku Solver ...")
puzzle = generatePuzzle()
print(puzzle)
checkGrid(puzzle)
# test()
# solved = isPuzzleSolved(formatGrid(puzzle))
# print(solved)
start_time = monotonic()
solve(formatGrid(puzzle), 0)
print(f"Run time {monotonic() - start_time} seconds")
# diff()
# print(calculatePercentComplete(formatGrid(puzzle)))
