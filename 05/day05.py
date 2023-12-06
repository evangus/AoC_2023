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

class Almanac:
    def __init__(self, filename):
        self.seeds, *self.maps = read_input(filename,split=True,sep='\n\n')
        self.seeds = [int(i) for i in self.seeds.split(' ')[1:]]
        self.seed_ranges = [range(self.seeds[2*i], self.seeds[2*i]+self.seeds[2*i+1]) 
                            for i in range(int(len(self.seeds)/2))]
        self.maps = [ConvertionMap(line) for line in self.maps]

    @staticmethod
    def ranges_overlap(x1:int,x2:int,y1:int,y2:int):
        ans = {
            'result': min(y2,x2) > max(x1,y1),
            'overlap':[max(y1,x1), min(x2,y2)] * (min(y2,x2) > max(x1,y1)),
            'rest':[[min(x1,y1),max(x1,y1)] * (x1<y1), [min(x2,y2), max(x2,y2)] * (x2>y2)]
            }    
        ans['rest'] = [i for i in ans['rest'] if len(i)>0]
        return ans
        
    def run_part1(self):
        converted_seeds = self.seeds
        for converting_map in self.maps:
            converted_seeds = [converting_map.convert(i) for i in converted_seeds]
        return min(converted_seeds)


class ConvertionMap:
    def __init__(self, line):
        self.name, raw_mapping = line.split(':\n')
        self.mapping = {}
        for mapping_rule in raw_mapping.split('\n'):
            dest_start, source_start, range_length = [int(i) for i in mapping_rule.split(' ')]
            self.mapping[range(source_start, source_start+range_length)] = dest_start-source_start

    def convert(self, i):
        for rule in self.mapping:
            if i in rule:
                return i + self.mapping[rule]
        return i
            
print(f"{Almanac('input.txt').run_part1()}")