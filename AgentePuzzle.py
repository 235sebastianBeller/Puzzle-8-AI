from AgenteIA.AgenteBuscador import AgenteBuscador
from copy import deepcopy
import numpy as np
class AgentePuzzle(AgenteBuscador):

    def __init__(self):
        AgenteBuscador.__init__(self)
        self.estados_visitados={}
        self.acciones = []
    def set_estado_inicial(self,estado_inicial):
        self.estado_inicial=estado_inicial
        print(estado_inicial)
    def set_estado_meta(self,estado_meta):
        self.estado_meta=estado_meta
    def buscar_vacio(self,mat):
        """
        Metodo que busca en la matriz dada, la posicion del cero.
        """
        tam_filas=len(mat)
        tam_cols=len(mat[0])
        for i in range(tam_filas):
            for j in range(tam_cols):
                if mat[i][j]==0:
                    return i,j
    def es_valido(self,posx,posy,mat):
        """
        Metodo que verifica si una posicion (posx,posy) es valida en una matriz dada.
        La posicion es valida si esta dentro de los limites de la matriz.
        """
        tam_filas=len(mat)
        tam_cols=len(mat[0])
        return  0<=posx<tam_cols and  0<=posy<tam_filas
    def get_costo(self, camino):
        return len(camino)-1
    def get_heuristica_manhatthan(self, camino):
        
        mat=camino[-1]
        estado=tuple([tuple(elem) for elem in mat])
        if estado in self.estados_visitados.keys(): # si ya visite el estado no necesito calcular nuevamente
            return self.estados_visitados[estado]
        distancias = 0
        tam_filas=len(mat)
        tam_cols=len(mat[0])
        for i in range(tam_filas):
            for j in range(tam_cols):
                valor=mat[i][j]
                if valor==0:
                    valor=9
                pos_x=(valor-1)%tam_cols
                pos_y=(valor-1)//tam_filas
                distancias+=(abs(pos_x-j)+abs(pos_y-i))
        self.estados_visitados[estado]=distancias
        return distancias
    def get_heuristica_fuera_de_pos(self, camino):
        mat=camino[-1]
        estado=tuple([tuple(elem) for elem in mat])
        if estado in self.estados_visitados.keys():# si ya visite el estado no necesito calcular nuevamente
            return self.estados_visitados[estado]
        tam_filas=len(mat)
        tam_cols=len(mat[0])
        numero=1
        diferencias=0
        for i in range(tam_filas):
            for j in range(tam_cols):
                valor=mat[i][j]
                if valor==0:
                    valor=9
                if valor!=numero:
                    diferencias+=1
                numero+=1
        self.estados_visitados[estado]=diferencias
        return diferencias
    def get_heuristica_manhattan_colisiones(self,camino):
        mat=camino[-1]
        estado=tuple([tuple(elem) for elem in mat])
        if estado in self.estados_visitados.keys():# si ya visite el estado no necesito calcular nuevamente
            return self.estados_visitados[estado]
        distancias = 0
        tam_filas=len(mat)
        tam_cols=len(mat[0])
        set_filas=set()
        set_cols=set()
        for i in range(tam_filas):
            for j in range(tam_cols):
                valor=mat[i][j]
                if valor==0:
                    valor=9
                pos_x=(valor-1)%tam_cols
                pos_y=(valor-1)//tam_filas
                cols,filas=abs(pos_x-j),abs(pos_y-i)
                if pos_y in set_filas or pos_x in set_cols:
                    distancias+=3*(cols+filas)
                else:
                    distancias+=(cols+filas)
                set_filas.add(pos_y)
                set_cols.add(pos_x)
        self.estados_visitados[estado]=distancias
        return distancias
    def get_heuristica(self, camino):
        """
        Funcion que devuelve el valor de la heuristica dependiendo de la que se haya elegido.
        """
        heuristica=100
        if self.heuristica=="manhattan":
            heuristica=self.get_heuristica_manhatthan(camino)
        if self.heuristica=="manhattan_colisiones":
            heuristica=self.get_heuristica_manhattan_colisiones(camino)
        if self.heuristica=="fuera_de_posicion":
            heuristica=self.get_heuristica_fuera_de_pos(camino)
        return heuristica
    def generar_hijos(self, e):
        """
        Genera los hijos de un estado, es decir todas las posibles combinaciones que se pueden
        obtener a partir de ese estado. La generacion se hace mediante un movimiento de un elemento
        alrededor de la posicion del cero. Es decir un intercambio entre el vacio con un vecino.
        """
        dx= [0,0,-1,1]
        dy=[-1,1,0,0]
        hijos=[]
        pos_y,pos_x=self.buscar_vacio(e)
        for i in range(len(dx)):
               estado_nuevo=deepcopy(e)
               if self.es_valido(pos_x+dx[i],pos_y+dy[i],estado_nuevo):
                   aux=estado_nuevo[pos_y][pos_x]
                   estado_nuevo[pos_y][pos_x]=estado_nuevo[pos_y+dy[i]][pos_x+dx[i]]
                   estado_nuevo[pos_y+dy[i]][pos_x+dx[i]]=aux
                   hijos.append(estado_nuevo)
        return hijos
