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

class MetalPlatform:
    def __init__(self, filename):
        self.surface = read_input(filename)
        self.row_length = self.surface.find('\n') + 1
        self.rows_count = len(self.surface.split('\n'))
        self.cube_rocks = []
        self.rounded_rocks = []
        self.map_rocks('#', self.cube_rocks)
        self.map_rocks('O', self.rounded_rocks)
        
    def map_rocks(self, s, target_array):
        start = 0
        while self.surface.find(s, start) != -1:
            target_array.append(self.surface.find(s, start))
            start = self.surface.find(s, start) + 1

    def remap(self):
        s = ('.' * (self.row_length - 1) + '\n') * self.rows_count
        for i in self.cube_rocks:
            s = s[:i] + '#' + s[i+1:]
        for i in self.rounded_rocks:
            s = s[:i] + 'O' + s[i+1:]
        self.surface = s

    def tilt(self, direction = 'N'):
        increment = {'N':(-1)*self.row_length, 'W':(-1), 'S':self.row_length, 'E':+1}
        order = {'N':0,'W':0,'S':-1,'E':-1}
        rounded_new = []
        while self.rounded_rocks:
            i = self.rounded_rocks.pop(order[direction])
            original_row = i // self.row_length
            while ((i + increment[direction] not in self.cube_rocks) 
                   & (i + increment[direction] not in rounded_new) 
                   & (self.border_condition(i + increment[direction],direction)) 
                   & ((direction in 'NS') | ((i + increment[direction]) // self.row_length == original_row))):
                i += increment[direction]
            rounded_new.append(i)
        self.rounded_rocks = rounded_new
        self.rounded_rocks.sort()

    def border_condition(self, i, direction = 'N'):
        if direction == 'N':
            return i >= 0
        elif direction == 'S':
            return i <= len(self.surface)
        elif direction == 'W':
            return (i % self.row_length >= 0) & (i>=0)
        elif direction == 'E':
            return i % self.row_length < self.row_length - 1
        
    def tilt_cycle(self, n = 1):
        for _ in range(n):
            for i in ['N', 'W', 'S', 'E']:
                self.tilt(i)
        
    def calculate_total_load(self):
        ans = 0
        for i in self.rounded_rocks:
            ans += (self.rows_count - (i // self.row_length))
        return ans
    
    def run_part1(self):
        self.tilt('N')
        return self.calculate_total_load()
    
    def run_part2(self, n):
        self.hashes = {0: hash(tuple(self.rounded_rocks))}
        for i in range(1,n):
            self.tilt_cycle()
            if hash(tuple(self.rounded_rocks)) in self.hashes.values():
                cycle_start = [j for j in self.hashes if self.hashes[j] == hash(tuple(self.rounded_rocks))][0]
                cycle_length = i - cycle_start
                break
            self.hashes[i] = hash(tuple(self.rounded_rocks))
        self.tilt_cycle((1000000000-cycle_start) % cycle_length)
        return self.calculate_total_load()
    
print(MetalPlatform('input.txt').run_part1())
print(MetalPlatform('input.txt').run_part2(200))
