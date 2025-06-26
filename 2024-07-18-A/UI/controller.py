import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        # read user input
        if self._view.dd_min_ch.value is None:
            self._view.create_alert("Selezionare un valore per Chromosoma min")
            return
        else:
            ch_min = int(self._view.dd_min_ch.value)
        if self._view.dd_max_ch.value is None:
            self._view.create_alert("Selezionare un valore per Chromosoma max")
            return
        else:
            ch_max = int(self._view.dd_max_ch.value)
        if ch_min > ch_max:
            self._view.create_alert("Attenzione: deve essere Chromosoma min <= Chromosoma max")
            return

        # crea grafo e stampa info del grafo
        self._model.builtGraph(ch_min, ch_max)

        self._view.txt_result1.controls.append(ft.Text(f"Grafo creato con {len(self._model._nodes)} nodi e {len(self._model._edges)} archi"))

        self._view.btn_dettagli.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_dettagli(self, e):
        sorted_nodes = self._model.get_node_max_uscenti()
        n_nodi = min(len(sorted_nodes), 5)
        self._view.txt_result1.controls.append(ft.Text(f"\nI {n_nodi} nodi col maggior numero di archi uscenti sono:"))
        for i in range(n_nodi):
            self._view.txt_result1.controls.append(ft.Text(f"{sorted_nodes[i][0]} | "
                                                           f"num. archi uscenti: {sorted_nodes[i][1]}  | "
                                                           f"peso tot.: {sorted_nodes[i][2]}"))

        self._view.update_page()


    def handle_path(self, e):
        cammino_ottimo, peso_ottimo = self._model.trova_cammino()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Numero di nodi: {len(cammino_ottimo)} || Peso totale del cammino: {peso_ottimo}"
                                                       f" || Nodi attraversati: "))
        for n in cammino_ottimo:
            self._view.txt_result2.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

    def fillDD(self):
        cromosomi = self._model.getCromosomi()
        for n in cromosomi:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(n))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(n))
        self._view.update_page()