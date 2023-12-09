import numpy as np

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

def recursive_derivative(history:list) -> int:
    if not np.diff(history).any():
        return history[-1]
    else:
        return history[-1] + recursive_derivative(np.diff(history))

def backwards_recursive_derivative(history:list) -> int:
    if not np.diff(history).any():
        return history[0]
    else:
        return history[0] - backwards_recursive_derivative(np.diff(history))

class OasisAndSandInstabilitySensor:
    def __init__(self, filename):
        self.values = [ValueRecord(i) for i in read_input(filename,split=True)]

    def run_part1(self):
        return sum([recursive_derivative(value.history) for value in self.values])
    
    def run_part2(self):
        return sum([backwards_recursive_derivative(value.history) for value in self.values])


class ValueRecord:
    def __init__(self, line):
        self.history = [int(i) for i in line.split(' ')]

    def __repr__(self):
        return str(self.history)
    

print(OasisAndSandInstabilitySensor('input.txt').run_part1())
print(OasisAndSandInstabilitySensor('input.txt').run_part2())
