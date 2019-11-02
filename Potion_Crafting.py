'''
Created on Oct 23, 2019
the secret password is: PS
@author: TorchStone
'''

class Component:
    
    def __init__(self,name, location, tier, aspects):
        assert type(name) == str, 'Error: name must be an str'
        assert type(tier) == int, 'Error: tier must be an int'
        assert tier in {1,2,3}, 'Error: tier must be a number 1-3'
        assert type(location) == str, 'Error: location must be a string'
        assert location in ('City','Wilds','Dungeon'), 'Error: {} is not a valid location'.format(location)
        assert type(aspects) == dict,'Error: aspects must be a dictionary'
        self.name = name
        self.location = location
        self.tier = tier-1 #tier is stored 0 based
        self.aspects = aspects
        self.tags = {name.lower(), location.lower(), str(tier)}
        self.tags.update( { k.lower() for k in aspects.keys()} )
    
        
    def __str__(self):
        return '{}\n  found in the {}\n  at tier {}\n  with aspects {}'.format(self.name,self.location,self.tier + 1,self.aspects)
    
    
    def __add__(self,right):
        assert type(right) in (Component, dict), 'Error: cannot add'
        if type(right) != dict:
            add_this = dict(right.aspects)
        else:
            add_this = dict(right)
        for k,v in self.aspects.items():
            if k in add_this.keys():
                add_this[k] += v
            else:
                add_this[k] = v
        return add_this
    
    
    def __radd__(self,left):
        assert type(left) in (Component, dict), 'Error: cannot add'
        if type(left) != dict:
            add_this = dict(left.aspects)
        else:
            add_this = dict(left)
        for k,v in self.aspects.items():
            if k in add_this.keys():
                add_this[k] += v
            else:
                add_this[k] = v
        return add_this
    
    
class Potion:
    def __init__(self, name, keyAspect, recipe, rRecipe):
        assert type(name) == str, 'Error: name must be an str'
        assert type(keyAspect) == str, 'Error: keyAspect must be an str'
        assert type(recipe) == dict, 'Error: recipe must be a dictionary'
        
        assert type(rRecipe) == tuple, 'Error: Recomended Recipe must be an set'
        
        self.name = name
        self.keyAspect = keyAspect
        self.recipe = recipe
        self.rRecipe = rRecipe
        self.tags = {name.lower(), keyAspect.lower()}
        
    def __str__(self):
        return '{}\n  is associated with {}\n  the recipe is {}\n  and can be brewed with {}'.format(self.name,self.keyAspect,self.recipe,self.rRecipe)
    def brew(self, cauldren):
        assert type(cauldren) == dict, 'Error: Input must be a dictionary'
        for a in self.recipe.keys():
            if a not in cauldren.keys():
                return False
        x = [( max(r) >= cauldren[a] and cauldren[a] >= min(r)) for a,r in self.recipe.items() if a in cauldren.keys()]
        if x == []:
            return False
        else:
            return all(x)
    
    
def print_menu(debugToggle):
    if debugToggle: print("DEBUGGING MOD")
    print('Alchemy Prototype Menu\n---------------')
    print('  V ~ View Aspects')
    print('  R ~ Research Components')
    print('  S ~ Study Potions')
    print('  B ~ Brew a Potion')
    if debugToggle: print("  >C ~ View Combination")
    if debugToggle: print("  >P ~ View Possible Recipes")
    print('  Q ~ Quit\n---------------')
    valid = False
    while valid == False:
        opt = input('Choose an option: ')
        if opt in 'vrsbqVRSBQ' or debugToggle or opt == 'PS':
            valid = True
            break
        else:
            print ('Invalid Option')
            
    return opt
    
    
