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

class ScratchcardsPile:
    def __init__(self, filename):
        self.scratchcards = [Scratchcard(line) for line in read_input(filename, split=True)]
        self.cards_won = {i.id:1 for i in self.scratchcards}

    def run_part1(self):
        return sum([card.value for card in self.scratchcards])
    
    def run_part2(self):
        self.cards_won = {i.id:1 for i in self.scratchcards}
        for card in self.scratchcards:
            for i in range(card.id + 1, card.id + card.matching_numbers_count + 1):
                self.cards_won[i] += self.cards_won[card.id]
        return sum(self.cards_won.values())

class Scratchcard:
    def __init__(self, line):
        self.id = int(line.split(':')[0].split(' ')[-1])
        self.winning_numbers =  {int(i) for i in line.split(':')[-1].split('|')[0].split(' ') if i!=''}
        self.present_numbers =  {int(i) for i in line.split(':')[-1].split('|')[-1].split(' ') if i!=''}
        self.matching_numbers_count = len(self.winning_numbers.intersection(self.present_numbers))
        self.value = int((self.matching_numbers_count!=0) * 2**(self.matching_numbers_count-1))

    def __repr__(self):
        return f'Card #{self.id}'


print(
    ScratchcardsPile('input.txt').run_part1(),
    ScratchcardsPile('input.txt').run_part2()
)
