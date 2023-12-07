from functools import total_ordering

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

@total_ordering
class Card:
    def __init__(self, name, with_joker=False):
        ranks_order = {str(i):i for i in range(2,10)}
        ranks_order = {**ranks_order, **{'T':10,'J':11,'Q':12,'K':13,'A':14}}
        if with_joker:
            ranks_order['J'] = 1
        self.name = name
        self.rank = ranks_order[name]

    def __repr__(self):
        return f'card {self.name} ({self.rank})'
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __lt__(self, other):
        return self.rank < other.rank


@total_ordering
class Hand:
    def __init__(self, line):
        self.line, bid = line.split(' ')
        self.bid = int(bid)
        self.cards = [Card(s) for s in self.line]
        type_check = {}
        for s in self.line:
            try:
                type_check[s] += 1
            except KeyError:
                type_check[s] = 1
        if 5 in type_check.values():
            self.type, self.strength = 'fiv5 of a kind', 7 
        elif 4 in type_check.values():
            self.type, self.strength = '4our of a kind', 6
        elif (3 in type_check.values()) & (2 in type_check.values()):
            self.type, self.strength = 'full house', 5
        elif 3 in type_check.values():
            self.type, self.strength = 'thr33 of a kind', 4
        elif '22' in ''.join(sorted([str(i) for i in type_check.values()])):
            self.type, self.strength = 'two pair', 3
        elif 2 in type_check.values():
            self.type, self.strength = 'one pair', 2
        else:
            self.type, self.strength = 'high card', 1

    def __repr__(self):
        return f'hand {self.line} w/ bid {self.bid} ({self.type})'
    
    def __eq__(self, other):
        return [self.strength] + [card.rank for card in self.cards] == [other.strength] + [card.rank for card in other.cards]
        #return (self.strength == other.strength) & (sum([self.cards[i] == other.cards[i] for i in range(5)]) == 5)
    
    def __lt__(self, other):
        return [self.strength] + [card.rank for card in self.cards] < [other.strength] + [card.rank for card in other.cards]


@total_ordering
class HandWithJokers(Hand):
    def __init__(self, line):
        self.line, bid = line.split(' ')
        self.bid = int(bid)
        self.cards = [Card(s, with_joker=True) for s in self.line]
        type_check = {}
        for s in self.line:
            try:
                type_check[s] += 1
            except KeyError:
                type_check[s] = 1
        if len(type_check) > 1:
            try:
                add = type_check.pop('J')
                type_check[max(type_check, key=type_check.get)] += add
            except KeyError:
                pass
        if 5 in type_check.values():
            self.type, self.strength = 'fiv5 of a kind', 7 
        elif 4 in type_check.values():
            self.type, self.strength = '4our of a kind', 6
        elif (3 in type_check.values()) & (2 in type_check.values()):
            self.type, self.strength = 'full house', 5
        elif 3 in type_check.values():
            self.type, self.strength = 'thr33 of a kind', 4
        elif '22' in ''.join(sorted([str(i) for i in type_check.values()])):
            self.type, self.strength = 'two pair', 3
        elif 2 in type_check.values():
            self.type, self.strength = 'one pair', 2
        else:
            self.type, self.strength = 'high card', 1


class CamelCardsGame:
    def __init__(self, filename):
        self.hands = [Hand(line) for line in read_input(filename, split=True)]
        self.hands_with_jokers = [HandWithJokers(line) for line in read_input(filename, split=True)]

    def run_part1(self):
        self.hands.sort()
        return sum([self.hands[i].bid * (i+1) for i in range(len(self.hands))])
    
    def run_part2(self):
        self.hands_with_jokers.sort()
        return sum([self.hands_with_jokers[i].bid * (i+1) for i in range(len(self.hands_with_jokers))])


print(CamelCardsGame('input.txt').run_part1())
print(CamelCardsGame('input.txt').run_part2())
