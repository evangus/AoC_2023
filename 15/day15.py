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

class LavaProductionFacility:
    def __init__(self, filename):
        self.initialization_sequence = [HolidayASCIIStringHelper(i) for i in read_input(filename,split=True,sep=',')]
        self.lens_arrangement_sequence = [HolidayASCIIStringHelperManualArrangementProcedure(i) for i in read_input(filename,split=True,sep=',')]
        self.lens_boxes = {i:[] for i in range(256)}

    def run_part1(self):
        return sum([i.value for i in self.initialization_sequence])
    
    def run_arrangement_sequence(self):
        for procedure in self.lens_arrangement_sequence:
            if procedure.type == '=':
                try:
                    loc = [i for i,j in enumerate(self.lens_boxes[procedure.box_id]) if j.label == procedure.label][0]
                    self.lens_boxes[procedure.box_id][loc] = procedure
                except IndexError:
                    self.lens_boxes[procedure.box_id].append(procedure)
            elif procedure.type == '-':
                try:
                    loc = [i for i,j in enumerate(self.lens_boxes[procedure.box_id]) if j.label == procedure.label][0]
                    del self.lens_boxes[procedure.box_id][loc]
                except IndexError:
                    pass

        for id in range(256):
            if len(self.lens_boxes[id]) == 0:
                del self.lens_boxes[id]

    def calc_focusing_power(self):
        power = 0
        for i in self.lens_boxes:
            for j, lens in enumerate(self.lens_boxes[i]):
                power += (i+1) * (j+1) * lens.focal_length
        return power
    
    def run_part2(self):
        self.run_arrangement_sequence()
        return self.calc_focusing_power()


class HolidayASCIIStringHelper:
    def __init__(self, line):
        self.value = 0
        self.string = line
        for s in line:
            self.value += ord(s)
            self.value = self.value * 17
            self.value = self.value % 256
    
    def __repr__(self):
        return f'{self.string} => {self.value}'
    
class HolidayASCIIStringHelperManualArrangementProcedure:
    def __init__(self, line):
        self.string = line
        self.type = '=' * ('=' in line) + '-' * ('-' in line)
        self.label = self.string.split(self.type)[0]
        self.box_id = HolidayASCIIStringHelper(self.label).value
        if self.type == '=':
            self.focal_length = int(self.string.split('=')[-1])

    def __repr__(self):
        if self.type == '=':
            return f'[{self.label} {self.focal_length}]'
        else:
            return f'[{self.label} -]'
        

print(LavaProductionFacility('input.txt').run_part1())
print(LavaProductionFacility('input.txt').run_part2())
