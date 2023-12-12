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

class HotSpringsField:
    def __init__(self, filename):
        self.rows = [HotSpringsRow(i) for i in read_input(filename, split=True)]

    def run_part1(self):
        return sum([i.recursive_pattern_check(i.map) for i in self.rows])

class HotSpringsRow:
    def __init__(self, line):
        self.map, pattern = line.split(' ')
        self.pattern = [int(i) for i in pattern.split(',')]
        while self.map.find('..') != -1:
            self.map = self.map.replace('..', '.')
        while self.map[0] == '.':
            self.map = self.map[1:]
        while self.map[-1] == '.':
            self.map = self.map[:-1]

    def check_pattern(self, s):
        return [len(i) for i in s.split('.') if i!=''] == self.pattern
    
    def recursive_pattern_check(self, s):
        if s.find('?') == -1:
            return self.check_pattern(s)
        else:
            i = s.find('?')
            return self.recursive_pattern_check(s[:i]+'.'+s[i+1:]) + self.recursive_pattern_check(s[:i]+'#'+s[i+1:])

    def __repr__(self):
        return self.map + ' || ' + str(self.pattern) + '\n'
    

print(HotSpringsField('input.txt').run_part1())
