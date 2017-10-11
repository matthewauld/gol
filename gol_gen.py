
import pickle
from gol import GOL


def test_iterations(structuresize, gridsize, rounds, failisblank = True,failnochange = False):
    '''
    Generates a list of all possible structures based on structuresize (a sqare grid)
    tests them for rounds, and returns the ones that pass
    '''
    teststructures = generate_binary_grid(structuresize)
    results = []
    for structure in teststructures:
        game = GOL(gridsize,gridsize)
        game.add_structure(structure, xoffset=int(gridsize/2),yoffset=int(gridsize/2))
        result = game.test(rounds, failisblank = failisblank,failnochange = failnochange)

        if result == True:
            results.append(structure)
    return results

def test_list(struclist, gridsize, rounds,failisblank = True,failnochange = False):
    '''
    Takes a list of structures, places each of them on the gameboard in the lower right
    quadrent, and tests it for x number of rounds. Returns a list of strucures that have passed
    '''
    results=[]
    for structure in struclist:
        game = GOL(gridsize,gridsize)
        game.add_structure(structure,xoffset=int(gridsize/2),yoffset=int(gridsize/2))
        result = game.test(rounds, failisblank = failisblank,failnochange = failnochange)
        if result == True:
            results.append(structure)
    return results

def rotate_structure(structure):
    '''
    Rotates a structre clockwise once.
    '''


def generate_binary_grid(gridsize):
    '''
    Generates all possible iterations of a square binary matrix. Gridsize is
    the size of the side of the square - eg. 3 generates all 3x3 binary matrixs
    '''
    results = []

    grid = [0 for x in range(gridsize**2)]     # Generates gird of all zeros

    for x in range((2**(gridsize)**2)-1): # Iterates though
        grid[0] += 1

        for index, entry in enumerate(grid):

            if entry > 1:
                grid[index] = 0
                grid[index+1] += 1
            else:
                break
        new_grid = [grid[i:i+gridsize] for i in range(0,len(grid),gridsize)]
        results.append(new_grid)
    return(results)
