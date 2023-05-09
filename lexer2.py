from constants import *

class Parser:
    def __init__(self, file):
        self.file = file
        self.slr_rules = {}
        #self.tokens = {}
        self.tokens = []
        #self.ignore_tokens = {}
        self.ignore_tokens = []
        self.FIRST = {}
        self.FOLLOW = {}
        self.ERROR = False
        self.read()
        self.get_first_and_follow()
        
    def read(self):   
        with open(YALEX_DIRECTORY + self.file, "r") as file:
            lines = file.readlines()
            production = False
            production_name = ''
            for line in lines:
                line = line.rstrip().lstrip().replace("\n",'')
                #print(repr(line),production)
                # comment lines
                if line.startswith('/*') and line.endswith('*/'):
                    if '->' in line:
                        pass
                        #print(repr(line))
                elif line.startswith('%token'):
                    line = line.replace('%token','',1).lstrip().rstrip()
                    line = line.split()
                    self.tokens.extend(line)
                    
                elif line.startswith('IGNORE'):
                    line = line.replace('IGNORE','',1).lstrip().rstrip()
                    line = line.split()
                    self.ignore_tokens.extend(line)
                elif line.endswith(':'):
                    production = not production
                    production_name = line.split(':')[0]
                    if production:
                        self.slr_rules[production_name] = []
                        #print(repr(production_name),production)
                    else:
                        print('Revisar el archivo .yalp')
                        self.ERROR = not self.ERROR
                        break
                elif line.startswith(';'):
                    production = not production
                else:
                    if len(line) > 0:
                        line = line.replace('|', '',1).lstrip().rstrip()
                        line = line.split()
                        self.slr_rules[production_name].append(line)
                        #print(repr(line),production_name)

    def get_first_and_follow(self):
        for symbol in self.slr_rules:
            first = list(self.calculate_first(symbol))
            follow = list(self.calculate_follow(symbol))
            self.FIRST[symbol] = first
            self.FOLLOW[symbol] = follow
            
    # Calculate FIRST sets for all non-terminal symbols
    def calculate_first(self,symbol):
        if symbol in self.FIRST:
            return self.FIRST[symbol]

        self.FIRST[symbol] = set()

        for production in self.slr_rules[symbol]:
            if production[0] not in self.slr_rules:
                self.FIRST[symbol].add(production[0])

            elif production[0] == symbol:
                continue

            else:
                first_of_production = self.calculate_first(production[0])
                self.FIRST[symbol].update(first_of_production)

                i = 1
                while 'epsilon' in first_of_production and i < len(production):
                    first_of_production = self.calculate_first(production[i])
                    self.FIRST[symbol].update(first_of_production - set(['epsilon']))
                    i += 1

                if 'epsilon' in first_of_production and i == len(production):
                    self.FIRST[symbol].add('epsilon')

        return self.FIRST[symbol]
    
    # Calculate FOLLOW sets for all non-terminal symbols
    def calculate_follow(self,symbol):
        if symbol in self.FOLLOW:
            return self.FOLLOW[symbol]

        self.FOLLOW[symbol] = set()

        if symbol == 'E':
            self.FOLLOW[symbol].add('$')

        for non_terminal in self.slr_rules:
            for production in self.slr_rules[non_terminal]:
                if symbol in production:
                    symbol_index = production.index(symbol)
                    if symbol_index == len(production) - 1:
                        self.FOLLOW[symbol].update(self.calculate_follow(non_terminal))
                    else:
                        next_symbol = production[symbol_index + 1]
                        if next_symbol not in self.slr_rules:
                            self.FOLLOW[symbol].add(next_symbol)
                        else:
                            first_of_next_symbol = self.calculate_first(next_symbol)
                            self.FOLLOW[symbol].update(first_of_next_symbol - set(['epsilon']))
                            if 'epsilon' in first_of_next_symbol:
                                self.FOLLOW[symbol].update(self.calculate_follow(non_terminal))

        return self.FOLLOW[symbol]
                
            
            
        
                        
                    
                    
#yalexFile = "slr-2.yalp"
#a = Parser(yalexFile)  
#print(a.FOLLOW)
#print(a.FIRST)
#for k in a.slr_rules.keys():print(k,a.slr_rules[k])
#print(a.slr_rules)