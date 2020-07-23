import random
import json



ZE_ZASEDENO = "Z"
NAPACEN_ZNAK = "#"
NAPACEN_UGIB = "&"
KONEC = "E"
NADALJUJ = "C"
TRI = "T"
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
    for vrstica in sudoku: #ali je v vsaki vrstici vseh 9 stevilk
        i = 1
        while i <= len(sudoku):
            if i not in vrstica:
                return False
            i += 1
    transponiran = transponiraj(sudoku)
    for vrstica in transponiran: #ali je v vsakem stolpcu vseh 9 stevilk
        i = 1
        while i <= len(transponiran):
            if i not in vrstica:
                return False
            i += 1
    seznam = [0,3,6]
    for j in seznam: #preveri ali je v vsakem kvadratku 3×3 vseh 9 stevilk
        li = []
        for vrstica in sudoku:
            if vrstica == sudoku[j] or vrstica == sudoku[j+1] or vrstica == sudoku[j+2]:
                l = vrstica[j:j+3]
                for m in l:
                    li.append(m)
        i = 1
        while i <= 9:
            if i not in li:
                return False
            i += 1
    return True

def preveri_delno(sudoku):
    for vrstica in sudoku:
        seznam_stevilk = []
        for element in vrstica:
            if element != 0:
                seznam_stevilk.append(element)
        for i in seznam_stevilk:
            if seznam_stevilk.count(i) > 1:
                return False
    for vrstica in transponiraj(sudoku):
        seznam_stevilk = []
        for element in vrstica:
            if element != 0:
                seznam_stevilk.append(element)
        for i in seznam_stevilk:
            if seznam_stevilk.count(i) > 1:
                return False
    seznam3 = [0,3,6]
    for j in seznam3: 
        li = []
        for vrstica in sudoku:
            if vrstica == sudoku[j] or vrstica == sudoku[j+1] or vrstica == sudoku[j+2]:
                l = vrstica[j:j+3]
                for m in l:
                    if m != 0:
                        li.append(m)
        for i in li:
            if li.count(i) > 1:
                return False
    return True

class Igra:

    def __init__(self, plosca, ugibi=None):
        self.plosca = plosca
        if ugibi is None:
            self.ugibi = []
        else:
            self.ugibi = ugibi

    def pravilni_del(self): #izpiše do sedaj rešen del
        plosca = self.plosca
        mreza = json.loads(plosca)
        for j in self.ugibi:
            vrstica = j[0]
            stolpec = j[1]
            stevilka = j[2]            
            mreza[vrstica - 1][stolpec - 1] = stevilka
        return mreza

    def napisana_polja(self, seznami):
        niz = ""
        for vrstica in seznami:
            prazno = ""
            for mesto in vrstica:
                prazno = prazno + " " + str(mesto)
            prazno += " \n"
            niz += prazno
        return niz

    def konec(self): #sudoku je rešen
        return preveri_sudoku(self.pravilni_del())

    def ugibaj(self, ugib):
        vrstica = ugib[0]
        stolpec = ugib[1]
        stevilka = ugib[2]
        if len(ugib) != 3:
            return TRI
        if vrstica not in seznam and stolpec not in seznam and stevilka not in seznam: 
            return NAPACEN_ZNAK    #preveri, da so vsi vpisani znaki stevilke med 1 in 9
        plosca = json.loads(self.plosca)
        if plosca[vrstica - 1][stolpec - 1] != 0:
            return ZE_ZASEDENO #če je na zacetni plosci na tem mestu stevilka, je sem ne mores vpisati
        for i in self.ugibi: #če je mesto novega ugiba enaka kateremu izmed prejsnjih, prejsnjega zamenja z novim
            if i[0] == vrstica and i[1] == stolpec:
                self.ugibi.replace(i, ugib)
        else:
            self.ugibi.append(ugib)
            if preveri_delno(self.pravilni_del()) == False: #sproti preveri, če ugib lahko pride na to mesto
                self.ugibi = self.ugibi[:-1]
                return NAPACEN_UGIB 
            if self.konec():
                return KONEC
            else:
                return NADALJUJ


with open("Plosce.txt", "r", encoding="utf-8") as datoteka_z_ploscami:
    mozne_plosce = [vrstica for vrstica in datoteka_z_ploscami]


def nova_igra(): 
    return Igra(random.choice(mozne_plosce))



