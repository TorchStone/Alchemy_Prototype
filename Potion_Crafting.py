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
    
    def s_print(self):
        return '{} - {}, {} - {}'.format(self.name, self.location, str(self.tier + 1), self.aspects)
    
    
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
        self.discovered = False
        
    def __str__(self):
        if self.discovered:
            return '{}\n  is associated with {}\n  and can be brewed with {},{}, and {}'.format(self.name,self.keyAspect,self.rRecipe[0],self.rRecipe[1],self.rRecipe[2])
        else:
            return '~ Undiscovered Potion ~'
            
    
    def brew(self, cauldren):
        assert type(cauldren) == dict, 'Error: Input must be a dictionary'
        for a in self.recipe.keys():
            if a not in cauldren.keys():
                return False
        x = [( max(r) >= cauldren[a] and cauldren[a] >= min(r)) for a,r in self.recipe.items() if a in cauldren.keys()]
        if x == []:
            return False
        else:
            if all(x): self.discovered = True
            return all(x)
    
    def s_print(self):
        return '{}, {} - {}'.format(self.name, self.keyAspect, self.recipe)
    
    
def print_menu(debugToggle):
    if debugToggle: print("DEBUGGING MODE")
    print('Alchemy Prototype Menu\n---------------')
    print('  V ~ View Aspects')
    print('  R ~ Research Components')
    print('  S ~ Study Potions')
    print('  B ~ Brew a Potion')
    if debugToggle: print("  >C ~ View Combination")
    if debugToggle: print("  >P ~ View Possible Recipes")
    if debugToggle: print("  >L ~ List all Potions and Components")
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
    maxAspect = []
    for a,v in cauldren.items():
        if v == max(cauldren.values()):
            maxAspect.append(a)
    if len(maxAspect) == 1:
        keyAsp = maxAspect[0]
    else:
        print('Error potion must have 1 key aspect, Canceling Brewing...')
        answ = 'N'
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
                    cauldren = a1+a2+a3
                    if potion.brew(cauldren) and (all((a1 != a2, a1 != a3, a2 != a3)) or mode == 'INCLUSIVE'):
                        maxAspect = []
                        for a,v in cauldren.items():
                            if v == max(cauldren.values()):
                                maxAspect.append(a)
                        x = {a1.name,a2.name,a3.name}
                        if x not in combos and len(maxAspect) == 1:
                            combos.append(x)
        print(combos)
        
    pass


def veiw_ids(IdDict):
    for i,v in IdDict.items():
        print('{} - {}'.format(i,v.name))
    pass


def simplePrint(allComponents,allPotions):
    for c in allComponents.values():
        print(c.s_print())
    print('\n---\n')
    for p in allPotions.values():
        print(p.s_print())
    pass


