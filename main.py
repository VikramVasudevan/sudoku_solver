import json
from time import monotonic
import config
import logging
logging.basicConfig(filename='main.log', encoding='utf-8',
                    level=logging.DEBUG, filemode="w")

SUDOKU_PUZZLE_SIZE = config.SUDOKU_PUZZLE_SIZE
debug = config.debug
SUBCUBE_CONFIG = config.SUBCUBE_CONFIG

g_prev_percent_complete = 0
g_percent_complete = 0

# Yield successive n-sized
# chunks from l.


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def printGridState(grid, title, mode):
    with open('grid_state.txt', mode) as f:
        f.write("\n")
        # f.write('#########################################################')
        f.write("\n")
        f.write(title + "\n")
        for cell in grid:
            if(cell["index"] % SUDOKU_PUZZLE_SIZE == 0):
                if(cell["row"] > 0):
                    f.write("|")
                f.write("\n")
            if(cell["row"] % 3 == 0 and cell["col"] == 0):
                f.write(" _ _ _ _ _ _ _ _ _ _")
                f.write("\n")
            if(cell["col"] % 3 == 0):
                f.write("|")
            f.write(str("." if cell['value'] == 0 else cell['value']))
            f.write(' ')
        f.write("|\n")
        f.write(" - - - - - - - - - -")
        # f.write('#########################################################')


def log(level, *message):
    if(level == 'debug'):
        if(debug == True):
            logging.debug(message)
    elif(level == 'error'):
        logging.error(message)
    else:
        logging.info(message)


def logInfo(*message):
    logging.info(message)


def generatePuzzle():
    logInfo("Generating puzzle ...")
    # hard coding for now instead of using a generator function.
    puzzle = config.SELECTED_PUZZLE
    logInfo("Generated puzzle ...")
    return puzzle


def checkGrid(grid):
    logInfo("Checking if grid is populated ...")
    fineRows = 0
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        rowValidated = False
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            # logInfo("Processing " + str(row) + "," + str(col))
            if(grid[row][col] > 0):
                # logInfo("Row is fine ...")
                rowValidated = True
                break
        if(rowValidated == True):
            fineRows = fineRows + 1
    if(fineRows == SUDOKU_PUZZLE_SIZE):
        logInfo("Grid looks fine")
    else:
        raise Exception('Grid has errors')
    logInfo("Checking if grid is populated ... DONE")


def getSubcubeByRowCol(prmRow, prmCol):
    subcubeNumber = -1
    # logInfo("Getting subcube for", prmRow, prmCol)
    index = 0
    for subcube in SUBCUBE_CONFIG:
        # logInfo("subcube = ", subcube)
        rowDimensions = subcube[0]
        colDimensions = subcube[1]
        if(prmRow >= rowDimensions[0] and prmRow <= rowDimensions[1] and prmCol >= colDimensions[0] and prmCol <= colDimensions[1]):
            subcubeNumber = index
            break
        index = index + 1
    return subcubeNumber


def getCellsBySubcubeNumber(subcubeNumber):
    # logInfo("getting cells for subcube", subcubeNumber)
    subcube = SUBCUBE_CONFIG[subcubeNumber]
    cells = []
    for row in range(subcube[0][0], subcube[0][1] + 1):
        for col in range(subcube[1][0], subcube[1][1] + 1):
            cells.append((row, col))
    return cells


def getCellsBySubcubeNumberExcludingPlane(subcubeNumber, plane, planeNumber):
    # print("getting cells for subcube", subcubeNumber,plane, planeNumber)
    subcube = SUBCUBE_CONFIG[subcubeNumber]
    cells = []
    xPlaneRange = range(subcube[0][0], subcube[0][1] + 1)
    yPlaneRange = range(subcube[1][0], subcube[1][1] + 1)
    # print("info",xPlaneRange, yPlaneRange)
    for row in xPlaneRange:
        if(plane == 'x' and row == planeNumber):
            continue
        for col in yPlaneRange:
            if(plane == 'y' and col == planeNumber):
                # print("breaking", col)
                continue
            cells.append((row, col))
    return cells


def isPuzzleSolved(grid):
    solved = len([x for x in grid if x['value'] == 0]) == 0
    calculatePercentComplete(grid)
    return solved


