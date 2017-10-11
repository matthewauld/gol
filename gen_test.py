

def generate_binary_grid(gridsize):
    results = []

    grid = [0 for x in range(gridsize**2)]     # Generates

    for x in range((2**(gridsize)**2)-1):
        grid[0] += 1

        for index, entry in enumerate(grid):

            if entry > 1:
                grid[index] = 0
                grid[index+1] += 1
            else:
                break
        new_grid = grid
        results.append(new_grid)
    return(results)
