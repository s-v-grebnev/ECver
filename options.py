import os

class Options(object):
    opts = {}
    def __init__(self):
        self.opts = {'UseAtkin':False, 'AtkinPath':'./atkin64',
                     'OutputBase':16, 'MRIterations':128}

    def SetOption(self, key, value):
        self.opts[key] = value

    def GetOption(self, key):
        return self.opts.get(key, None)

    def SaveOptions(self, filename):
        with open(filename, 'w') as fh:
            for i in self.opts.keys():
                fh.write(i + '=' + str(self.opts[i]).rstrip('\n') + '\n')

        print('Saved options')

    def LoadOptions(self, filename):
        with open(filename, 'r') as fh:
            lines = fh.readlines()
            for line in lines:
                sline = line.split('=')
                self.SetOption(sline[0], sline[1].rstrip('\n'))
        print('Loaded options')