def calculatePercentComplete(grid):
    global g_prev_percent_complete
    global g_percent_complete
    g_prev_percent_complete = g_percent_complete
    unsolved = len([x for x in grid if x['value'] == 0])
    totalGridCount = SUDOKU_PUZZLE_SIZE * SUDOKU_PUZZLE_SIZE
    g_percent_complete = round(
        (totalGridCount-unsolved)/totalGridCount * 100, 2)
    logInfo("unsolved = ", unsolved, "total = ",
            totalGridCount, "percent = ", g_percent_complete)
    return round(g_percent_complete, 2)


def isPossibleValue(prmPossibleValue, prmSolvedGrid, prmRow, prmCol):
    log("info", prmRow, prmCol, "Checking possible value %s" %
        (prmPossibleValue))
    endAlgorithm = False
    outcome = (True, 0)
    currentGridIndex = (prmRow * SUDOKU_PUZZLE_SIZE) + prmCol
    # Return a tuple containing
    # # - a boolean saying whether or not it is a possible value
    # # - a number indicating confidence level

    log("debug", "Checking all cells in the row ...", prmRow)
    # SCENARIO 1: Check if this value is already present in the entire row
    for y in range(0, SUDOKU_PUZZLE_SIZE):
        solvedGridIndex = (prmRow * SUDOKU_PUZZLE_SIZE) + y
        matched = prmSolvedGrid[solvedGridIndex]['value'] == prmPossibleValue
        log("info", (prmRow, prmCol, "SCENARIO-1", solvedGridIndex,
                      prmSolvedGrid[solvedGridIndex]['value'], prmPossibleValue, matched))
        if(y != prmCol and matched == True):
            outcome = (False, 100)
            endAlgorithm = True
            break

    if(endAlgorithm):
        logInfo(prmRow, prmCol, "outcome for possible value",
                prmPossibleValue, "1", outcome)
        return outcome

    log("debug", "Checking all cells in the column ...", prmCol)
    # SCENARIO 2: Check if this value is already present in the entire column
    for x in range(0, SUDOKU_PUZZLE_SIZE):
        solvedGridIndex = (x * SUDOKU_PUZZLE_SIZE) + prmCol
        matched = prmSolvedGrid[solvedGridIndex]['value'] == prmPossibleValue
        log("info", (prmRow,prmCol, "SCENARIO-2", solvedGridIndex,
                     prmSolvedGrid[solvedGridIndex]['value'], prmPossibleValue, matched))
        if(x != prmRow and matched == True):
            outcome = (False, 100)
            endAlgorithm = True
            break

    if(endAlgorithm):
        logInfo(prmRow, prmCol, "outcome for possible value",
                prmPossibleValue, "2", outcome)
        return outcome

    # Find the subcube for this row and col
    subcubeNumber = getSubcubeByRowCol(prmRow, prmCol)
    cells = getCellsBySubcubeNumber(subcubeNumber)
    # SCENARIO 3: Check if this value is already present in the entire subcube.
    for cell in cells:
        solvedGridIndex = (cell[0] * SUDOKU_PUZZLE_SIZE) + cell[1]
        matched = prmSolvedGrid[solvedGridIndex]['value'] == prmPossibleValue
        log("info", (prmRow,prmCol, "SCENARIO-3", solvedGridIndex,
                     prmSolvedGrid[solvedGridIndex]['value'], prmPossibleValue, matched))
        if(matched == True):
            outcome = (False, 100)
            endAlgorithm = True
            break

    if(endAlgorithm):
        logInfo(prmRow, prmCol, "outcome for possible value",
                prmPossibleValue, "3", outcome)
        return outcome

    # SCENARIO 4: if this possible value cannot be fit (impossible value) into another cell in the row, col or subcube, then it is a possible value for sure here

    # Scenario 4a:
    valueCannotBeFitAnywhereElse = True
    for y in range(0, SUDOKU_PUZZLE_SIZE):
        solvedGridIndex = (prmRow * SUDOKU_PUZZLE_SIZE) + y
        if(prmSolvedGrid[solvedGridIndex]['finalized'] == False and currentGridIndex != solvedGridIndex):
            matched = prmPossibleValue in prmSolvedGrid[solvedGridIndex]['impossibleValues']
            log("info", (prmRow,prmCol, "SCENARIO-4a", solvedGridIndex,
                        prmSolvedGrid[solvedGridIndex]['impossibleValues'], prmPossibleValue, matched))
            valueCannotBeFitAnywhereElse = valueCannotBeFitAnywhereElse and matched
    if(valueCannotBeFitAnywhereElse):
        outcome = (True, 100)
        endAlgorithm = True
    if(endAlgorithm):
        logInfo(prmRow, prmCol, "outcome for possible value",
                prmPossibleValue, '4a', outcome)
        return outcome

    # Scenario 4b:
    valueCannotBeFitAnywhereElse = True
    for x in range(0, SUDOKU_PUZZLE_SIZE):
        solvedGridIndex = (x * SUDOKU_PUZZLE_SIZE) + prmCol
        # logInfo(prmRow, prmCol, prmPossibleValue, "Checking in col ", currentGridIndex, solvedGridIndex,  prmPossibleValue, "in",
        #         prmSolvedGrid[solvedGridIndex]['impossibleValues'], prmPossibleValue in prmSolvedGrid[
        #             solvedGridIndex]['impossibleValues'])
        if(prmSolvedGrid[solvedGridIndex]['finalized'] == False and currentGridIndex != solvedGridIndex):
            valueCannotBeFitAnywhereElse = valueCannotBeFitAnywhereElse and prmPossibleValue in prmSolvedGrid[
                solvedGridIndex]['impossibleValues']
    if(valueCannotBeFitAnywhereElse):
        outcome = (True, 100)
        endAlgorithm = True
    if(endAlgorithm):
        logInfo(prmRow, prmCol, "outcome for possible value",
                prmPossibleValue, '4b', outcome)
        return outcome

    # Scenario 4c:
    valueCannotBeFitAnywhereElse = True
    for cell in cells:
        solvedGridIndex = (cell[0] * SUDOKU_PUZZLE_SIZE) + cell[1]
        # logInfo(prmRow, prmCol, prmPossibleValue, "Checking in subcube ", currentGridIndex, solvedGridIndex, prmPossibleValue, "in",
        #         prmSolvedGrid[solvedGridIndex]['impossibleValues'], prmPossibleValue in prmSolvedGrid[
        #             solvedGridIndex]['impossibleValues'])
        if(prmSolvedGrid[solvedGridIndex]['finalized'] == False and currentGridIndex != solvedGridIndex):
            valueCannotBeFitAnywhereElse = valueCannotBeFitAnywhereElse and prmPossibleValue in prmSolvedGrid[
                solvedGridIndex]['impossibleValues']

    if(valueCannotBeFitAnywhereElse):
        outcome = (True, 100)
        endAlgorithm = True

    if(endAlgorithm):
        logInfo(prmRow, prmCol, "outcome for possible value",
                prmPossibleValue, '4c', outcome)
        return outcome

    # Scenario 5: check if this possible value can ONLY occur in this x or y plane (because it cannot occur anywhere else in the subcubes of those cells)
    # Scenario 5a: x plane
    if True:
        for y in range(0, SUDOKU_PUZZLE_SIZE):
            subcubeNumberOfOtherCell = getSubcubeByRowCol(prmRow, y)
            # ignore current subcube
            if(subcubeNumberOfOtherCell == subcubeNumber):
                continue
            cellsinThatSubcube = getCellsBySubcubeNumberExcludingPlane(
                subcubeNumberOfOtherCell, "x", prmRow)
            log("info", prmRow, prmCol, "possibleValue=", prmPossibleValue,
                "cellsinThatSubcube = ", "plane-x-", y, "subcubeNumberOfOtherCell = ", subcubeNumberOfOtherCell, cellsinThatSubcube)
            for cell in cellsinThatSubcube:
                solvedGridIndex = (cell[0] * SUDOKU_PUZZLE_SIZE) + cell[1]
                if(prmSolvedGrid[solvedGridIndex]['finalized'] == False):
                    if(prmPossibleValue not in prmSolvedGrid[solvedGridIndex]['impossibleValues']):
                        outcome = (False, 0)
                        endAlgorithm = True
                        break
            if(endAlgorithm):
                break
            else:
                outcome = (True, 100)
                endAlgorithm = True
                break

        if(endAlgorithm):
            logInfo(prmRow, prmCol, "outcome for possible value",
                    prmPossibleValue, '5a', outcome)
            return outcome

    if False:
        # Scenario 5b: y plane
        for x in range(0, SUDOKU_PUZZLE_SIZE):
            subcubeNumberOfOtherCell = getSubcubeByRowCol(x, prmCol)
            # ignore current subcube
            if(subcubeNumberOfOtherCell == subcubeNumber):
                continue
            cellsinThatSubcube = getCellsBySubcubeNumberExcludingPlane(
                subcubeNumberOfOtherCell, "y", prmCol)
            log("info", prmRow, prmCol,
                "cellsinThatSubcube = ", "plane-y-", x, subcubeNumberOfOtherCell, cellsinThatSubcube)
            for cell in cellsinThatSubcube:
                solvedGridIndex = (cell[0] * SUDOKU_PUZZLE_SIZE) + cell[1]
                if(prmSolvedGrid[solvedGridIndex]['finalized'] == False):
                    if(prmPossibleValue not in prmSolvedGrid[solvedGridIndex]['impossibleValues']):
                        outcome = (False, 0)
                        endAlgorithm = True
                        break
            if(endAlgorithm):
                break
            else:
                outcome = (True, 100)
                endAlgorithm = True
                break

        if(endAlgorithm):
            logInfo(prmRow, prmCol, "outcome for possible value",
                    prmPossibleValue, '5b', outcome)
            return outcome

    # Scenario 5c : If a possible value is impossible to fill any cell in its x, y planes, then it is 100% possible here.

    return outcome


