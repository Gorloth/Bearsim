class Bear:
    def __init__(self):
        self.reset()
        self.places = [ 0 for _ in range(racers) ]
        
    def reset( self ):
        self.square = 0
        self.rank = 1
        self.finished = False

class Black(Bear):
    name = 'Black'
    def move( self, roll ):
        if roll in ( 1, 2, 3 ):
            self.square += roll
        return self.square
        
class Sloth(Bear):
    name = 'Sloth'
    def move( self, roll ):
        self.square += 1
        return self.square

class Grizzly(Bear):
    name = 'Grizzly'
    def move( self, roll ):
        if roll in ( 5, 6 ):
            self.square += 3
        return self.square
        
class Mother(Bear):
    name = 'Mother'
    def move( self, roll ):
        if roll in ( 1, 2, 5, 6 ):
            if self.has_cub:
                self.square += 1
            else:    
                self.square += 2
                if self.square >= self.cub_square and self.has_cub is False:
                    self.square = self.cub_square
                    self.has_cub = True
        elif self.has_cub is False:
            self.cub_square += 1
        return self.square
        
    def reset( self ):
        Bear.reset(self)
        self.cub_square = 7
        self.has_cub = False

class Kodiak(Bear):
    name = 'Kodiak'
    def move( self, roll ):
        if roll <= self.rank:
            self.square += 2
        return self.square
        
class Teddy(Bear):
    name = 'Teddy'
    def move( self, roll ):
        if roll <= 3:
            self.square += ( ( self.rank ) / 2 ) + 1
        return self.square
        
class Panda(Bear):
    name = 'Panda'
    def move( self, roll ):
        if self.stopped:
            self.stopped = False
        elif roll in ( 2, 3, 4, 5 ):
            if self.square in (4, 9):
                self.square += 1
                self.stopped = True
            else:    
                self.square += 2
        return self.square
        
    def reset( self ):
        Bear.reset(self)
        self.stopped = False

class Polar(Bear):
    name = 'Polar'
    def move( self, roll ):
        self.tokens += 1
        if roll <= self.tokens:
            self.square += self.tokens
            self.tokens = 0
        return self.square
        
    def reset( self ):
        Bear.reset(self)
        self.tokens = 1
        
class Sun(Bear):
    name = 'Sun'
    def move( self, roll ):
        if roll >3:
            self.square += self.tokens
            self.tokens = 1
        else:
            self.tokens += 1
        return self.square
        
    def reset( self ):
        Bear.reset(self)
        self.tokens = 2

class Spectacled(Bear):
    name = 'Spectacled'
    def move( self, roll ):
        if roll in ( 3, 4 ):
            self.square += 1
        elif roll in ( 5, 6 ):
            self.square += 2
        return self.square       

import random
import numpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--attempts', default=10000, type=int, help='Number of simulated rounds to run')
parser.add_argument('-l', '--length', default=15, type=int, help='lenght of the board')
parser.add_argument('-r', '--racers', default=5, type=int, help='number of racers')
parser.add_argument('-s', '--standalone', action='store_true', help='flag to do a standalone simulation (runs individual racers and gives stats)')
parser.add_argument('-d', '--seed', default=0, type=int, help='number of racers')
args = parser.parse_args()

attempts = args.attempts
finish = args.length
racers = args.racers
if args.seed is not 0:
    random.seed( args.seed )
print args

bears = random.sample([ Black(), Sloth(), Grizzly(), Mother(), Panda(), Polar(), Kodiak(), Sun(), Spectacled(), Teddy()  ], racers )

random.shuffle(bears)

if args.standalone:
    for bear in bears:
        with open( '{0}.csv'.format(bear.name), 'w' ) as f:
            total_rounds = 0
            all = []
            for i in range( attempts ):
                rounds = 0
                bear.reset()
                while bear.square < finish:
                    bear.move(random.randint(1,6))
                    rounds += 1
                total_rounds += rounds
                all.append(rounds)
                f.write( '{},\n'.format(rounds) )
            print 'Took {0: <7} average of {1:0<6} tries to win, var of {2:0<6}, std of {3:0<6}'.format( bear.name, 1.0*total_rounds/attempts, numpy.var(all), numpy.std(all))
else:
    results = {}
    for bear in bears:
        results[bear.name] = 0
    for j in range( attempts ):
        place = 0
        for bear in bears:
            bear.reset()
        while place < racers:
            roll = random.randint(1, 6)
            for bear in bears:
                bear.move(roll)
            rank = sorted(bears, key=lambda x: x.square, reverse=True)
            current_place = 1
            previous = rank[0].square
            for bear in rank:
                if bear.square != previous:
                    current_place = rank.index(bear) + 1
                if bear.square >= finish and not bear.finished:
                    bear.places[place] += 1
                    place += 1
                    bear.finished = True
                bear.rank = current_place
                previous = bear.square
    for bear in bears:
        print bear.name
        print bear.places, bear.places[0]*4+bear.places[1]*3+bear.places[2]*2+bear.places[3]
            