import random


ZE_ZASEDENO = "Z"
NAPACEN_ZNAK = "#"
NAPACNA_STEVILKA = "~"
seznam = [1,2,3,4,5,6,7,8,9]


def transponiraj(matrika): #transponira sudoku v obliki matrike
    transponiranka = []
    for i in range(len(matrika[0])):
        vrstica = []
        for j in range(len(matrika)):
            vrstica.append(matrika[j][i])
        transponiranka.append(vrstica)
    return transponiranka

def preveri_sudoku(sudoku): #preveri, če je sudoku rešen pravilno
    for vrstica in sudoku:
        i = 1
        while i <= len(sudoku):
            if i not in vrstica:
                return False
            i += 1
    transponiran = transponiraj(sudoku)
    for vrstica in transponiran:
        i = 1
        while i <= len(transponiran):
            if i not in vrstica:
                return False
            i += 1
    return True
    

class Igra:

    def __init__(self, plosca, ugibi=None):
        self.plosca = plosca
        if ugibi is None:
            self.ugibi = []
        else:
            self.ugibi = ugibi

    def pravilni_del(self): #izpise do sedaj resen del
        mreza = self.plosca
        for j in self.ugibi:
            vrstica = j[0][0]
            stolpec = j[0][1]
            stevilka = j[1]            
            mreza[vrstica - 1][stolpec - 1] = stevilka
        return mreza

    def konec(self): #sudoku je rešen
        return preveri_sudoku(self.pravilni_del())

    def ugibaj(self, ugib):
        vrstica = ugib[0][0]
        stolpec = ugib[0][1]
        stevilka = ugib[1]
        if vrstica not in seznam and stolpec not in seznam and stevilka not in seznam: 
            return NAPACEN_ZNAK    #preveri, da so vsi vpisani znaki stevilke med 1 in 9
        if self.plosca[vrstica - 1][stolpec - 1] != 0:
            return ZE_ZASEDENO #če je na zacetni plosci na tem mestu stevilka, je sem ne mores vpisati
        for i in self.ugibi: #če je pozicija novega ugiba enaka kateremu izmed prejsnjih, prejsnjega zamenja z novim
            if i[0][0] == vrstica and i[0][1] == stolpec:
                self.ugibi.replace(i, ugib)
        else:
            self.ugibi.append(ugib)


with open("Plosce.txt", "r", encoding="utf-8") as datoteka_z_ploscami:
    mozne_plosce = [vrstica for vrstica in datoteka_z_ploscami]


def nova_igra():
    return Igra(random.choice(mozne_plosce))

