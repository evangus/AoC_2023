def read_input(filename, split = False, convert_to_int = False, sep = '\n'):
    f = open(filename)
    data = f.read()[:-1]
    f.close()
    if split:
        data = data.split(sep)
    if convert_to_int:
        data = [int(item) for item in data]
    return data

class GardenStepCounter:
    def __init__(self,filename):
        self.map = read_input(filename)
        self.plots = set()
        for i,line in enumerate(self.map.split('\n')):
            for j,s in enumerate(line):
                if s != '#':
                    self.plots.add((i,j))
                    if s == 'S':
                        self.start = (i,j)
        self.increments = {(0,1),(1,0),(-1,0),(0,-1)}
        self.odd_steps = set()
        self.even_steps = set()
        self.even_steps.add(self.start)
        self.plots_in_reach = {1:self.odd_steps, 0:self.even_steps}

    def run_part1(self, n):
        for i in range(1,n+1):
            for loc in self.plots_in_reach[(i - 1) % 2]:
                for d in self.increments:
                    new_loc = (loc[0]+d[0],loc[1]+d[1])
                    if new_loc in self.plots:
                        self.plots_in_reach[i % 2].add(new_loc)
        return(len(self.plots_in_reach[n % 2]))
    

print(GardenStepCounter('input.txt').run_part1(64))
