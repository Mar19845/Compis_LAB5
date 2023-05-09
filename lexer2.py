from constants import *

class Parser:
    def __init__(self, file):
        self.file = file
        self.slr_rules = {}
        self.first_pos = {}
        #self.tokens = {}
        self.tokens = []
        #self.ignore_tokens = {}
        self.ignore_tokens = []
        self.read()
        self.get_first_positions()
        
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
                        break
                elif line.startswith(';'):
                    production = not production
                else:
                    if len(line) > 0:
                        line = line.replace('|', '',1).lstrip().rstrip()
                        line = line.split()
                        self.slr_rules[production_name].append(line)
                        #print(repr(line),production_name)

    def get_first_positions(self):
        for key in self.slr_rules:
            first_pos,first_pos1 = self.calculate_first_position(self.slr_rules[key][0])
            #for term in self.slr_rules[key]:
                #first_pos,first_pos1 = self.calculate_first_position(term)
            first_pos1 = list(dict.fromkeys(first_pos1))
            list_of_productions = list(self.slr_rules.keys())
                    
            #test = [val val not in list_of_productions for val in first_pos1]
            first_pos = [val for val in first_pos1 if val not in list_of_productions]
            #print(first_pos)
            self.first_pos[key] = first_pos
    
    def calculate_first_position(self,production_list):
        #
        first_pos = production_list #
        first_pos_1 = [] #
        first_pos_2 = [] #
        for production in production_list:
            if production in self.slr_rules:
                first_pos_1.append(production)
                for production_rules in self.slr_rules[production]:
                    
                    if production_rules[0] not in first_pos_1 : #and production_rules[0] not in self.slr_rules:
                        first_pos.append(production_rules[0])
                        first_pos_2.append(production_rules[0])
                        
        if sorted(first_pos) == sorted(production_list):
            return first_pos,first_pos_2
        else:
            return self.calculate_first_position(first_pos)
            
                
            
            
        
                        
                    
                    
yalexFile = "slr-2.yalp"
a = Parser(yalexFile)
#print(a.tokens)
#a.get_first_positions()
for k in a.first_pos:
    print(k,a.first_pos[k])
#for k in a.slr_rules.keys():print(k,a.slr_rules[k])
#print(a.slr_rules)

