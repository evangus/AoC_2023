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

class TrebuchetCalibrator:
    def __init__(self, filename):
        self.lines = read_input(filename, split=True)
        self.calibration_sum = 0

    def run(self):
        self.calibration_sum = 0
        for line in self.lines:
            calibration_value = ''
            for s in line:
                if s.isdigit():
                    calibration_value += s
                    break
            for s in line[::-1]:
                if s.isdigit():
                    calibration_value += s
                    break
            self.calibration_sum += int(calibration_value)
        return self.calibration_sum

TrebuchetCalibrator('input.txt').run()

class SpelledOutTrebuchetCalibrator:
    def __init__(self, filename):
        self.lines = read_input(filename, split=True)
        self.calibration_sum = 0
        
    @staticmethod
    def parse_line(line):
        number_map = {'one': '1' , 'two': '2', 'three': '3', 'four': '4', 'five': '5', 
                      'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
        
        possible_first_digit_indexes = {}
        for i, s in enumerate(line):
            if s.isdigit():
                possible_first_digit_indexes[i] = s
                break
        for key in number_map:
            if line.find(key) >= 0:
                possible_first_digit_indexes[line.find(key)] = number_map[key]

        possible_second_digit_indexes = {}

        for s in line[::-1]:
            if s.isdigit():
                possible_second_digit_indexes[line.rfind(s)] = s
                break

        for key in number_map:
            if line.rfind(key) >= 0:
                possible_second_digit_indexes[line.rfind(key)] = number_map[key]
        
        return int(possible_first_digit_indexes[min(possible_first_digit_indexes)] 
                   + possible_second_digit_indexes[max(possible_second_digit_indexes)])
    
    def run(self):
        self.calibration_sum = 0
        for line in self.lines:
            self.calibration_sum += SpelledOutTrebuchetCalibrator.parse_line(line)
        return(self.calibration_sum)
    
SpelledOutTrebuchetCalibrator('input.txt').run()
