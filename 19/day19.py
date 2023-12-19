
def read_input(filename, split = False, convert_to_int = False, sep = '\n'):
    f = open(filename)
    data = f.read()[:-1]
    f.close()
    if split:
        data = data.split(sep)
    if convert_to_int:
        data = [int(item) for item in data]
    return data

class Part:
    def __init__(self, line) -> None:
        self.x, self.m, self.a, self.s = [int(i.split('=')[-1]) for i in line[1:-1].split(',')]
        self.status = 'in'

    def __repr__(self) -> str:
        return f'part x: {self.x} m: {self.m} a: {self.a} s: {self.s}'
        

class Workflow:
    def __init__(self, line) -> None:
        self.name, rules = line[:-1].split('{')
        self.rules = rules.split(',')

    def __repr__(self) -> str:
        return f'wrkflw {self.name} | {self.rules}'

    def apply_rule(self, part, rule):
        if ':' not in rule:
            return rule
        elif '<' in rule:
            comparison, target = rule.split(':')
            property, value = comparison.split('<')
            if {'x':part.x,'m':part.m,'a':part.a,'s':part.s}[property] < int(value):
                return target
        elif '>' in rule:
            comparison, target = rule.split(':')
            property, value = comparison.split('>')
            if {'x':part.x,'m':part.m,'a':part.a,'s':part.s}[property] > int(value):
                return target

    def process_part(self, part):
        for rule in self.rules:
            a = self.apply_rule(part, rule)
            if a:
                return a


class RelentlessAvalancheOrganizer:
    def __init__(self,filename) -> None:
        self.workflows, self.parts = [i.split('\n') for i in read_input(filename,split=True,sep='\n\n')]
        self.workflows = [Workflow(i) for i in self.workflows]
        self.parts = [Part(i) for i in self.parts]
        
    def run(self):
        for part in self.parts:
            while part.status not in 'RA':
                part.status = [i for i in self.workflows if i.name == part.status][0].process_part(part)

    def run_part1(self):
        self.run()
        return sum([i.x + i.m + i.a + i.s for i in self.parts if i.status == 'A'])
    

print(RelentlessAvalancheOrganizer('input.txt').run_part1())
