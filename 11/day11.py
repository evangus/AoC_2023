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

class Universe:
    def __init__(self, filename):
        self.map = read_input(filename)
        self.row_length = self.map.find('\n') + 1
        self.row_count = int((len(self.map) + 1) / self.row_length)
        self.galaxies = {}
        start = 0
        while self.map.find('#',start) != -1:
            self.galaxies[len(self.galaxies)] = self.map.find('#',start)
            start = self.map.find('#',start) + 1
        self.paths = {(i,j):None for i in range(len(self.galaxies)) for j in range(i+1,len(self.galaxies))}

    def update_map(self):
        s = ('.' * (self.row_length - 1) + '\n') * self.row_count
        for i in self.galaxies.values():
            s = s[:i] + '#' + s[i+1:]
        self.map = s

    def expand(self, multiplier = 2):
        rows_to_expand = list(range(self.row_count))
        columns_to_expand = list(range(self.row_length - 1))

        for i in self.galaxies.values():
            try:
                rows_to_expand.remove(i // self.row_length)
            except ValueError:
                pass
            try:
                columns_to_expand.remove(i % self.row_length)
            except ValueError:
                pass

        for i in self.galaxies:
            row = self.galaxies[i] // self.row_length
            column = self.galaxies[i] % self.row_length
            new_row = row + sum([row > j for j in rows_to_expand]) * (multiplier - 1)
            new_column = column + sum([column > k for k in columns_to_expand]) * (multiplier - 1)

            self.galaxies[i] = new_row * (self.row_length + len(columns_to_expand) * (multiplier - 1)) + new_column

        self.row_count += len(rows_to_expand) * (multiplier - 1)
        self.row_length += len(columns_to_expand) * (multiplier - 1)

        #self.update_map()

    def calc_paths(self):
        for pair in self.paths:
            dy = abs(self.galaxies[pair[0]] // self.row_length - self.galaxies[pair[1]] // self.row_length)
            dx = abs(self.galaxies[pair[0]] % self.row_length - self.galaxies[pair[1]] % self.row_length)
            self.paths[pair] = dx + dy

    def run_part1(self):
        self.expand()
        self.calc_paths()
        return sum(self.paths.values())
    
    def run_part2(self, multiplier):
        self.expand(multiplier)
        self.calc_paths()
        return sum(self.paths.values())


print(Universe('input.txt').run_part1())
print(Universe('input.txt').run_part2(1000000))