def formatGrid(unsolvedGrid):
    formattedGrid = []
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            currentVal = unsolvedGrid[row][col]
            subcubeNumber = getSubcubeByRowCol(row, col)
            obj = {
                "index": (row * SUDOKU_PUZZLE_SIZE) + col,
                "row": row,
                "col": col,
                "subcube": {
                    "index": subcubeNumber,
                    "cells": getCellsBySubcubeNumber(subcubeNumber),
                },
                "possibleValues": [],
                "impossibleValues": [] if currentVal == 0 else [x for x in range(1, SUDOKU_PUZZLE_SIZE+1) if x != currentVal],
                "value": currentVal,
                "finalized": currentVal != 0
            }
            formattedGrid.append(obj)

    return formattedGrid


def solve(unsolvedGrid, level):
    logInfo("Solving attempt %d [completion percent = %f]..." % (
        level, g_percent_complete))
    solvedGrid = unsolvedGrid
    printGridState(solvedGrid, "Level-" + str(level) + " ~ [" +
                   str(g_percent_complete) + "% complete]", "a")
    # logInfo("solvedGrid", json.dumps(list(solvedGrid), indent=1))

    for row in range(0, SUDOKU_PUZZLE_SIZE):
        # logInfo("Processing row ...", row)
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            # logInfo("Processing column ...", col)
            gridIndex = (row * SUDOKU_PUZZLE_SIZE) + col
            # row == 8 and col == 7 and
            if(unsolvedGrid[gridIndex]['value'] == 0):
                log('debug', ("solvedGridIndex = ", gridIndex))
                # Unsolved cell. Solve it.
                # logInfo("This cell is unsolved. solving it ...", row, col)
                for possibleValue in range(1, SUDOKU_PUZZLE_SIZE + 1):
                    # for possibleValue in range(1, 2):
                    # logInfo("Checking if " + str(possibleValue) +
                    #      " would fit here ...")
                    outcome = isPossibleValue(
                        possibleValue, solvedGrid, row, col)
                    if(outcome[0] == True):
                        if(outcome[1] == 100):
                            # this is a possible value with 100% confidence. just update the cell
                            logInfo(row, col, "setting to ", possibleValue)
                            solvedGrid[gridIndex]["value"] = possibleValue
                            solvedGrid[gridIndex]["finalized"] = True
                            solvedGrid[gridIndex]["impossibleValues"] = [x for x in range(1,SUDOKU_PUZZLE_SIZE +1) if x != possibleValue]
                        elif(outcome[1] > 0):
                            if possibleValue not in solvedGrid[gridIndex]['possibleValues']:
                                solvedGrid[gridIndex]['possibleValues'].append(
                                    possibleValue)
                    elif(outcome[0] == False and outcome[1] == 100):
                        # this is an impossible value with 100% confidence. just add to array
                        logInfo(row, col, "level = ", level, "Adding", possibleValue,
                                "to impossibleValues")

                        if (possibleValue not in solvedGrid[gridIndex]['impossibleValues']):
                            solvedGrid[gridIndex]['impossibleValues'].append(
                                possibleValue)
                        else:
                            logInfo(row, col, gridIndex, "level = ", level, "Value", possibleValue,
                                    "already exists", solvedGrid[gridIndex]['impossibleValues'])

                if(len(solvedGrid[gridIndex]['impossibleValues']) == SUDOKU_PUZZLE_SIZE - 1):
                    # these are  having exactly 8 impossible values indicating that only one possible value is there
                    # find that value and set it directly
                    possibleValues = [x for x in range(
                        1, SUDOKU_PUZZLE_SIZE + 1) if x not in solvedGrid[gridIndex]['impossibleValues']]
                    # logInfo("Possible Values = ", solvedGrid[gridIndex]['impossibleValues'], range(1, SUDOKU_PUZZLE_SIZE + 1), possibleValues)
                    if(len(possibleValues) >= 1):
                        solvedGrid[gridIndex]['value'] = possibleValues[0]
                        solvedGrid[gridIndex]['finalized'] = True
    if(isPuzzleSolved(solvedGrid)):
        logInfo("Solved ...", json.dumps(
            list(divide_chunks([cell['value'] for cell in solvedGrid], 9)), indent=4))
        finalize(solvedGrid, level)
        logInfo("*****SOLVED*****")
    else:
        if(level < config.MAX_ATTEMPTS - 1):
            logInfo("Attempting again ...", g_percent_complete)
            g_prev_percent_complete = g_percent_complete - 1
            if(g_percent_complete == g_prev_percent_complete):
                log("error", "STAGNATED at %f%% ..." % g_percent_complete)
                finalize(solvedGrid, level)
            else:
                solve(solvedGrid, level + 1)
        else:
            finalize(solvedGrid, level)
            log("error", "****COULD NOT SOLVE IN %d ATTEMPTS****" %
                (config.MAX_ATTEMPTS))


