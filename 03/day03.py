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

class GondolaLiftEngine:
    def __init__(self, filename):
        self.engine_schematic = ['.' + line + '.' for line in read_input(filename,split=True)]
        self.engine_schematic = ['.'*len(self.engine_schematic[0])] + self.engine_schematic + ['.'*len(self.engine_schematic[0])]
        self.digit_locations = []
        self.star_locations = []
        for i, line in enumerate(self.engine_schematic):
            for j, s in enumerate(line):
                if s.isdigit():
                    if (self.engine_schematic[i][j-1].isdigit()==False):
                        self.digit_locations.append((i,j))
                    if (self.engine_schematic[i][j+1].isdigit()==False):
                        self.digit_locations.append((i,j))
                elif s == '*':
                    self.star_locations.append((i,j))
        self.gear_dict = {}
        
        
    def return_number(self, loc1, loc2):
        return int(self.engine_schematic[loc1[0]][loc1[1]:loc2[1]+1])
    
    def check_number(self, loc1, loc2):
        i, j1 = loc1
        j2 = loc2[1]
        s = self.engine_schematic[i-1][j1-1:j2+2]+self.engine_schematic[i][j1-1:j2+2]+self.engine_schematic[i+1][j1-1:j2+2]
        return bool(len(s.translate({ord(i): None for i in '1234567890.'})))

    def run_part1(self):
        return sum(
            [self.check_number(*self.digit_locations[i:i+2]) * self.return_number(*self.digit_locations[i:i+2]) 
             for i in range(0,len(self.digit_locations),2)]
            )
    
    def run_part2(self):
        for k in range(0, len(self.digit_locations), 2):
            (i1,j1),(_,j2) = self.digit_locations[k:k+2]
            for i in range(i1-1,i1+2):
                for j in range(j1-1,j2+2):
                    if self.engine_schematic[i][j] == '*':
                        try:
                            self.gear_dict[(i,j)].append(self.return_number(*self.digit_locations[k:k+2]))
                        except KeyError:
                            self.gear_dict[(i,j)] = [self.return_number(*self.digit_locations[k:k+2])]

        return sum([self.gear_dict[gear][0]*self.gear_dict[gear][1] 
                    for gear in self.gear_dict if len(self.gear_dict[gear]) == 2])


print(GondolaLiftEngine('sample.txt').run_part1() == 4361)
print(GondolaLiftEngine('sample.txt').run_part2() == 467835)
print(GondolaLiftEngine('input.txt').run_part1())
print(GondolaLiftEngine('input.txt').run_part2())
