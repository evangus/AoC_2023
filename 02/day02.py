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

class BagWithCubes:
    def __init__(self, filename, red_cubes=12,green_cubes=13,blue_cubes=14):
        self.red_cubes = red_cubes
        self.green_cubes = green_cubes
        self.blue_cubes = blue_cubes
        self.games_log = read_input(filename, split=True)
        self.games = []
        for line in self.games_log:
            self.games.append(CubeGame(line))
        self.part1_answer = 0

    def run_part1(self):
        for game in self.games:
            if (game.r_max <= self.red_cubes) & (game.g_max <= self.green_cubes) & (game.b_max <= self.blue_cubes):
                self.part1_answer += game.id
        return self.part1_answer
    
    def run_part2(self):
        return sum([game.power for game in self.games])


class CubeGame:
    def __init__(self, line):
        self.id = int(line.split(': ')[0].split(' ')[-1])
        self.r_max = max([int(s.split(' ')[-1]) for s in line.split(' red')[:-1]])
        self.g_max = max([int(s.split(' ')[-1]) for s in line.split(' green')[:-1]])
        self.b_max = max([int(s.split(' ')[-1]) for s in line.split(' blue')[:-1]])
        self.power = self.r_max * self.g_max * self.b_max

    def __repr__(self):
        return f'Game {self.id}: max of {self.r_max} red, {self.g_max} green, {self.b_max} blue cubes'


print(BagWithCubes('input.txt').run_part1())
print(BagWithCubes('input.txt').run_part2())
