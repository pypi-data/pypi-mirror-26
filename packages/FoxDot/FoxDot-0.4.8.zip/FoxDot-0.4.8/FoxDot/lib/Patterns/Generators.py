from __future__ import absolute_import, division, print_function

from .Main  import GeneratorPattern, Pattern, asStream

class PRand(GeneratorPattern):
    ''' Returns a random integer between start and stop. If start is a container-type it returns
        a random item for that container. '''
    def __init__(self, start, stop=None, **kwargs):
        GeneratorPattern.__init__(self, **kwargs)
        # If we're given a list, choose from that list
        if hasattr(start, "__iter__"):
            self.data = Pattern(start)
            try:
                assert(len(self.data)>0)
            except AssertionError:
                raise AssertionError("{}: Argument size must be greater than 0".format(self.name))
            self.choosing = True
            self.low = self.high = None
        else:
            self.choosing = False
            self.low  = start if stop is not None else 0
            self.high = stop  if stop is not None else start
            try:
                assert((self.high - self.low)>=1)
            except AssertionError:
                raise AssertionError("{}: Range size must be greater than 1".format(self.name))
            self.data = "{}, {}".format(self.low, self.high)
            
    def func(self, index):
        if self.choosing:
            value = self.choice(self.data)
        else:
            value = self.randint(self.low, self.high)
        return value

    def string(self):
        """ Used in PlayString to show a PRand in curly braces """
        return "{" + self.data.string() + "}"

class PxRand(PRand):
    def func(self, index):
        value = PRand.func(self, index)
        while value == self.last_value:
            value = PRand.func(self, index)
        self.last_value = value                
        return self.last_value

class PwRand(GeneratorPattern):
    def __init__(self, values, weights, **kwargs):
        GeneratorPattern.__init__(self, **kwargs)
        try:
            assert(all(type(x) == int for x in weights))
        except AssertionError:
            e = "{}: Weights must be integers".format(self.name)
            raise AssertionError(e)
        self.data    = Pattern(values)
        self.weights = Pattern(weights).stretch(len(self.data))
        self.items   = self.data.stutter(self.weights)

    def func(self, index):
        return self.choice(self.items)     

class PChain(GeneratorPattern):
    def __init__(self, mapping, **kwargs):
        GeneratorPattern.__init__(self, **kwargs)
        self.last_value = 0
        self.mapping = {}
        i = 0
        for key, value in mapping.items():
            self.mapping[key] = asStream(value)
            # Use the first key to start with
            if i == 0:
                self.last_value = key
                i += 1
                
    def func(self, index):
        self.last_value = self.choice(self.mapping[self.last_value])
        return self.last_value

class PTree(GeneratorPattern):
    """ Takes a starting value and two functions as arguments. The first function, f, must
        take one value and return a container-type of values and the second function, choose,
        must take a container-type and return a single value. In essence you are creating a
        tree based on the f(n) where n is the last value chosen by choose.
    """
    def __init__(self, n=0, f=lambda x: (x + 1, x - 1), choose=lambda x: random.choice(x), **kwargs):
        GeneratorPattern.__init__(self, **kwargs)
        self.f  = f
        self.choose = choose
        self.values = [n]

    def func(self, index):
        self.values.append( self.choose(self.f( self.values[-1] )) )
        return self.values[-1]

class PWalk(GeneratorPattern):
    def __init__(self, max=7, step=1, start=0, **kwargs):

        GeneratorPattern.__init__(self, **kwargs)
        
        self.max   = abs(max)
        self.min   = self.max * -1
        
        self.step  = asStream(step).abs()
        self.start = start

        self.data = [self.start, self.step, self.max]

        self.directions = [lambda x, y: x + y, lambda x, y: x - y]

        self.last_value = None

    def func(self, index):
        if self.last_value is None:
            self.last_value = 0
        else:
            if self.last_value >= self.max: # force subtraction
                f = self.directions[1]
            elif self.last_value <= self.min: # force addition
                f = self.directions[0]
            else:
                f = self.choice(self.directions)
            self.last_value = f(self.last_value, self.step.choose())
        return self.last_value   

class PWhite(GeneratorPattern):
    ''' Returns random floating point values between 'lo' and 'hi' '''
    def __init__(self, lo=0, hi=1, **kwargs):
        GeneratorPattern.__init__(self, **kwargs)
        self.low = float(lo)
        self.high = float(hi)
        self.mid = (lo + hi) / 2.0
        self.data = "{}, {}".format(self.low, self.high)
    def func(self, index):
        return self.triangular(self.low, self.high, self.mid)

class PSquare(GeneratorPattern):
    ''' Returns the square of the index being accessed '''
    def func(self, index):
        return index * index