if __name__=='__main__':
    allComponents = {}
    
    ##CITY##
    allComponents['000'] = Component('Milk', 'City', 1, {"Terra":2, "Victus": 3, "Aqua":2})
    allComponents['001'] = Component('Water', 'City', 1, {"Aqua":5, "Instramentum": 2})
    allComponents['002'] = Component('Salt', 'City', 1, {"Terra":2, "Vitreus": 3, "Fames":2})
    allComponents['003'] = Component('Pitch', 'City', 1, {"Tenebrae":3, "Vinculum": 2, "Instramentum":2})
    allComponents['011'] = Component('Saltpetre', 'City', 2, {"Vitreus":1, "Potentia": 4, "Victus":2})
    allComponents['012'] = Component('Phosphorus', 'City', 2, {"Lux": 4, "Vitreus": 3})
    allComponents['020'] = Component('Quicksilver', 'City', 3, {"Lucrum":2, "Voltus":2, "Venenum":2})
    allComponents['010'] = Component('Sulfur', 'City', 2, {"Ignis":2, "Potentia": 3, "Telum":2})
    allComponents['022'] = Component('Hemlock Extract', 'City', 3, {"Venenum":4, "Telum":2, "Herba":2})
    
    ##WILDS##
    allComponents['100'] = Component('Lavander', 'Wilds', 1, {"Herba":3, "Victus": 4})
    allComponents['101'] = Component('Peppermint', 'Wilds', 1, {"Herba":3, "Gelum": 4})
    allComponents['102'] = Component('Honey', 'Wilds', 1, {"Vinculum":3, "Fames": 4})
    allComponents['103'] = Component('Mana Bean', 'Wilds', 1, {"Arbor":3, "Praecantatio": 4})
    allComponents['111'] = Component('Magnetite', 'Wilds', 2, {"Terra":3, "Instramentum": 4})
    allComponents['112'] = Component('Rime Wood', 'Wilds', 2, {"Tutamen":3, "Gelum": 2, "Arbor":2})
    allComponents['120'] = Component('Griffon Talon', 'Wilds', 3, {"Telum":3, "Voltus": 3, "Lucrum":3})
    allComponents['110'] = Component('Owlbear Further', 'Wilds', 2, {"Bestia":3, "Tutamen": 2, "Voltus":2})
    allComponents['121'] = Component('Will-o\'-Wisp Essence', 'Wilds', 3, {"Lux": 4, "Mortus":2, "Examinus": 3})
    
    ##Dungeon##
    allComponents['200'] = Component('Bone', 'Dungeon', 1, {"Mortus":4, "Examinus": 3})
    allComponents['201'] = Component('Caustic Ooze', 'Dungeon', 1, {"Aqua":4, "Mortus": 3})
    allComponents['202'] = Component('Rat Tail', 'Dungeon', 1, {"Bestia":4, "Tenebrae": 3, })
    allComponents['203'] = Component('Spider Silk', 'Dungeon', 1, {"Vinculum":3, "Venenum": 3})
    allComponents['211'] = Component('Phantom Ectoplasm', 'Dungeon', 2, {"Praecantatio":2, "Examinus": 3, "Gelum":2})
    allComponents['212'] = Component('Mimic Splinter', 'Dungeon', 2, {"Fames":3, "Praecantatio": 2, "Arbor":2})
    allComponents['220'] = Component('Primordial Fire', 'Dungeon', 3, {"Ignis":4, "Potentia": 2, "Lux":3})
    allComponents['210'] = Component('Bailisk Blood', 'Dungeon', 2, {"Tenebrae":3, "Bestia": 2, "Venenum":2})
    allComponents['222'] = Component('Dragon Scale', 'Dungeon', 3, {"Lucrum": 5, "Ignis": 2, "Tutamen":2})
    
    allPotions = {}
    allPotions['0'] = Potion('Deathward Potion', 'Mortus', {'Mortus':(5,8), 'Examinus':(2,4), 'Victus':(2,4)}, ('Bone','Caustic Ooze','Lavander'))
    allPotions['1'] = Potion('Necromancer\'s Poison', 'Examinus', {'Examinus':(5,7), 'Mortus':(3,5), 'Aqua':(3,5)}, ('Phantom Ectoplasm','Bone','Water'))
    allPotions['2'] = Potion('Animal Friendship Potion', 'Bestia', {'Bestia':(4,8), 'Victus':(2,4), 'Terra':(1,3)}, ('Rat Tail','Owlbear Further','Milk'))
    allPotions['3'] = Potion('The Philosopher\'s Stone', 'Lucrum', {'Lucrum':(9,10), 'Voltus':(3,6), 'Ignis':(1,3)}, ('Quicksilver','Griffon Talon','Dragon Scale'))
    allPotions['4'] = Potion('Strength Potion', 'Telum', {'Telum':(3,5), 'Victus':(2,4), 'Potentia':(1,4)}, ('Sulfur','Griffin Talon','Milk'))
    allPotions['5'] = Potion('Paralisis Poison', 'Vinculum', {'Vinculum':(5,9), 'Fames':(2,4),'Venenum':(1,4)}, ('Spider Silk','Pitch','Honey'))
    allPotions['6'] = Potion('Assasin\'s Poison', 'Venenum', {'Venenum':(6,9), 'Tenebrae':(2,4), 'Vinculum':(2,5)}, ('Hemlock Extract','Bailisk Blood','Spider Silk'))
    allPotions['7'] = Potion('Wisdom Potion', 'Praecantatio', {'Praecantatio':(4,6), 'Fames':(2,5), 'Vitreus':(1,5)}, ('Mimic Splinter','Mana Bean','Salt'))
    allPotions['8'] = Potion('Saitey Potion', 'Fames', {'Fames':(5,8), 'Aqua':(3,5), 'Praecantatio':(1,4)}, ('Mimic Splinter','Honey','Water'))
    allPotions['9'] = Potion('Cold Resistance Potion', 'Ignis', {'Ignis':(4,7), 'Potentia':(2,6), 'Tutamen':(1,4)}, ('Sulfur','Rime Wood','Primordial Fire'))
    allPotions['10'] = Potion('Defense Potion', 'Tutamen', {'Tutamen':(4,7), 'Instramentum':(2,5), 'Terra':(2,5)}, ('Magnetite','Rime Wood','Owlbear Further'))
    allPotions['11'] = Potion('Flying Potion', 'Voltus', {'Voltus':(3,6), 'Praecantatio':(2,4), 'Bestia':(2,5)}, ('Owlbear Further','Griffon Talon','Mana Bean'))
    allPotions['12'] = Potion('Dexterity Potion', 'Instramentum', {'Instramentum':(5,9), 'Terra':(2,4), 'Aqua':(2,5)}, ('Water','Pitch','Magnetite'))
    allPotions['13'] = Potion('Flame Resistance Potion', 'Gelum', {'Gelum':(5,7), 'Herba':(2,4), 'Aqua':(3,5)}, ('Peppermin','Water','Rime Wood'))
    allPotions['14'] = Potion('Health Potion', 'Victus', {'Victus':(6,8), 'Fames':(2,4), 'Terra':(1,4)}, ('Peppermin','Water','Rime Wood'))
    allPotions['15'] = Potion('Mana Potion', 'Potentia', {'Potentia':(5,8), 'Praecantatio':(3,6), 'Ignis':(1,3)}, ('Mana Bean','Sulfur','Saltpetre'))  #Only 1 Possible Combo
    allPotions['16'] = Potion('Darkvision Potion', 'Lux', {'Lux':(5,8), 'Tenebrae':(2,4), 'Vitreus':(1,4)}, ('Phosphorus','Will-o\'-Wisp Essence','Pitch'))
    allPotions['17'] = Potion('Mindvision Potion', 'Vitreus', {'Vitreus':(4,7), 'Victus':(1,4), 'Lux':(2,5)}, ('Phosphorus','Salt','Milk'))
    allPotions['18'] = Potion('Blinding Poison', 'Tenebrae', {'Tenebrae':(5,9), 'Venenum':(1,4), 'Vinculum':(1,4)}, ('Pitch','Bailisk Blood','Rat Tail'))
    allPotions['19'] = Potion('Water Breathing Potion', 'Aqua', {'Aqua':(5,8), 'Praecantatio':(2,5), 'Victus':(3,6)}, ('Water','Milk','Rat Tail'))
    allPotions['20'] = Potion('Slowness Potion', 'Terra', {'Terra':(4,8), 'Vinculum':(1,4), 'Aqua':(1,3)}, ('Magnetite','Milk','Salt'))
    allPotions['21'] = Potion('Plant Growth Potion', 'Herba', {'Herba':(4,7), 'Victus':(2,5), 'Terra':(1,4)}, ('Lavender','Peppermint','Salt'))
    allPotions['22'] = Potion('Barkskin Potion', 'Arbor', {'Arbor':(3,8), 'Tutamen':(1,4), 'Praecantatio':(1,4)}, ('Lavander','Rime Wood','Mana Bean'))
    
    
    
    
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
        elif opt in 'lL':
            simplePrint(allComponents,allPotions)
            continue
        else:
            raise ValueError
        
