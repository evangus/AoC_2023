def read_input(filename, split = False, convert_to_int = False, sep = '\n'):
    f = open(filename)
    raw = f.read()[:-1]
    f.close()
    data = raw
    if split:
        data = data.split(sep)
    if convert_to_int:
        data = [int(item) for item in data]
    return data

class MetalPipesArea:
    def __init__(self, filename):
        self.map = read_input(filename)
        
    def follow_pipe(self, coordinate_1, coordinate_2):
        row_length = self.map.find('\n') + 1
        if self.map[coordinate_2] == '|':
            if coordinate_1 < coordinate_2:
                return coordinate_2 + row_length
            elif coordinate_1 > coordinate_2:
                return coordinate_2 - row_length
        elif self.map[coordinate_2] == '-':
            if coordinate_1 < coordinate_2:
                return coordinate_2 + 1
            elif coordinate_1 > coordinate_2:
                return coordinate_2 - 1
        elif self.map[coordinate_2] == 'L':
            if coordinate_1 < coordinate_2:
                return coordinate_2 + 1
            elif coordinate_1 > coordinate_2:
                return coordinate_2 - row_length
        elif self.map[coordinate_2] == 'J':
            if coordinate_1 < coordinate_2 - 1:
                return coordinate_2 - 1
            elif coordinate_1 == coordinate_2 - 1:
                return coordinate_2 - row_length
        elif self.map[coordinate_2] == '7':
            if coordinate_1 < coordinate_2:
                return coordinate_2 + row_length
            elif coordinate_1 > coordinate_2:
                return coordinate_2 - 1
        elif self.map[coordinate_2] == 'F':
            if coordinate_1 > coordinate_2 + 1:
                return coordinate_2 + 1
            elif coordinate_1 == coordinate_2 + 1:
                return coordinate_2 + row_length
    
    def find_loop(self):
        first_steps = []
        row_length = self.map.find('\n') + 1
        start = self.map.find('S')

        if self.map[start - row_length] in '|7F':
            first_steps.append(start - row_length)
        if self.map[start - 1] in '-LF':
            first_steps.append(start - 1)
        if self.map[start + 1] in '-J7':
            first_steps.append(start + 1)
        if self.map[start + row_length] in '|LJ':
            first_steps.append(start + row_length)

        self.path_1 = [start, first_steps[0]]
        self.path_2 = [start, first_steps[-1]]
        
        while self.path_1[-1] != self.path_2[-1]:
            self.path_1.append(self.follow_pipe(*self.path_1[-2:]))
            self.path_2.append(self.follow_pipe(*self.path_2[-2:]))

    def run_part1(self):
        self.find_loop()
        return len(self.path_1) - 1

    def run_part2(self):
        self.find_loop()
        #inside_loop = []
        #outside_loop = []
        count = 0
        edge_counter = 0
        latest_edge = ''
        for i in range(len(self.map)):
            if (i in self.path_1 + self.path_2):
                if (self.map[i] in 'SF7|LJ') & (latest_edge + self.map[i] not in ['FJ','L7']):
                    edge_counter += 1
                    latest_edge = self.map[i]
            elif self.map[i] == '\n':
                pass
            else:
                if edge_counter % 2 == 1:
                    count += 1
        #            inside_loop.append(i)
        #        else:
        #            outside_loop.append(i)
        
        #s = self.map
        #for i in inside_loop:
        #    s = s[:i] + '*' + s[i+1:]
        #for i in outside_loop:
        #    s = s[:i] + '.' + s[i+1:]
        #print(s)
        return count

print(MetalPipesArea('input.txt').run_part1())
print(MetalPipesArea('input.txt').run_part2())
