import sys
sys.setrecursionlimit(10000)

def read_input(filename, split = False, convert_to_int = False, sep = '\n'):
    f = open(filename)
    data = f.read()[:-1]
    f.close()
    if split:
        data = data.split(sep)
    if convert_to_int:
        data = [int(item) for item in data]
    return data

class Contraption:
    def __init__(self, filename) -> None:
        self.map = read_input(filename)
        self.row_length = self.map.find('\n') + 1
        self.rows_count = len(self.map.split('\n'))
        self.energized = {}
        self.increment = {'U':(-1)*self.row_length, 'D':self.row_length, 'L':-1, 'R':1}

    def print_energized(self):
        s = self.map
        for i in self.energized.keys():
            s = s[:i] + '#' + s[i+1:]
        print(s)

    def launch_beam(self, location, direction):
        try:
            if direction in self.energized[location]:
                return
            else:
                self.energized[location].add(direction)
        except KeyError:
            self.energized[location] = {direction}
        
        new_location = location + self.increment[direction]
        
        if (((location // self.row_length == 0) & (direction == 'U')) 
            or ((location % self.row_length == 0) & (direction == 'L'))
            or ((location // self.row_length == self.rows_count - 1) & (direction == 'D'))
            or ((location % self.row_length == self.row_length - 2) & (direction == 'R'))):
            return
        elif self.map[new_location] == '.':
            self.launch_beam(new_location, direction)
        elif self.map[new_location] == '-':
            if direction in 'LR':
                self.launch_beam(new_location, direction)
            else:
                self.launch_beam(new_location, 'L')
                self.launch_beam(new_location, 'R')
        elif self.map[new_location] == '|':
            if direction in 'UD':
                self.launch_beam(new_location, direction)
            else:
                self.launch_beam(new_location, 'U')
                self.launch_beam(new_location, 'D')
        elif self.map[new_location] == '/':
            if direction == 'U':
                self.launch_beam(new_location, 'R')
            elif direction == 'D':
                self.launch_beam(new_location, 'L')
            elif direction == 'L':
                self.launch_beam(new_location, 'D')
            elif direction == 'R':
                self.launch_beam(new_location, 'U')
        elif self.map[new_location] == '\\':
            if direction == 'U':
                self.launch_beam(new_location, 'L')
            elif direction == 'D':
                self.launch_beam(new_location, 'R')
            elif direction == 'L':
                self.launch_beam(new_location, 'U')
            elif direction == 'R':
                self.launch_beam(new_location, 'D')

    def run_part1(self):
        self.launch_beam(0, 'R')
        return len(self.energized)
    
    def run_part2(self):
        max_energized = 0
        for i in range(self.row_length - 1):
            self.energized = {}
            self.launch_beam(i,'D')
            if len(self.energized) > max_energized:
                max_energized = len(self.energized)
        for i in range(self.row_length - 1):
            self.energized = {}
            self.launch_beam(self.row_length * (self.rows_count - 1) + i, 'U')
            if len(self.energized) > max_energized:
                max_energized = len(self.energized)
        for i in range(self.rows_count):
            self.energized = {}
            self.launch_beam(i * self.row_length, 'R')
            if len(self.energized) > max_energized:
                max_energized = len(self.energized)
        for i in range(self.rows_count):
            self.energized = {}
            self.launch_beam(i * self.row_length + self.row_length - 1, 'L')
            if len(self.energized) > max_energized:
                max_energized = len(self.energized)
        return max_energized


print(Contraption('input.txt').run_part1())
print(Contraption('input.txt').run_part2())
