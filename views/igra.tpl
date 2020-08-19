%import model
%rebase("base.tpl", title="Sudoku")

    <table style="background-color:ghostwhite; border:1px solid; margin: auto;">
        %for j in range(11):
        <tr>
            %for i in range(21):
            <td>{{igra.za_igro(igra.napisana_polja(igra.pravilni_del()))[j][i]}}</td>
            %end
        </tr>
        %end
    </table>

    %if poskus == model.KONEC:
        <h2>Sudoku je končan!</h2>
        <br>
        <form action="/nova_igra/" method="post">
            <button type="submit">Nova igra</button>
        </form>

    %elif poskus == model.ZE_ZASEDENO:
        <h3>Na to mesto ne moreš vstaviti številke.</h3>
        <br>
        <form action="/igra/" method="post">
            Vrstica: <input type="number" name="vrstica" min="1" max="9" required>
            Stolpec: <input type="number" name="stolpec" min="1" max="9" required>
            Številka: <input type="number" name="stevilka" min="1" max="9" required>
            <button type="submit">Pošlji ugib</button>
        </form>
    
    %elif poskus == model.NAPACEN_UGIB:
        <h3>Ta številka na to mesto ne  more priti.</h3>
        <br>
        <form action="/igra/" method="post">
            Vrstica: <input type="number" name="vrstica" min="1" max="9" required>
            Stolpec: <input type="number" name="stolpec" min="1" max="9" required>
            Številka: <input type="number" name="stevilka" min="1" max="9" required>
            <button type="submit">Pošlji ugib</button>
        </form>
    %else:
        <br>
        <br>
        <br>
        <br>
        <form action="/igra/" method="post">
            Vrstica: <input type="number" name="vrstica" min="1" max="9" required>
            Stolpec: <input type="number" name="stolpec" min="1" max="9" required>
            Številka: <input type="number" name="stevilka" min="1" max="9" required>
            <button type="submit">Pošlji ugib</button>
        </form>
    %end
