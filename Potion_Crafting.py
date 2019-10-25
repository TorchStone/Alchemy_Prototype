'''
Created on Oct 23, 2019

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
        
        assert keyAspect == recipe[max(recipe.keys())], 'Error: keyAspect must be the largest aspect in the recipe'
        assert type(rRecipe) == tuple, 'Error: Recomended Recipe must be an set'
        
        self.name = name
        self.keyAspect = keyAspect
        self.recipe = recipe
        self.rRecipe = rRecipe
    def __str__(self):
        return '{}\n  is associated with {}\n  the recipe is {}\n  and can be brewed with {}'.format(self.name,self.keyAspect,self.recipe,self.rRecipe)
    def brew(self, cauldren):
        assert type(cauldren) == dict, 'Error: Input must be a dictionary'
        return all([( max(r) >= cauldren[a] and cauldren[a] >= min(r)) for r,a in self.recipe.items()])
if __name__=='__main__':
    allComponents = {}
    
    ##CITY##
    allComponents['000'] = Component('Milk', 'City', 1, {"Terra":2, "Victus": 1})
    allComponents['001'] = Component('Water', 'City', 1, {"Aqua":3})
    allComponents['002'] = Component('Salt', 'City', 1, {"Terra":1, "Vitreus": 2})
    allComponents['010'] = Component('Pitch', 'City', 2, {"Tenebrae":3, "Vinculum": 1, "Instramentum":1})
    allComponents['011'] = Component('Saltpetre', 'City', 2, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['012'] = Component('Phosphorus', 'City', 2, {"Lux":4, "Metalum": 2})
    allComponents['020'] = Component('Quicksilver', 'City', 3, {"Metalum":2, "Motus": 6, "Venenum":2})
    allComponents['021'] = Component('Sulfur', 'City', 3, {"Ignis":3, "Potentia": 3, "Telum":3})
    allComponents['022'] = Component('Arsenic', 'City', 3, {"Venenum":6, "Mortus": 3})
    
    ##WILDS##
    allComponents['100'] = Component('lavander', 'Wilds', 1, {"Herba":2, "Victus": 1})
    allComponents['101'] = Component('Peppermint', 'Wilds', 1, {"Herba":2, "Gelum": 1})
    allComponents['102'] = Component('honey', 'Wilds', 1, {"Vinculum":1, "Fames": 2})
    allComponents['110'] = Component('Galena', 'Wilds', 2, {"Metalum":3, "Permutatio": 3})
    allComponents['111'] = Component('Magnetite', 'Wilds', 2, {"Metalum":2, "Instramentum": 4})
    allComponents['112'] = Component('Cinnabar', 'Wilds', 2, {"Tutamen":4, "Metalum": 2})
    allComponents['120'] = Component('Griffon Talon', 'Wilds', 3, {"Telum":4, "voltus": 4, "Aer":1})
    allComponents['121'] = Component('Owlbear Further', 'Wilds', 3, {"Bestia":4, "Tutamen": 1, "Aer":4})
    allComponents['122'] = Component('Treant Bark', 'Wilds', 3, {"Arbor":5, "Praecantatio": 3})
    
    ##Dungeon##
    allComponents['200'] = Component('Saltpetre', 'Dungeon', 1, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['201'] = Component('Saltpetre', 'Dungeon', 1, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['202'] = Component('Saltpetre', 'Dungeon', 1, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['210'] = Component('Saltpetre', 'Dungeon', 2, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['211'] = Component('Saltpetre', 'Dungeon', 2, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['212'] = Component('Saltpetre', 'Dungeon', 2, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['220'] = Component('Saltpetre', 'Dungeon', 3, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['221'] = Component('Saltpetre', 'Dungeon', 3, {"Vitreus":2, "Potentia": 3, "Victus":1})
    allComponents['222'] = Component('Saltpetre', 'Dungeon', 3, {"Vitreus":2, "Potentia": 3, "Victus":1})
    
    test_potion = Potion('test', 'Aqua', {(4,10):'Aqua', (0,3):'Terra', (0,1):'Victus'}, ('Water','Water','Milk'))
    print(test_potion)
# materialsDB = {"city":
#{0:{"Milk":{"Terra":2, "Victus": 1}, "Water":{"Aqua":3}, "Salt":{"Terra":1, "Vitreus":2}},
#1:{"Pitch":{"Tenebrae":3, "Vinculum":1, "Instramentum":2}, "Saltpetre": {"Vitreus":2, "Potentia":3, "Victus":1}, "Phosporus":{"Lux":4, "Metalum":2}},
#2:{"Quicksilver": {"Metalum":2, "Motus": 4, "Venenum":2}, "Sulfer": {"Ignis":3, "Potentia":3, "Telum":3}}},
#"Wilds":{}}