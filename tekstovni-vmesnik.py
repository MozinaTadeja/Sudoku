import model


def izpis_igre(igra):
    tekst = (
        "###############################\n\n"
        "{pravilni_del}\n\n"
        "###############################"
    ).format(
        pravilni_del=igra.napisana_polja(igra.pravilni_del())   
    )
    return tekst

def izpis_konca(igra):
    tekst = "\n ##### Bravo! Sudoku je končan! #####"
    return tekst

def izpis_neenako():
    return "\n\n ##### Vpisati moraš tri številke! #####"
def izpis_napacni_znak():
    return "\n\n ##### Ugib naj vsebuje samo številke med 1 in 9! #####"

def izpis_zasedeno():
    return "\n\n ##### Na to mesto ne moreš vstaviti številke. #####"

def izpis_napacni_ugib():
    return "\n\n ##### Ta številka na to mesto ne  more priti. #####"

def zahtevaj_vnos():
    return input("Vrstica, stolpec, številka:  ")

def pozeni_vmesnik():

    igra = model.nova_igra()

    while True:
        print(izpis_igre(igra))
        poskus = zahtevaj_vnos()
        poskus_v_seznamih = [int(i) for i in poskus.split(",")]
        rezultat_ugiba = igra.ugibaj(poskus_v_seznamih)
        if rezultat_ugiba == model.TRI:
            print()
        if rezultat_ugiba == model.NAPACEN_ZNAK:
            print(izpis_napacni_znak())
        elif rezultat_ugiba == model.ZE_ZASEDENO:
            print(izpis_zasedeno())
        elif rezultat_ugiba == model.NAPACEN_UGIB:
            print(izpis_napacni_ugib())
        elif rezultat_ugiba == model.KONEC:
            print(izpis_konca(igra))
            ponovni_zagon = input("Za ponovni zagon vpišite R.").strip().upper()
            if ponovni_zagon == "R":
                igra = model.nova_igra()
            else:
                break

pozeni_vmesnik()
