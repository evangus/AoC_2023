def read_input(filename, split = False, convert_to_int = False, sep = '\n'):
    f = open(filename)
    data = f.read()[:-1]
    f.close()
    if split:
        data = data.split(sep)
    if convert_to_int:
        data = [int(item) for item in data]
    return data

class LargeLagoon:
    def __init__(self, filename):
        self.dig_plan = [DigInstruction(i) for i in read_input(filename,split=True)]
        self.current = (0,0)
        self.map = {self.current: 1}
        self.vertical_edges = {}
        self.increment = {'U':(-1,0),'D':(1,0),'L':(0,-1),'R':(0,1)}

        last_direction = self.dig_plan[-1].direction
        for instruction in self.dig_plan:
            self.vertical_edges[self.current] = ('F'*(last_direction+instruction.direction in ('UR','LD')) 
                                        + '7'*(last_direction+instruction.direction in ('RD','UL')) 
                                        + 'L'*(last_direction+instruction.direction in ('DR','LU')) 
                                        + 'J'*(last_direction+instruction.direction in ('RU','DL')))
            self.dig_trench_side(instruction)
            last_direction = instruction.direction
        self.vertical_edges[self.current] = ('F'*(last_direction+self.dig_plan[0].direction in ('UR','LD')) 
                                        + '7'*(last_direction+self.dig_plan[0].direction in ('RD','UL')) 
                                        + 'L'*(last_direction+self.dig_plan[0].direction in ('DR','LU')) 
                                        + 'J'*(last_direction+self.dig_plan[0].direction in ('RU','DL')))

        self.min_i = min([x[0] for x in self.map.keys()])
        self.max_i = max([x[0] for x in self.map.keys()])
        self.min_j = min([x[1] for x in self.map.keys()])
        self.max_j = max([x[1] for x in self.map.keys()])

    def visualize(self):
        for i in range(self.min_i,self.max_i+1):
            s = ''
            for j in range(self.min_j,self.max_j+1):
                s = s + '#'*((i,j) in self.map) + '.'*((i,j) not in self.map)
            print(s)

    def dig_trench_side(self, instruction):
        for _ in range(instruction.length):
            self.current = (self.current[0] + self.increment[instruction.direction][0],
                            self.current[1] + self.increment[instruction.direction][1])
            self.map[self.current] = 1
            if instruction.direction in 'UD':
                self.vertical_edges[self.current] = '|'

    def dig_lagoon_interior(self):
        edge_counter = 0
        latest_edge = ''
        interior_map = {}
        for i in range(self.min_i, self.max_i+1):
            for j in range(self.min_j,self.max_j+1):
                if ((i,j) in self.vertical_edges):
                    if (latest_edge + self.vertical_edges[(i,j)] not in ['FJ','L7']):
                        edge_counter += 1
                        latest_edge = self.vertical_edges[(i,j)]
                elif ((i,j) not in self.map) & (edge_counter % 2 == 1):
                    interior_map[(i,j)] = 1
        self.map.update(interior_map)
        
    def run_part1(self):
        self.dig_lagoon_interior()
        return sum(self.map.values())
        

class DigInstruction:
    def __init__(self, line):
        self.direction, self.length, self.color = line.split(' ')
        self.length = int(self.length)
        

print(LargeLagoon('input.txt').run_part1())