def finalize(grid, level):
    storePuzzleState(grid)
    printGridState(grid, "Level-" + str(level) + "-" +
                   str(g_percent_complete) + "% complete", "a")


def storePuzzleState(grid):
    with open('output.json', 'w') as f:
        json.dump(grid, f, indent=4)


def test():
    for row in range(0, SUDOKU_PUZZLE_SIZE):
        for col in range(0, SUDOKU_PUZZLE_SIZE):
            logInfo("subcube of ", row, col, "=", getSubcubeByRowCol(row, col))

    logInfo(getCellsBySubcubeNumber(5))


def diff():
    list1 = [1, 2, 3, 4, 5, 6, 8, 9]
    list2 = range(1, 10)
    logInfo(list1, list2)
    value = [x for x in list2 if x not in list1]
    logInfo(value)


logInfo("Starting Sudoku Solver ...")
puzzle = generatePuzzle()
logInfo(puzzle)
checkGrid(puzzle)
# test()
# solved = isPuzzleSolved(formatGrid(puzzle))
# logInfo(solved)
start_time = monotonic()
# logInfo(json.dumps(formatGrid(puzzle),indent=1))
##################################################################
puzzle = formatGrid(puzzle)
g_percent_complete = calculatePercentComplete(puzzle)
printGridState(puzzle, "INITIAL STATE - " +
               str(g_percent_complete) + "% complete", "w")
solve(puzzle, 0)
##################################################################
logInfo(f"Run time {monotonic() - start_time} seconds")
# diff()
# logInfo(calculatePercentComplete(formatGrid(puzzle)))
print("==> See main.log for log output")
print("==> See output.json for puzzle state")
# print(getCellsBySubcubeNumberExcludingPlane(0, "x", 0))
# printGridState(formatGrid(puzzle))
