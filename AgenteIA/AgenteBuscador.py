
from AgenteIA.Agente import Agente
from copy import deepcopy
import time


class AgenteBuscador(Agente):
    def __init__(self):
        Agente.__init__(self)
        self.estado_inicial = None
        self.estado_meta = None
        self.funcion_sucesor = []
        self.tecnica = None
        self.count=0

    def add_funcion(self, f):
        self.funcion_sucesor.append(f)

    def test_objetivo(self, e):
        return e == self.estado_meta

    def generar_hijos(self, e):
        hijos = []
        for fun in self.funcion_sucesor:
            h = fun(e)
            #[1,2,3]
            hijos.append(h)
        return hijos

    def get_costo(self, camino):
        raise Exception("Error: No existe implementacion")

    def get_heuristica(self, camino):
        raise Exception("Error: No existe implementacion")

    def get_funcion_a(self, camino):
        return self.get_costo(camino) + self.get_heuristica(camino)

    def mide_tiempo(funcion):
        def funcion_medida(*args, **kwards):
            inicio = time.time()
            c = funcion(*args, **kwards)
            print("Tiempo de ejecucion: ", time.time()-inicio)
            return c
        return funcion_medida

    @mide_tiempo
    def programa(self):
        frontera = [[self.estado_inicial]]
        visitados = []
        while frontera:
            if self.tecnica == "profundidad":
                camino = frontera.pop()
            else:
                camino = frontera.pop(0)
            nodo = camino[-1]
            visitados.append(nodo)
            if self.test_objetivo(nodo):
                self.acciones = camino
                break
            else:
                for hijo in self.generar_hijos(nodo):
                    if hijo not in visitados:
                        aux = deepcopy(camino)
                        aux.append(hijo)
                        frontera.append(aux)
                if self.tecnica == "costouniforme":
                    frontera.sort(key=lambda tup: self.get_costo(tup))
                elif self.tecnica == "codicioso":
                    frontera.sort(key=lambda tup: self.get_heuristica(tup))
                elif self.tecnica == "a_estrella":
                    frontera.sort(key=lambda tup: self.get_funcion_a(tup))
