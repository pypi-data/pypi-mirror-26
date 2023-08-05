"""

optionloop.py

Provides implementation of a simple iteratable dictionary structure
that can be used to iterate over options in a single for-loop.

No longer will you need a million nested for-loops...

The OptionLoop works as follows:

First, initialize a dictionary with various keys and values, e.g.:

d = {'doThingX' : [True, False], 'doThingY' : False,
        'thingZValue' : ['a', 'b', 1]}

Next create the option loop:

oploop = OptionLoop(d)

Finally iterate and get your values:

for state in oploop:
    doX = state['doThingX']
    doY = state['doThingY']
    zVal = state['thingZValue']

    f(doX, doY, zVal)

This is intended to replace an equivalent looping structure of:

for doX in doThingX:
    for doY in doThingY:
        for zVal in thingZValue:
            f(doX, doY, zVal)

which quickly becomes cumbersome.

Also, option loops can be added to create even more complex looping structures, e.g.:

d1 = {'lang' : ['c'], 'doThingX' : [True, False]}
d2 = {'lang' : ['fortran'], 'doThingX' : [True, False], 'doThingY' : [True, False]}

oploop1 = OptionLoop(d1)
oploop2 = OptionLoop(d2)
oploop = oploop1 + oploop2

for state in oploop:
    ...

is equivalent to:

langs = ['c', 'fortran']
doThingX = [True, False]
doThingY = [True, False]

for lang in langs:
    if lang == 'c':
        for doX in doThingX:
            f(lang, doX)
    elif lang == 'fortran':
        for doX in doThingX:
            for doY in doThingY:
                f(lang, doX, doY)

d = OrderedDict()
d['a'] = [False, True]
d['b'] = [False]
d['c'] = [1, 2, 3]
oploop = OptionLoop(d)
for state in oploop:
    ...

is equivalent to:

for a in [False, True]:
    for b in [False]:
        for c in [1, 2, 3]:
            ....

"""

from collections import defaultdict
import six


class OptionLoop(object):
    class optionloopconcat(object):

        def __init__(self, oploop_list):
            self.oplooplist = oploop_list
            self.master_index = 0

        def check_all(self):
            """
            Checks to see that all option loops are unstarted
            """
            return all(oploop.index == 0 for oploop in self.oplooplist) \
                and self.master_index == 0

        def __next__(self):
            if self.master_index < len(self.oplooplist):
                try:
                    return self.oplooplist[self.master_index].__next__()
                except StopIteration:
                    self.master_index += 1
                    return self.__next__()
            else:
                raise StopIteration()

        def copy(self):
            newlist = []
            for oploop in self.oplooplist:
                newlist.append(oploop.copy())
            return OptionLoop.optionloopconcat(newlist)

        def __iter__(self):
            return self

        def __add__(self, other):
            if not self.check_all():
                raise Exception('Cannot add to already started option loop!')
            if isinstance(other, OptionLoop.optionloopconcat):
                if not other.check_all():
                    raise Exception('Cannot add already started option loop!')

                thelist = self.oplooplist[:]
                thelist.extend(other.oplooplist)
                return OptionLoop.optionloopconcat(thelist)
            elif isinstance(other, OptionLoop):
                return OptionLoop.optionloopconcat(self.oplooplist[:] + [other])

        next = __next__  # python 2 compatiblity

    def __init__(self, initializing_dictionary, default_dict_factory=None):
        """
        Initializes the OptionLoop.

        @param initializing_dictionary :
        The basis of the option loop.
        The various options to iterate are the keys of the dictionary,
        while the value(s) associated with the key are iterated over

        @param default_dict_factory :
        if not None, default dicts will be returned using this factory
        """

        assert isinstance(initializing_dictionary, dict)

        self.mydict = initializing_dictionary.copy()
        self.index = 0
        self.end_index = None
        for key, value in six.iteritems(self.mydict):
            if isinstance(value, (str, bytes)):
                self.mydict[key] = [value]
                size = 1
            else:
                try:
                    size = len(value)
                except TypeError:
                    self.mydict[key] = [value]
                    size = len([value])

            if self.end_index is None:
                self.end_index = 1
            # the maximum index is the multiplicative sum
            # of the length of all interior arrays
            self.end_index *= size
        self.default_dict_factory = default_dict_factory
        self.use_dd = default_dict_factory is not None

    def copy(self):
        return OptionLoop(self.mydict,
                          self.default_dict_factory)

    def __next__(self):
        if self.use_dd:
            value_list = defaultdict(self.default_dict_factory)
        else:
            value_list = {}
        startlen = 1
        if self.end_index is not None and self.index < self.end_index:
            for key, value in six.iteritems(self.mydict):
                value_list[key] = value[int(self.index / startlen) % len(value)]
                startlen *= len(value)

            self.index += 1
        else:
            raise StopIteration()

        return value_list

    def __add__(self, other):
        assert isinstance(other, OptionLoop) or isinstance(other, self.optionloopconcat), \
            "Adding object of type {} to option loop undefined".format(
                type(other))

        if isinstance(other, self.optionloopconcat):
            if self.index > 0 or not other.check_all():
                raise Exception(
                    'Cannot add option loops once iteration has begun...')
            return self.optionloopconcat([self] + other.oplooplist)

        if self.index > 0 or other.index > 0:
            raise Exception(
                'Cannot add option loops once iteration has begun...')

        return self.optionloopconcat([self, other])

    def __iter__(self):
        return self

    next = __next__  # python 2 compatiblity
