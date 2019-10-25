'''
Created on Oct 23, 2019

@author: TorchStone
'''
class Component:
    
    def __init__(self, location, tier, Aspects):
        assert type(tier) == int, 'Error: tier must be an int'
        assert tier in {1,2,3}, 'Error: tier must be a number 1-3'
        assert type(location) == str, 'Error: location must be a string'
        assert location in ('City','Wilds','Dungeon'), 'Error: {} is not a valid location'.format(location)
        assert type(Aspects) == dict,'Error: aspects must be a dictionary'
        self.location = location
        self.tier=tier-1 #tier is stored 
        self.Aspects=Aspects

if __name__=='__main__':        
    Milk = Component('City', 1, {"Terra":2, "Victus": '1'})
# materialsDB = {"city":
#{0:{"Milk":{"Terra":2, "Victus": 1}, "Water":{"Aqua":3}, "Salt":{"Terra":1, "Vitreus":2}},
#1:{"Pitch":{"Tenebrae":3, "Vinculum":1, "Instramentum":2}, "Saltpetre": {"Vitreus":2, "Potentia":3, "Victus":1}, "Phosporus":{"Lux":4, "Metalum":2}},
#2:{"Quicksilver": {"Metalum":2, "Motus": 4, "Venenum":2}, "Sulfer": {"Ignis":3, "Potentia":3, "Telum":3}}},
#"Wilds":{}}