def print_aspects(allAspects):    
    atl = sorted(list(allAspects))
    col = 0
    print('\nALL ASPECTS\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    x = 0
    line = ''
    for n in atl:
        line += '{:15}'.format(n)
        col +=1
        x += 1
        if col >= 4 or x == len(atl):
            print(line)
            line = ''
            col = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    pass


def print_components():
    print('\nALL POTION COMPONENTS\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    names = {c.name for c in allComponents.values()}
    col = 0
    x = 0
    line = ''
    for n in names:
        line += '{:20}'.format(n)
        col +=1
        x += 1
        if col >= 4 or x == len(names):
            print(line)
            line = ''
            col = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    
    
def research(allComponents):
    researching = True
    print_components()
    while researching:
        keyString = input('Search for an aspect by Name, location, Tier, and/or Aspects seperated by commas(,)\n or enter \"M\" to return to the Main Menu: ')
        if keyString == 'm' or keyString == 'M':
            break
        keywords = [x.strip().lower() for x in keyString.split(',')]
        matches = []
        for c in allComponents.values():
            if all((w in c.tags) for w in keywords):
                matches.append(c)
        
        if matches == []:
            print('----------')
            print('No Matches')
            print('----------')
        elif len(matches) == 1:
            print('----------')
            print(matches[0])
            print('----------')
        else:
            print('----------')
            print('matching components: ',[c.name for c in matches])
            print('----------')
    pass

    
def study(allPotions):
    studying = True
    print('\nALL POTIONS\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    names = {p.name for p in allPotions.values()}
    col = 0
    x = 0
    line = ''
    for n in names:
        line += '{:25}'.format(n)
        col +=1
        x += 1
        if col >= 4 or x == len(names):
            print(line)
            line = ''
            col = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    while studying:
        keyString = input('Search for an potion by Name, or Key Aspect seperated by commas(,)\n or enter \"M\" to return to the Main Menu: ')
        if keyString == 'm' or keyString == 'M':
            break
        keywords = [x.strip().lower() for x in keyString.split(',')]
        matches = []
        for p in allPotions.values():
            if all(((w in p.tags) for w in keywords)):
                matches.append(p)
      
        if matches == []:
            print('----------')
            print('No Matches')
            print('----------')
        elif len(matches) == 1:
            print('----------')
            print(matches[0])
            print('----------')
        else:
            print('----------')
            print('matching potions: ',[p.name for p in matches])
            print('----------')
    pass


def print_graph(inputDict):
    height = max(inputDict.values())
    for lvl in range(height+1):
        line = ''
        for k in sorted(list(inputDict.keys())):
            if inputDict[k] > height-lvl:
                line += '{:14}'.format('-----')
            else:
                line += '{:14}'.format('')
        print(line)
    l1 = ''
    l2 = ''
    for k in sorted(list(inputDict.keys())):
        l1 += '______________'
        l2 += '{:14}'.format(k)
    print(l1)
    print(l2)
    pass


def brewPotion(allComponents,allPotions,debugToggle):
    print_components()
    cauldren = {}
    for i in range(3):
        while 1:
            addition = None
            name_adition = input('Add component {}: '.format(i + 1))
            for c in allComponents.values():
                if c.name.lower() == name_adition.lower():
                    addition = c
            if addition == None:
                print('--Invalid component name--')
            else:
                break
        cauldren += addition
        print_graph(cauldren)
    answ = input('Brew this Potion?(Y/N): ')
    for a in cauldren.keys():
        if cauldren[a] == max(cauldren.values()):
            keyAsp = a
            break
    
    if answ in 'Yy':
        found = False
        for p in allPotions.values():
            if keyAsp == p.keyAspect:
                found = True
                if debugToggle:
                    print('Attempting to brew {}...'.format(p.name))
                if p.brew(cauldren):
                    print('You succesfully brewed {}!'.format(p.name))
                    break
                else:
                    print('hmm... that recipe didn\'t work')
                    break
        if not found:
            print('A potion for {} has not yet been implemented'.format(keyAsp))
        opt = input('Try again?(Y/N): ')
        if opt in 'Yy':
            brewPotion(allComponents,allPotions,debugToggle)
        else:
            print('returning to Main Menu...')
            pass
    else:
        print('returning to Main Menu...')
        pass
    pass


def veiw_combo(allComponents):
    veiw_ids(allComponents)
    while 1:
        I = input('Input ID\'s (seperated buy commas) or Q to quit: ')
        if I == 'Q' or I == 'q':
            break
        Ids = [x.strip() for x in I.split(',')]
        for i in Ids:
            if i not in allComponents.keys():print(str(i), 'is not a valid ID')
            continue
        print(allComponents[Ids[0]]+allComponents[Ids[1]]+allComponents[Ids[2]])
    pass


def view_posible(allComponents,allPotions):
    veiw_ids(allPotions)
    mode = 'EXCLUSIVE'
    while 1:
        print('The mode is [{}]:'.format(mode))
        I = input('Input ID, I or E to change mode, or Q to quit: ')
        if I in 'Qq':
            break
        if I in 'Ee':
            mode = 'EXCLUSIVE'
        if I in 'Ii':
            mode = 'INCLUSIVE'
        try:
            potion = allPotions[I]
        except:
            print(str(I), 'is not a valid ID')
            continue
        posComp = set()
        combos = []
        for c in allComponents.values():
            for a in potion.recipe.keys():
                if a in c.aspects.keys(): posComp.add(c)
        for a1 in posComp:
            for a2 in posComp:
                for a3 in posComp:
                    if potion.brew(a1+a2+a3) and (all((a1 != a2, a1 != a3, a2 != a3)) or mode == 'INCLUSIVE'):
                        x = {a1.name,a2.name,a3.name}
                        if x not in combos: combos.append(x)
        print(combos)
        
    pass


def veiw_ids(IdDict):
    for i,v in IdDict.items():
        print('{} - {}'.format(i,v.name))
    pass

if __name__=='__main__':
    allComponents = {}
    
    ##CITY##
    allComponents['000'] = Component('Milk', 'City', 1, {"Terra":2, "Victus": 3})
    allComponents['001'] = Component('Water', 'City', 1, {"Aqua":4})
    allComponents['002'] = Component('Salt', 'City', 1, {"Terra":2, "Vitreus": 3})
    allComponents['010'] = Component('Pitch', 'City', 2, {"Tenebrae":5, "Vinculum": 2, "Instramentum":3})
    allComponents['011'] = Component('Saltpetre', 'City', 2, {"Vitreus":2, "Potentia": 5, "Victus":3})
    allComponents['012'] = Component('Phosphorus', 'City', 2, {"Lux": 7, "Metalum": 3})
    allComponents['020'] = Component('Quicksilver', 'City', 3, {"Metalum":2, "Motus": 8, "Venenum":4})
    allComponents['021'] = Component('Sulfur', 'City', 3, {"Ignis":6, "Potentia": 5, "Telum":4})
    allComponents['022'] = Component('Arsenic', 'City', 3, {"Venenum":7, "Mortus": 3, "Telum":5})
    
    ##WILDS##
    allComponents['100'] = Component('lavander', 'Wilds', 1, {"Herba":2, "Victus": 3})
    allComponents['101'] = Component('Peppermint', 'Wilds', 1, {"Herba":2, "Gelum": 3})
    allComponents['102'] = Component('Honey', 'Wilds', 1, {"Vinculum":1, "Fames": 2, "Aer": 2})
    allComponents['110'] = Component('Galena', 'Wilds', 2, {"Metalum":3, "Praecantatio": 5, "Venenum":2})
    allComponents['111'] = Component('Magnetite', 'Wilds', 2, {"Metalum":5, "Instramentum": 5})
    allComponents['112'] = Component('Cinnabar', 'Wilds', 2, {"Tutamen":5, "Metalum": 2, "Aer":3})
    allComponents['120'] = Component('Griffon Talon', 'Wilds', 3, {"Telum":6, "voltus": 6, "Aer":3})
    allComponents['121'] = Component('Owlbear Further', 'Wilds', 3, {"Bestia":6, "Tutamen": 3, "Aer":6})
    allComponents['122'] = Component('Treant Bark', 'Wilds', 3, {"Arbor": 7, "Praecantatio": 4, "Victus":4})
    
    ##Dungeon##
    allComponents['200'] = Component('Bone', 'Dungeon', 1, {"Mortus":4, "Examinus": 1})
    allComponents['201'] = Component('Caustic Ooze', 'Dungeon', 1, {"Limus":4, "Mortus": 1})
    allComponents['202'] = Component('Goblin Blood', 'Dungeon', 1, {"Lucrum":2, "Telum": 3})
    allComponents['210'] = Component('Spider Silk', 'Dungeon', 2, {"Vinculum":4, "Venenum": 2, "Aer":4})
    allComponents['211'] = Component('Ectoplasum', 'Dungeon', 2, {"Praecantatio":3, "Mortus":1 , "Examinus": 6})
    allComponents['212'] = Component('Mimic Tooth', 'Dungeon', 2, {"Fames":7, "Praecantatio": 3})
    allComponents['220'] = Component('Primordial Fire', 'Dungeon', 3, {"Ignes":7, "Praecantatio": 6, "Lux":2})
    allComponents['221'] = Component('Yeti Fur', 'Dungeon', 3, {"Bestia":5, "Gelum": 8, "Aqua": 2})
    allComponents['222'] = Component('Dragon Scale', 'Dungeon', 3, {"Lucrum":10, "Ignis": 3, "Tutamen":2})
    
    allPotions = {}
    allPotions['0'] = Potion('Deathward Potion', 'Mortus', {'Mortus':(4,8), 'Examinus':(1,5), 'Victus':(1,5)}, ('Bone','Caustic Ooze','Milk'))
    allPotions['1'] = Potion('Necromancer\'s Poison', 'Examinus', {'Examinus':(5,9), 'Mortus':(3,7), 'Praecantatio':(1,10)}, ('Ectoplasum','Bone','water'))
    allPotions['2'] = Potion('Slippery Potion', 'Limus', {'Limus':(2,6), 'Aqua':(2,5), 'Gelum':(1,3)}, ('Caustic Ooze','Peppermint','water'))
    allPotions['3'] = Potion('The Philosopher\'s Stone', 'Lucrum', {'Lucrum':(10,15), 'Motus':(4,10), 'Praecantatio':(2,10)}, ('%$#$%!##@$$','@#%$#%$','@#%@##@%@@#'))
    allPotions['4'] = Potion('Strength Potion', 'Telum', {'Telum':(3,10), 'Victus':(2,6), 'Lucrum':(1,4)}, ('Goblin Blood','Griffin Talon','Lavender'))
    allPotions['5'] = Potion('Paralisis Poison', 'Vinculum', {'Vinculum':(4,9), 'Fames':(1,3),'Venenum':(1,4)}, ('Spider Silk','Pitch','honey'))
    allPotions['6'] = Potion('Assasin\'s Poison', 'Venenum', {'Venenum':(6,12), 'Aqua':(2,6), 'Mortus':(2,6)}, ('Arsenic','Galena','Water'))
    allPotions['7'] = Potion('Wisdom Potion', 'Praecantatio', {'Praecantatio':(6,10), 'Victus':(3,7), 'Vitreus':(1,5)}, ('Primordial Fire','Treant Bark','Salt'))
    allPotions['8'] = Potion('Saitey Potion', 'Fames', {'Fames':(5,11), 'Victus':(1,5), 'Praecantatio':(1,5)}, ('Mimic tooth','Honey','Milk'))
    allPotions['9'] = Potion('Cold Resistance Potion', 'Ignis', {'Ignis':(5,11), 'Victus':(1,5), 'Praecantatio':(1,5)}, ('Sulfur','Lavander','Peppermint'))
    componentAspects = set()
    for c in allComponents.values():
        componentAspects.update(set(c.aspects.keys()))

    potionAspects = set()
    for p in allPotions.values():
        potionAspects.add(p.keyAspect)
    
    if potionAspects != componentAspects:
        print( "Error P and C aspects don't agree\n   Missing potions for:\n   {}\n   Missing Components which include:\n   {}".format((componentAspects-potionAspects),(potionAspects-componentAspects)))
    debugToggle = False
    menu = True
    while menu:
        opt = print_menu(debugToggle)
        
        if opt in 'vV':
            print_aspects(componentAspects)
            continue
        elif opt in 'rR':
            research(allComponents)
            continue
        elif opt in 'sS':
            study(allPotions)
            continue
        elif opt in 'bB':
            brewPotion(allComponents,allPotions,debugToggle)
        elif opt in 'qQ':
            menu = False
            break
        elif opt == 'PS':
            debugToggle = not debugToggle
            continue
        elif opt in 'cC':
            veiw_combo(allComponents)
            continue
        elif opt in 'pP':
            view_posible(allComponents,allPotions)
            continue
        else:
            raise ValueError
        
