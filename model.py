import random
import json

ZE_ZASEDENO = "Z"
NAPACEN_ZNAK = "#"
NAPACEN_UGIB = "&"
KONEC = "E"
NADALJUJ = "C"
TRI = "T"
seznam = [1,2,3,4,5,6,7,8,9]
ZACETEK = "S"


def transponiraj(matrika): #transponira sudoku, ki je v obliki matrike
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
    for j in range(0, 9, 3): #preveri ali je v vsakem kvadratku 3×3 vseh 9 stevilk
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
    for j in range(0, 9, 3): 
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
            for i in range(len(vrstica)):
                if i % 3 == 0 and i % 9 != 0:
                    prazno = prazno + " | " + str(vrstica[i])
                else:
                    prazno = prazno + " " + str(vrstica[i])
            prazno = prazno[1:]
            prazno += " \n"
            niz += prazno
            if vrstica == seznami[2] or vrstica == seznami[5]:
                niz += "──────+───────+──────\n"
        return niz
    
    def za_igro(self, niz):
        seznam = []
        vrstice = niz.split("\n")
        for i in vrstice:
            vrstica = []
            for j in i:
                vrstica.append(j)
            seznam.append(vrstica)
        return seznam

    def konec(self): #sudoku je rešen
        return preveri_sudoku(self.pravilni_del())

    def ugibaj(self, ugib):
        vrstica = ugib[0]
        stolpec = ugib[1]
        stevilka = ugib[2]
        if len(ugib) != 3:
            return TRI
        if vrstica not in seznam or stolpec not in seznam or stevilka not in seznam: 
            return NAPACEN_ZNAK    #preveri, da so vsi vpisani znaki stevilke med 1 in 9
        plosca = json.loads(self.plosca)
        if plosca[vrstica - 1][stolpec - 1] != 0:
            return ZE_ZASEDENO #če je na zacetni plosci na tem mestu stevilka, je sem ne mores vpisati
        else:
            self.ugibi.append(ugib)
            for i, u in enumerate(self.ugibi): #če je mesto novega ugiba enaka kateremu izmed prejsnjih, prejsnjega spremeni v novega
                if u[0] == vrstica and u[1] == stolpec and preveri_delno(self.pravilni_del()) == True:
                    self.ugibi[i] = ugib
            if preveri_delno(self.pravilni_del()) == False: #sproti preveri, če ugib lahko pride na to mesto
                self.ugibi = self.ugibi[:-1]
                return NAPACEN_UGIB 
            if self.konec():
                return KONEC


with open("Plosce.txt", "r", encoding="utf-8") as datoteka_s_ploscami:
    mozne_plosce = [vrstica for vrstica in datoteka_s_ploscami]

def nova_igra(): 
    return Igra(random.choice(mozne_plosce))


class Sudoku:

    def __init__(self, datoteka_s_stanjem, datoteka_s_ploscami="Plosce.txt"):
        self.igre = {}
        self.datoteka_s_ploscami = datoteka_s_ploscami
        self.datoteka_s_stanjem = datoteka_s_stanjem

    def prost_id_igre(self):
        if len(self.igre) == 0:
            return 0
        else:
            return max(self.igre.keys()) + 1

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        with open(self.datoteka_s_ploscami, 'r', encoding='utf-8') as dsp:
            mozne_plosce = [vrstica.strip() for vrstica in dsp]
        igra = Igra(random.choice(mozne_plosce))
        id_igre = self.prost_id_igre()
        self.igre[id_igre] = (igra, ZACETEK)
        self.zapisi_igre_v_datoteko()
        return id_igre

    def ugibaj(self, id_igre, ugib):
        self.nalozi_igre_iz_datoteke()
        igra = self.igre[id_igre][0]
        poskus = igra.ugibaj(ugib)
        self.igre[id_igre] = (igra, poskus)
        self.zapisi_igre_v_datoteko()

    def zapisi_igre_v_datoteko(self):
        with open(self.datoteka_s_stanjem, "w", encoding="utf-8") as dss:
            igre1 = {id_igre: ((igra.plosca, igra.ugibi), poskus) for id_igre, (igra, poskus) in self.igre.items()}
            json.dump(igre1, dss, ensure_ascii=False)
        return

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, "r", encoding="utf-8") as dss:
            igre = json.load(dss)
            self.igre = {int(id_igre): (Igra(plosca, ugibi), poskus) for id_igre, ((plosca, ugibi), poskus) in igre.items()}





