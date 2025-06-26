import copy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._idMap = {}
        self._edges = []
        self._nodi_numArchi = {}
        self._cammino_ottimo = []
        self._peso_ottimo = 0

    def trova_cammino(self):
        for n in self._grafo.nodes():
            nuovi_successori = self.calcola_successori_ammissibili(n,[n])
            self._ricorsione([n], nuovi_successori)
        return self._cammino_ottimo, self._peso_ottimo

    def _ricorsione(self, parziale, successori):
        # caso terminale
        if len(successori) == 0:
            if len(parziale) > len(self._cammino_ottimo):
                self._cammino_ottimo = parziale
                self._peso_ottimo = self._peso_cammino(self._cammino_ottimo)
            elif len(parziale) == len(self._cammino_ottimo) and self._peso_cammino(parziale) < self._peso_ottimo:
                self._cammino_ottimo = copy.deepcopy(parziale)
                self._peso_ottimo = self._peso_cammino(self._cammino_ottimo)
        #caso ricorsivo
        else:
            for n in successori:
                parziale.append(n)
                nuovi_successori = self.calcola_successori_ammissibili(n, parziale)
                self._ricorsione(parziale, nuovi_successori)
                parziale.pop()

    def _peso_cammino(self, cammino_ottimo):
        peso = 0
        if len(cammino_ottimo) ==1:
            return peso
        for i in range(0, len(cammino_ottimo)-1):
            peso += self._grafo.get_edge_data(cammino_ottimo[i], cammino_ottimo[i+1])['weight']
        return peso

    def calcola_successori_ammissibili(self, n, parziale):
        # Un nodo può essere attraversato una sola volta.
        # Gli archi possono essere attraversati solo nella loro direzione di percorrenza
        # Nel cammino, non ci possono essere due geni consecutivi con lo stesso valore del campo Essential
        # Si possono attraversare solo archi di peso crescente (ovvero ogni nuovo arco percorso deve avere
        # peso >= del precedente).
        last_essential = parziale[-1].Essential
        if len(parziale) == 1:
            nuovi_successori =[i for i in list(self._grafo.successors(n)) if
                               i not in parziale and i.Essential != last_essential]
        else:
            last_peso = self._grafo.get_edge_data(parziale[-2], parziale[-1])['weight']
            nuovi_successori = [i for i in list(self._grafo.successors(n)) if
                                i not in parziale and i.Essential != last_essential
                                and self._grafo.get_edge_data(parziale[-1], i)['weight'] >= last_peso]

        return nuovi_successori

    def builtGraph(self, ch_min, ch_max):
        self._nodes = DAO.getNodi(ch_min, ch_max)
        self._grafo.add_nodes_from(self._nodes)

        archi = DAO.getArchi(ch_min, ch_max)
        for riga in archi:
            n1 = None
            n2 = None
            if n1 is None or n2 is None:
                for nodo1 in self._nodes:
                    if nodo1.__eq__(riga[0]):
                        n1 = nodo1
                    if nodo1.__eq__(riga[1]):
                        n2= nodo1

            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
            self._grafo.add_edge( n1, n2, weight=riga[2])
            self._edges.append((n1, n2))

    def get_node_max_uscenti(self):
        sorted_nodes = sorted(self._grafo.nodes(), key=lambda n: self._grafo.out_degree(n), reverse=True)
        # E' una lista di nodi ordinati in base al numero di archi uscenti, dal più alto al più basso.
        result = []
        for i in range(min(len(sorted_nodes), 5)):
            # Il ciclo considera al massimo i primi 5 nodi, ma se ce ne sono meno di 5, si adatta (min(...)).
            peso_tot = 0.0
            for e in self._grafo.out_edges(sorted_nodes[i], data=True):
                peso_tot += float(e[2].get("weight"))
            result.append((sorted_nodes[i], self._grafo.out_degree(sorted_nodes[i]), peso_tot))
        return result

    def getCromosomi(self):
        return DAO.getCromosomi()