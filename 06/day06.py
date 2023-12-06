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

class BoatRacingCompetition:
    def __init__(self, filename:str):
        times, distances = read_input(filename, split=True)
        self.races =  [BoatRace(int(i)) for i in times.split(':')[-1].split(' ') if i!='']
        for j,k in enumerate([int(i) for i in distances.split(':')[-1].split(' ') if i!='']):
            self.races[j].distance = k

    def run_races(self):
        for i in self.races:
            i.model_race()
            print(i.min_to_win, i.max_to_win)

    def run_part1(self):
        ans = 1
        for race in self.races:
            ans *= race.return_error_margin()
        return ans
            

class BoatRace:
    def __init__(self, time=0, distance=0):
        self.time, self.distance = time, distance
        self.min_to_win:int
        self.max_to_win:int

    def model_race(self):
        f = 'below_record'
        for wait_time in range(self.time):
            speed = wait_time
            if (speed*(self.time-wait_time) > self.distance) & (f == 'below_record'):
                self.min_to_win = wait_time
                f = 'over_record'
            if (speed*(self.time-wait_time) <= self.distance) & (f == 'over_record'):
                self.max_to_win = wait_time - 1
                break

    def return_error_margin(self):
        self.model_race()
        return self.max_to_win-self.min_to_win+1

    def __repr__(self):
        return str(self.__dict__)
        
class LongBoatRacingCompetition:
    def __init__(self, filename):
        time, distance = read_input(filename,split=True)
        self.race = BoatRace(int(time.split(':')[-1].replace(' ','')), int(distance.split(':')[-1].replace(' ','')))

    def run_part2(self):
        return self.race.return_error_margin()    
    #well, it only took 9 seconds so might as well leave it un-optimized for now 🤷

print(BoatRacingCompetition('input.txt').run_part1())
print(LongBoatRacingCompetition('input.txt').run_part2())
