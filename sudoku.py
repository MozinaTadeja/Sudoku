import model
import bottle

DATOTEKA_S_STANJEM = "stanje.json"
DATOTEKA_S_PLOSCAMI = "Plosce.txt"
SKRIVNOST = "skrivnost"


sudoku = model.Sudoku(DATOTEKA_S_STANJEM, DATOTEKA_S_PLOSCAMI)
sudoku.nalozi_igre_iz_datoteke()

@bottle.get("/")
def prva_stran():
    return bottle.template("prva_stran.tpl")

@bottle.post("/nova_igra/")
def nova_igra():
    id_igre = sudoku.nova_igra()
    bottle.response.set_cookie("idigre", "idigre{}".format(id_igre), secret=SKRIVNOST, path="/")
    bottle.redirect("/igra/")

@bottle.get("/igra/")
def pokazi_igro():
    id_igre = int(bottle.request.get_cookie("idigre", secret=SKRIVNOST)[6:])
    igra, poskus1 = sudoku.igre[id_igre]
    return bottle.template("igra.tpl", igra=igra, poskus=poskus1)


@bottle.post("/igra/")
def ugibaj():
    id_igre = int(bottle.request.get_cookie("idigre", secret=SKRIVNOST)[6:])
    ugib = [int(bottle.request.forms["vrstica"]), int(bottle.request.forms["stolpec"]), int(bottle.request.forms["stevilka"])]
    sudoku.ugibaj(id_igre, ugib)
    bottle.redirect("/igra/")

bottle.run(reloader=True, debug=True)