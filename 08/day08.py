from math import lcm

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

class SandstormNetwork:
    def __init__(self, filename):
        self.instruction, nodes_to_parse = read_input(filename, split=True, sep='\n\n')
        self.nodes = {}
        for line in nodes_to_parse.split('\n'):
            key, turns = line.split(' = ')
            self.nodes[key] = turns[1:-1].split(', ')

    def run_part1(self):
        current_node = 'AAA'
        step = 0
        while current_node!='ZZZ':
            if self.instruction[step % len(self.instruction)] == 'R':
                current_node = self.nodes[current_node][-1]
            elif self.instruction[step % len(self.instruction)] == 'L':
                current_node = self.nodes[current_node][0]
            step += 1
        return step
    
    def run_part2(self):
        current_nodes = [i for i in self.nodes if i[-1]=='A']
        node_patterns = []
        for current_node in current_nodes:
            node_pattern = []
            step = 0
            for _ in range(100000):
                if current_node[-1] == 'Z':
                    node_pattern.append(step)
                if self.instruction[step % len(self.instruction)] == 'R':
                    current_node = self.nodes[current_node][-1]
                elif self.instruction[step % len(self.instruction)] == 'L':
                    current_node = self.nodes[current_node][0]
                step += 1
            node_patterns.append(node_pattern)
        return lcm(*[i[0] for i in node_patterns])


print(SandstormNetwork('input.txt').run_part1())
print(SandstormNetwork('input.txt').run_part2())
