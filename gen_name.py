###############################################################################
# Markov Name model
# A random name generator, by Peter Corbett
###############################################################################

import random

PLACES = ['Adara', 'Adele', 'Adena', 'Adrianne', 'Alarice', 'Alvita', 'Amara', 'Ambika', 'Anastasia', 'Antonia', 
'Araceli', 'Balandria', 'Basha', 'Beryl', 'Bryn', 'Callia', 'Caryssa', 'Cassandra', 'Casondrah', 'Chatha', 'Ciara', 
'Cynara', 'Cytheria', 'Dabria', 'Darcei', 'Deandra', 'Deirdre', 'Delores', 'Desdomna', 'Devi', 'Dominique', 'Drucilla',
'Duvessa', 'Ebony', 'Fantine', 'Florri', 'Fuscienne', 'Gabi', 'Gallia', 'Hanna', 'Hedda', 'Jerica', 'Jetta', 'Joby', 
'Kacila', 'Kagami', 'Kala', 'Kallie', 'Keelia', 'Kerry', 'Kimberly', 'Killian', 'Kory', 'Lilith', 'Lucretia', 'Lysha',
'Mercedes', 'Mia', 'Mickie', 'Maura', 'Perdita', 'Quella', 'Riona', 'Safiya', 'Salina', 'Severin', 'Sidonia', 'Sirena',
'Solita', 'Tempest', 'Terra', 'Thea', 'Treva', 'Trista', 'Vala', 'Winta', 'Zarla', 'Zea','Zelda']

class Mdict:
    def __init__(self):
        self.d = {}
    def __getitem__(self, key):
        if key in self.d:
            return self.d[key]
        else:
            raise KeyError(key)
    def add_key(self, prefix, suffix):
        if prefix in self.d:
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]
    def get_suffix(self,prefix):
        l = self[prefix]
        return random.choice(l)  

class GenUser:
    """
    A name from a Markov chain
    """
    def __init__(self, chainlen = 2):
        """
        Building the dictionary
        """
        if chainlen > 10 or chainlen < 1:
            print("Chain length must be between 1 and 10, inclusive")
            sys.exit(0)
    
        self.mcd = Mdict()
        oldnames = []
        self.chainlen = chainlen
    
        for l in PLACES:
            l = l.strip()
            oldnames.append(l)
            s = " " * chainlen + l
            for n in range(0,len(l)):
                self.mcd.add_key(s[n:n+chainlen], s[n+chainlen])
            self.mcd.add_key(s[len(l):len(l)+chainlen], "\n")
    
    def new(self):
        """
        New name from the Markov chain
        """
        prefix = " " * self.chainlen
        name = ""
        suffix = ""
        while True:
            suffix = self.mcd.get_suffix(prefix)
            if suffix == "\n" or len(name) > 9:
                break
            else:
                name = name + suffix
                prefix = prefix[1:] + suffix
        return name.capitalize()
